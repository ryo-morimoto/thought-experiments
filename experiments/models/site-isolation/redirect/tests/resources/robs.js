// Runner for the redirect-chain popup scenarios (redirect/RESULTS.md). The
// test page is the opener (origin A = HTTPS_ORIGIN, headers from its .headers
// file); it defines OPENER and SCEN and calls runRedirect(SCEN). Every
// observation is a passing subtest "OBS <sid>.<kind> :: <value>"; nothing is
// asserted. Kinds: closed (opener's popup.closed), opener (popup's
// window.opener != null), coi (popup's crossOriginIsolated), hlen (popup's
// history.length). The settle time (500 ms) is popup_test()'s in
// html/cross-origin-opener-policy/resources/popup-test.js.
setup({explicit_done: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
function obs(row, value) { test(() => {}, `OBS ${row} :: ${value}`); }
const ORIGIN = {"same-origin": get_host_info().HTTPS_ORIGIN,
                "same-site": get_host_info().HTTPS_REMOTE_ORIGIN,
                "cross-site": get_host_info().HTTPS_NOTSAMESITE_ORIGIN};
function execUrl(origin, uuid, coop, coep) {
  let pipe = "";
  if (coop !== "unsafe-none") pipe += `|header(Cross-Origin-Opener-Policy,${coop})`;
  if (coep !== "unsafe-none") pipe += `|header(Cross-Origin-Embedder-Policy,${coep})`;
  return `${origin}/common/dispatcher/executor.html?uuid=${uuid}&pipe=${encodeURIComponent(pipe)}`;
}
function chainUrl(sc, uuid) {
  let url = execUrl(ORIGIN[sc.fin.rel], uuid, sc.fin.coop, sc.fin.coep);
  for (const h of [...sc.hops].reverse()) {
    const q = new URLSearchParams({coop: h.coop, coep: h.coep, next: url});
    url = `${ORIGIN[h.rel]}/redirect-si/resources/hop.py?${q}`;
  }
  return url;
}
function withTimeout(p, ms) {
  return Promise.race([p, sleep(ms).then(() => "timeout")]);
}
async function scenario(sc) {
  const ptok = token(), rtok = token();
  const url = chainUrl(sc, ptok);
  let popup;
  if (sc.st === "blank") {
    popup = window.open(url);
  } else {
    const dtok = token();
    popup = window.open(execUrl(ORIGIN["same-origin"], dtok, OPENER.coop, OPENER.coep));
    send(dtok, `send("${rtok}", "doc")`);
    if (await withTimeout(receive(rtok), 15000) !== "doc") return {err: "doc-load"};
    send(dtok, `location.href = ${JSON.stringify(url)};`);
  }
  send(ptok, `send("${rtok}", JSON.stringify({opener: window.opener != null,
      coi: self.crossOriginIsolated, hlen: history.length}))`);
  const r = await withTimeout(receive(rtok), 20000);
  if (r === "timeout") { try { popup.close(); } catch (e) {} return {err: "final-load"}; }
  const m = JSON.parse(r);
  await sleep(500);
  m.closed = popup.closed;
  send(ptok, "close()");
  try { popup.close(); } catch (e) {}
  await sleep(100);
  return m;
}
async function runRedirect(list) {
  for (const sc of list) {
    let m;
    try { m = await scenario(sc); } catch (e) { m = {err: "exc:" + e.name}; }
    if (m.err) { obs(`${sc.id}.error`, m.err); continue; }
    obs(`${sc.id}.closed`, String(m.closed).toUpperCase());
    obs(`${sc.id}.opener`, String(m.opener).toUpperCase());
    obs(`${sc.id}.coi`, String(m.coi).toUpperCase());
    obs(`${sc.id}.hlen`, String(m.hlen));
  }
}
