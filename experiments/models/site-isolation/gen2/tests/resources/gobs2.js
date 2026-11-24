// Runners for the gen2 scenarios (gen2/RESULTS.md). A generated test page
// defines HOSTS, PORTS and SCEN and calls one runner. Each observation is a
// passing subtest "OBS <sid>.<kind> :: <value>". Nothing is asserted.
// The popup runner uses getExecutorPath / getPopupHasOpener from
// /html/cross-origin-opener-policy/resources/popup-test.js (loaded at run time).
setup({explicit_done: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
const within = (p, ms, v) => Promise.race([p, sleep(ms).then(() => v)]);
function obs(row, value) { test(() => {}, `OBS ${row} :: ${value}`); }
function rurl(scheme, host, path, port) {
  return `${scheme}://${HOSTS[host]}:${port || PORTS[scheme]}/gen2-si/resources/${path}`;
}
async function fo(url, init) {
  try { const r = await fetch(url, init); return r.type; }
  catch (e) { return e.name === "TypeError" ? "error" : "exc:" + e.name; }
}
function imgOutcome(url) {
  return within(new Promise(resolve => {
    const el = document.createElement("img");
    el.onload = () => { el.remove(); resolve("load"); };
    el.onerror = () => { el.remove(); resolve("error"); };
    el.src = url;
    document.body.appendChild(el);
  }), 15000, "timeout");
}

// P: opener (this page, COOP from .headers) opens the popup directly, via
// about:blank then a navigation, or with noopener. Value TRUE: severed
// (closed from here and opener null there; with noopener only the latter),
// FALSE: not severed, else the raw pair.
async function popupOne(sc) {
  const ptok = token(), rtok = token();
  const origin = `${sc.s}://${HOSTS[sc.h]}:${PORTS[sc.s]}`;
  const u = getExecutorPath(ptok, origin, {coop: sc.pc === "unsafe-none" ? undefined : sc.pc});
  let w = null;
  if (sc.mode === "noopener") window.open(u, "_blank", "noopener");
  else if (sc.mode === "blank") { w = window.open("about:blank"); w.location.href = u; }
  else w = window.open(u);
  send(ptok, `send('${rtok}', 'loaded');`);
  if (await within(receive(rtok), 20000, "timeout") !== "loaded") return "timeout";
  await sleep(500);
  const closed = w ? w.closed : null;
  const op = await within(getPopupHasOpener(ptok), 10000, "timeout");
  send(ptok, "close()");
  await sleep(150);
  if (sc.mode === "noopener") return op === "false" ? "TRUE" : op === "true" ? "FALSE" : "raw:" + op;
  if (closed && op === "false") return "TRUE";
  if (!closed && op === "true") return "FALSE";
  return `closed=${closed},opener=${op}`;
}
async function runPopup(list) {
  for (const sc of list) {
    let v;
    try { v = await popupOne(sc); } catch (e) { v = "exc:" + e.name; }
    obs(`${sc.id}.sev`, v);
  }
  done();
}

// O: each scenario in its own noopener popup (a fresh browsing context group).
async function runOAC(list) {
  for (const sc of list) {
    const uuid = token();
    const q = new URLSearchParams({uuid, coi: sc.coi ? "1" : "0", h0: sc.h[0], h1: sc.h[1], h2: sc.h[2]});
    window.open(rurl(sc.s, "a", "oac-top.py?" + q), "_blank", "noopener");
    let res;
    try { res = JSON.parse(await within(receive(uuid), 30000, '{"error":"timeout"}')); }
    catch (e) { res = {error: "exc:" + e.name}; }
    for (const k of ["g0", "g1", "g2", "dd"]) obs(`${sc.id}.${k}`, res.error ? "error:" + res.error : res[k]);
  }
  done();
}

// S: sandboxed iframes in batches; the child posts its values to this page.
const SKINDS = ["coi", "sec", "orig", "fself", "fx", "fhttp", "ihttp"];
async function runSandbox(list) {
  const got = {}, alive = {}, late = [], recorded = {};
  window.addEventListener("message", e => {
    const m = e.data;
    if (m && m.g2alive) alive[m.sid] = true;
    if (!m || !m.g2) return;
    got[m.sid] = m;
    if (recorded[m.sid]) late.push(m.sid);
  });
  const BATCH = 27, WAIT = 12000;
  for (let i = 0; i < list.length; i += BATCH) {
    const batch = list.slice(i, i + BATCH);
    const frames = batch.map(sc => {
      const f = document.createElement("iframe");
      if (sc.sb === "scripts") f.sandbox = "allow-scripts";
      if (sc.sb === "scripts-so") f.sandbox = "allow-scripts allow-same-origin";
      const q = new URLSearchParams({sid: sc.id, coep: sc.coep, corp: sc.corp,
        fx: rurl("https", sc.o, `res.py?sid=${sc.id}&k=fx`),
        fh: rurl("http", sc.o, `res.py?sid=${sc.id}&k=fhttp`),
        ih: rurl("http", sc.o, `img.py?sid=${sc.id}&corp=cross-origin`, PORTS.https)});
      f.src = rurl("https", sc.h, "sframe.py?" + q);
      document.body.appendChild(f);
      return f;
    });
    const start = performance.now();
    while (!batch.every(sc => got[sc.id]) && performance.now() - start < WAIT) await sleep(100);
    for (const sc of batch) {
      recorded[sc.id] = true;
      const m = got[sc.id];
      // alive without the full report: the child ran but did not finish in time.
      obs(`${sc.id}.load`, m ? "loaded" : alive[sc.id] ? "noreport" : "blocked");
      if (m) for (const k of SKINDS) obs(`${sc.id}.${k}`, m[k]);
    }
    frames.forEach(f => f.remove());
    await sleep(200);
  }
  await sleep(1000);
  test(() => {}, `LATE :: ${late.join(" ") || "none"}`);
  done();
}

// C: fetch() (no-cors) or <img> from this top-level page.
async function corpOne(sc) {
  const path = (sc.dest === "img" ? "img.py" : "res.py") + `?sid=${sc.id}&corp=${sc.corp}`;
  const u = sc.rs === "http-tls" ? rurl("http", sc.h, path, PORTS.https) : rurl(sc.rs, sc.h, path);
  return sc.dest === "img" ? imgOutcome(u) : within(fo(u, {mode: "no-cors"}), 15000, "timeout");
}
async function runCorp(list) {
  for (let i = 0; i < list.length; i += 12) {
    const batch = list.slice(i, i + 12);
    const vals = await Promise.all(batch.map(sc => corpOne(sc).catch(e => "exc:" + e.name)));
    batch.forEach((sc, j) => obs(`${sc.id}.r`, vals[j]));
  }
  done();
}
