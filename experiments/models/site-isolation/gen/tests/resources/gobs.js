// Runner for the generated scenarios (gen/RESULTS.md). The top-level test page
// is level 0; it defines HOSTS, PORTS, TOP_ID, TOP_TGT and SCEN, then calls
// runGen(). Each observation is a passing subtest "OBS <row> :: <value>",
// row = <scenario>.<level>.<kind>. Nothing is asserted.
setup({explicit_done: true});
const BATCH = 27, WAIT = 12000;
const sleep = ms => new Promise(r => setTimeout(r, ms));
function obs(row, value) { test(() => {}, `OBS ${row} :: ${value}`); }
async function fo(url, init) {
  try { const r = await fetch(url, init); return r.type; }
  catch (e) { return e.name === "TypeError" ? "error" : "exc:" + e.name; }
}
function rurl(scheme, host, path) {
  return `${scheme}://${HOSTS[host]}:${PORTS[scheme]}/gen-si/resources/${path}`;
}
// URL of level l (1-based) of scenario sc, with the deeper levels nested in "next".
function frameUrl(sc, l) {
  const lv = sc.lv[l - 1];
  const q = new URLSearchParams({sid: sc.id, lvl: String(l), coep: lv.coep, corp: lv.corp});
  if (l < sc.lv.length) q.set("next", frameUrl(sc, l + 1));
  else q.set("tgt", rurl("https", sc.t, `res.py?sid=${sc.id}`));
  return rurl(lv.s, lv.h, "frame.py?" + q.toString());
}
async function runGen() {
  obs(`${TOP_ID}.0.coi`, String(self.crossOriginIsolated));
  obs(`${TOP_ID}.0.sec`, String(self.isSecureContext));
  const t0 = rurl("https", TOP_TGT, `res.py?sid=${TOP_ID}`);
  obs(`${TOP_ID}.0.fetch`, await fo(t0 + "&c=0", {mode: "no-cors"}));
  obs(`${TOP_ID}.0.fetchc`, await fo(t0 + "&c=1", {mode: "no-cors", credentials: "include"}));
  const got = {}, recorded = {}, late = [];
  window.addEventListener("message", e => {
    const m = e.data;
    if (!m || !m.gen) return;
    (got[m.sid] = got[m.sid] || {})[m.lvl] = m;
    if (recorded[m.sid]) late.push(`${m.sid}.${m.lvl}`);
  });
  for (let i = 0; i < SCEN.length; i += BATCH) {
    const batch = SCEN.slice(i, i + BATCH);
    const onload = {};
    const frames = batch.map(sc => {
      const f = document.createElement("iframe");
      f.onload = () => { onload[sc.id] = true; };
      f.src = frameUrl(sc, 1);
      document.body.appendChild(f);
      return f;
    });
    const complete = () => batch.every(sc => {
      const g = got[sc.id] || {};
      for (let l = 1; l <= sc.lv.length; l++) if (!g[String(l)]) return false;
      return true;
    });
    const start = performance.now();
    while (!complete() && performance.now() - start < WAIT) await sleep(100);
    for (const sc of batch) {
      const g = got[sc.id] || {};
      recorded[sc.id] = true;
      obs(`${sc.id}.1.onload`, onload[sc.id] ? "fired" : "none");
      for (let l = 1; l <= sc.lv.length; l++) {
        const m = g[String(l)];
        if (!m) { obs(`${sc.id}.${l}.load`, "blocked"); break; }
        obs(`${sc.id}.${l}.load`, "loaded");
        obs(`${sc.id}.${l}.coi`, m.coi);
        obs(`${sc.id}.${l}.sec`, m.sec);
        if (l === sc.lv.length) {
          obs(`${sc.id}.${l}.fetch`, m.fetch);
          obs(`${sc.id}.${l}.fetchc`, m.fetchc);
        }
      }
    }
    frames.forEach(f => f.remove());
    await sleep(200);
  }
  await sleep(1000);
  test(() => {}, `LATE :: ${late.join(" ") || "none"}`);
  done();
}
