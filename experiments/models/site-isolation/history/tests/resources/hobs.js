// Runner for the session-history / bfcache scenarios (history/RESULTS.md). The
// test page is the opener (origin A = HTTPS_ORIGIN, headers from its .headers
// file); it defines SCEN and calls runHistory(SCEN). Every observation is a
// passing subtest "OBS <sid>.<kind> :: <value>"; nothing is asserted.
// Documents are the back-forward-cache executor
// (html/browsers/browsing-the-web/back-forward-cache/resources/executor.html)
// with COOP/COEP header pipes, driven through RemoteContext as in that
// directory's helper.sub.js: navigations and history.go() are started from
// prepareNavigation() so no polling fetch is in flight.
// Kinds: hit1/hit2 (the k-th traversal target was restored from bfcache:
// pageshow persisted with loadCount 1), closed (opener's popup.closed),
// opener (final doc's window.opener != null), coi (crossOriginIsolated),
// hlen (history.length). Settle 500 ms as popup_test() in
// html/cross-origin-opener-policy/resources/popup-test.js.
setup({explicit_done: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
function obs(row, value) { test(() => {}, `OBS ${row} :: ${value}`); }
const ORIGIN = {"same-origin": get_host_info().HTTPS_ORIGIN,
                "cross-site": get_host_info().HTTPS_NOTSAMESITE_ORIGIN};
const EXEC = "/html/browsers/browsing-the-web/back-forward-cache/resources/executor.html";
function execUrl(origin, uuid, coop, coep) {
  let pipe = "";
  if (coop !== "unsafe-none") pipe += `|header(Cross-Origin-Opener-Policy,${coop})`;
  if (coep !== "unsafe-none") pipe += `|header(Cross-Origin-Embedder-Policy,${coep})`;
  return `${origin}${EXEC}?uuid=${uuid}&pipe=${encodeURIComponent(pipe)}`;
}
function withTimeout(p, ms) {
  return Promise.race([p, sleep(ms).then(() => { throw new Error("timeout"); })]);
}
const showP = () => window.pageShowPromise.then(() => true);
const openWS = (u) => new Promise(res => {
  window.__ws = new WebSocket(u);
  window.__ws.onopen = () => res(true);
  window.__ws.onerror = () => res(false);
});
async function settle(ctx, doc, step) {
  try { await withTimeout(ctx.execute_script(showP), 15000); }
  catch (e) { throw new Error(`load-${step}`); }
  const st = await withTimeout(ctx.execute_script(() =>
      [window.loadCount, window.isPageshowFired, window.isPageshowPersisted]), 10000);
  const hit = st[0] === 1 && st[1] === true && st[2] === true;
  if (!hit && doc.ws) {
    if (!await withTimeout(ctx.execute_script(openWS, [WSS_ECHO]), 10000)) throw new Error(`ws-${step}`);
  }
  return {hit, st};
}
async function scenario(sc) {
  const ctx = sc.docs.map(() => new RemoteContext(token()));
  const url = j => execUrl(ORIGIN[sc.docs[j].rel], ctx[j].context_id, sc.docs[j].coop, sc.docs[j].coep);
  const popup = sc.st === "popup" ? window.open(url(0)) : window.open(url(0), "_blank", "noopener");
  const out = {hits: [], odd: []};
  await settle(ctx[0], sc.docs[0], "open");
  let es = [0], cur = 0, nd = 1;
  for (const [i, op] of sc.ops.entries()) {
    const from = ctx[es[cur]];
    if (op === 0) {
      const j = nd++;
      await withTimeout(from.execute_script(u => { prepareNavigation(() => { location.href = u; }); }, [url(j)]), 10000);
      await settle(ctx[j], sc.docs[j], `nav${i}`);
      es = es.slice(0, cur + 1); es.push(j); cur = es.length - 1;
    } else {
      const t = cur + op;
      await withTimeout(from.execute_script(d => { prepareNavigation(() => { history.go(d); }); }, [op]), 10000);
      const r = await settle(ctx[es[t]], sc.docs[es[t]], `trav${i}`);
      out.hits.push(r.hit);
      if (!r.hit && !(r.st[0] === 2 && r.st[1] === false)) out.odd.push(r.st.join("/"));
      cur = t;
    }
  }
  const last = ctx[es[cur]];
  const m = await withTimeout(last.execute_script(() =>
      ({opener: window.opener != null, coi: self.crossOriginIsolated, hlen: history.length})), 10000);
  await sleep(500);
  if (popup) m.closed = popup.closed;
  Object.assign(out, m);
  try { await withTimeout(last.execute_script(() => { setTimeout(() => window.close(), 0); return true; }), 5000); }
  catch (e) {}
  try { if (popup) popup.close(); } catch (e) {}
  await sleep(200);
  return out;
}
async function runHistory(list) {
  for (const sc of list) {
    let m;
    try { m = await scenario(sc); } catch (e) { obs(`${sc.id}.error`, e.message); continue; }
    m.hits.forEach((h, k) => obs(`${sc.id}.hit${k + 1}`, String(h).toUpperCase()));
    if (m.odd.length) obs(`${sc.id}.odd`, m.odd.join(","));
    if (sc.st === "popup") obs(`${sc.id}.closed`, String(m.closed).toUpperCase());
    obs(`${sc.id}.opener`, String(m.opener).toUpperCase());
    obs(`${sc.id}.coi`, String(m.coi).toUpperCase());
    obs(`${sc.id}.hlen`, String(m.hlen));
  }
}
