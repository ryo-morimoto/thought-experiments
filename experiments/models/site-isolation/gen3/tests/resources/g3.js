// Runners for the gen3 scenarios (gen3/RESULTS.md). A generated test page
// defines HOSTS, PORT and SCEN and calls one runner. Each observation is a
// passing subtest "OBS <sid>.<kind> :: <value>". Nothing is asserted.
// send/receive/token come from /common/dispatcher/dispatcher.js and
// /common/utils.js (loaded from the WPT clone at run time).
setup({explicit_done: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
const within = (p, ms, v) => Promise.race([p, sleep(ms).then(() => v)]);
function obs(row, value) { test(() => {}, `OBS ${row} :: ${value}`); }
const ORIGIN = h => `https://${HOSTS[h]}:${PORT}`;
const rurl = (h, path) => `${ORIGIN(h)}/gen3-si/resources/${path}`;
const TOK = {s: "allow-scripts", p: "allow-popups", e: "allow-popups-to-escape-sandbox",
             so: "allow-same-origin", t: "allow-top-navigation",
             tu: "allow-top-navigation-by-user-activation"};
const sbAttr = sb => sb.split("-").map(t => TOK[t]).join(" ");
function messages(pred) {
  const got = {};
  window.addEventListener("message", e => { if (e.data && pred(e.data)) got[e.data.sid] = e.data; });
  return got;
}
async function until(cond, ms) {
  const t0 = performance.now();
  while (!cond() && performance.now() - t0 < ms) await sleep(100);
}

// X: a sandboxed frame calls window.open; the popup reports through the dispatcher.
async function runX(list) {
  const got = messages(m => m.g3x);
  for (let i = 0; i < list.length; i += 7) {
    const batch = list.slice(i, i + 7);
    const frames = batch.map(sc => {
      sc.uuid = token();
      const f = document.createElement("iframe");
      if (sc.sb !== "none") f.sandbox = sbAttr(sc.sb);
      const q = new URLSearchParams({sid: sc.id, pu: rurl(sc.ph, `xpop.py?uuid=${sc.uuid}`)});
      f.src = rurl(sc.fh, "xframe.py?" + q);
      document.body.appendChild(f);
      return f;
    });
    await until(() => batch.every(sc => got[sc.id]), 10000);
    await Promise.all(batch.map(async sc => {
      const m = got[sc.id];
      if (!m) { obs(`${sc.id}.pop`, "noreport"); return; }
      obs(`${sc.id}.fdd`, m.fdd);
      obs(`${sc.id}.pop`, m.opened);
      if (m.opened !== "TRUE") return;
      let p;
      try { p = JSON.parse(await within(receive(sc.uuid), 10000, '{"porig":"noreport","pdd":"noreport"}')); }
      catch (e) { p = {porig: "exc", pdd: "exc"}; }
      obs(`${sc.id}.porig`, p.porig);
      obs(`${sc.id}.pdd`, p.pdd);
    }));
    await sleep(6500);   // the frames close their popups after 6 s
    frames.forEach(f => f.remove());
  }
  done();
}

// Y: in a popup (the top), a sandboxed frame sets top.location.
async function runY(list) {
  for (const sc of list) {
    const uuid = token();
    const q = new URLSearchParams({uuid, sb: sc.sb === "none" ? "" : sbAttr(sc.sb),
      sbon: sc.sb === "none" ? "0" : "1",
      fu: rurl(sc.fh, `yframe.py?uuid=${uuid}&nav=${encodeURIComponent(rurl("a", "ynav.py?uuid=" + uuid))}`)});
    const w = window.open(rurl("a", "ytop.py?" + q));
    const seen = [], t0 = performance.now();
    while (performance.now() - t0 < 7000) {
      const m = await within(receive(uuid), 7000 - (performance.now() - t0), null);
      if (m === null) break;
      seen.push(m);
      if (m === "nav") break;
    }
    obs(`${sc.id}.tnav`, seen.includes("nav") ? "nav" : seen.some(m => m.startsWith("threw")) ? "threw"
        : seen.includes("noexc") ? "silent" : "none");
    try { w.close(); } catch (e) {}
    await sleep(300);
  }
  done();
}

// R: fetch() through 307 redirects; the last URL stores the Origin and
// Referer headers it got; this page takes them back (same origin).
function chainUrl(hosts, last, firstQuery) {
  let u = last;
  for (let j = hosts.length - 2; j >= 0; j--)
    u = rurl(hosts[j], `rd.py?to=${encodeURIComponent(u)}${j === 0 ? firstQuery : ""}`);
  return u;
}
async function rOne(sc) {
  const key = token(), hs = sc.urls.split("-");
  const u = chainUrl(hs, rurl(hs[hs.length - 1], `echo.py?key=${key}`), sc.hrp ? `&rp=${sc.hrp}` : "");
  const init = {mode: sc.mode, method: sc.meth, referrerPolicy: sc.rp};
  if (sc.meth === "POST") init.body = "x";
  let res;
  try { res = (await fetch(u, init)).type; } catch (e) { res = "error"; }
  let h = {};
  try { h = await (await fetch(rurl("a", `take.py?key=${key}`))).json(); } catch (e) { h = {err: 1}; }
  const org = h.err ? "takeerr" : h.origin === undefined || h.origin === null ? "absent"
      : h.origin === "null" ? "null" : h.origin === location.origin ? "self" : "other:" + h.origin;
  const ref = h.err ? "takeerr" : !h.referer ? "none" : h.referer === location.href ? "full"
      : h.referer === location.origin + "/" ? "origin" : "other:" + h.referer;
  return {res, org, ref, recorded: h.recorded};
}
async function runR(list) {
  for (let i = 0; i < list.length; i += 8) {
    const batch = list.slice(i, i + 8);
    const vals = await Promise.all(batch.map(sc => rOne(sc).catch(e => ({res: "exc", org: "exc", ref: "exc"}))));
    batch.forEach((sc, j) => {
      obs(`${sc.id}.res`, vals[j].res);
      obs(`${sc.id}.org`, vals[j].recorded ? vals[j].org : "notreached");
      obs(`${sc.id}.ref`, vals[j].recorded ? vals[j].ref : "notreached");
    });
  }
  done();
}

// K: <img> through redirects in a frame with CSP img-src 'self' [+ extra].
async function runK(list) {
  const got = messages(m => m.g3k);
  for (let i = 0; i < list.length; i += 20) {
    const batch = list.slice(i, i + 20);
    const frames = batch.map(sc => {
      const hs = sc.urls.split("-");
      const last = rurl(hs[hs.length - 1], `pix.py?k=${token()}`);
      sc.list = [];
      let u = last;
      sc.list.unshift(u);
      for (let j = hs.length - 2; j >= 0; j--) {
        u = rurl(hs[j], `rd.py?to=${encodeURIComponent(u)}`);
        sc.list.unshift(u);
      }
      const f = document.createElement("iframe");
      f.src = rurl("a", "kframe.py?" + new URLSearchParams({sid: sc.id, img: u,
        ex: sc.ex === "none" ? "" : ORIGIN(sc.ex)}));
      document.body.appendChild(f);
      return f;
    });
    await until(() => batch.every(sc => got[sc.id]), 15000);
    for (const sc of batch) {
      const m = got[sc.id];
      if (!m) { obs(`${sc.id}.img`, "noreport"); continue; }
      obs(`${sc.id}.img`, m.img);
      const o = u => new URL(u).origin;
      const cls = b => b === sc.list[0] ? "orig" : sc.list.includes(b) ? "cur"
          : (b === o(sc.list[0]) || b === o(sc.list[0]) + "/") ? "orig-origin"
          : sc.list.some(u => b === o(u) || b === o(u) + "/") ? "cur-origin" : "other:" + b;
      obs(`${sc.id}.bu`, m.bu.length === 0 ? "none" : m.bu.map(cls).join("+"));
    }
    frames.forEach(f => f.remove());
  }
  done();
}

// D, N: each scenario in its own noopener popup (a fresh browsing context
// group); every document there sends Origin-Agent-Cluster: ?0.
async function popupScen(sc, kinds, extra) {
  const uuid = token();
  const q = new URLSearchParams(Object.assign({uuid, sid: sc.id, dom: HOSTS.a}, extra));
  window.open(rurl("a", "dpop.py?" + q), "_blank", "noopener");
  let res;
  try { res = JSON.parse(await within(receive(uuid), 20000, '{"error":"timeout"}')); }
  catch (e) { res = {error: "exc"}; }
  for (const k of kinds) obs(`${sc.id}.${k}`, res.error ? "error:" + res.error : res[k]);
}
async function runD(list) {
  for (const sc of list) {
    await popupScen(sc, ["pc", "cp", "cset"], {fam: "D", set: sc.set, csb: sc.csb,
      cu: rurl(sc.ch, `dchild.py?sid=${sc.id}&set=${sc.set}&dom=${sc.ch === "b" ? HOSTS.b : HOSTS.a}`)});
  }
  done();
}
async function runN(list) {
  for (const sc of list) {
    await popupScen(sc, ["reuse"], {fam: "N", dd: sc.dd, how: sc.how,
      cu: rurl(sc.tgt, `nchild.py?sid=${sc.id}`)});
  }
  done();
}

// W: dedicated, shared and blob: workers; each reports crossOriginIsolated
// and a no-cors fetch() to b without CORP.
const WSRC = `
async function g3run() {
  let fx;
  try { fx = (await fetch(FX, {mode: "no-cors"})).type; } catch (e) { fx = "error"; }
  return {coi: String(self.crossOriginIsolated).toUpperCase(), fx};
}
if (typeof SharedWorkerGlobalScope !== "undefined" && self instanceof SharedWorkerGlobalScope)
  onconnect = e => { const p = e.ports[0]; g3run().then(m => p.postMessage(m)); };
else g3run().then(m => postMessage(m));
`;
function wOne(sc) {
  return new Promise(resolve => {
    const fx = rurl("b", `nores.py?k=${token()}`);
    const q = new URLSearchParams({coep: sc.wc, fx, k: token()});
    const url = rurl("a", "wscript.py?" + q);
    let w;
    try {
      if (sc.kind === "shared") {
        w = new SharedWorker(url);
        w.port.onmessage = e => resolve(e.data);
        w.onerror = () => resolve("error");
      } else {
        const src = sc.kind === "blob"
          ? URL.createObjectURL(new Blob([`const FX = ${JSON.stringify(fx)};` + WSRC], {type: "text/javascript"}))
          : url;
        w = new Worker(src);
        w.onmessage = e => resolve(e.data);
        w.onerror = () => resolve("error");
      }
    } catch (e) { resolve("exc:" + e.name); }
    setTimeout(() => resolve("timeout"), 10000);
  });
}
async function runW(list) {
  for (const sc of list) {
    const m = await wOne(sc);
    if (typeof m === "string") { obs(`${sc.id}.load`, m); continue; }
    obs(`${sc.id}.load`, "load");
    obs(`${sc.id}.coi`, m.coi);
    obs(`${sc.id}.fx`, m.fx);
  }
  done();
}

// F: cross-origin cors fetch() from this page.
async function runF(list) {
  for (let i = 0; i < list.length; i += 12) {
    const batch = list.slice(i, i + 12);
    const vals = await Promise.all(batch.map(async sc => {
      const u = rurl(sc.tg, `cres.py?acao=${sc.acao}&corp=${sc.corp}&k=${token()}`);
      try { return (await within(fetch(u, {mode: "cors", credentials: sc.cred}), 15000, {type: "timeout"})).type; }
      catch (e) { return e.name === "TypeError" ? "error" : "exc:" + e.name; }
    }));
    batch.forEach((sc, j) => obs(`${sc.id}.r`, vals[j]));
  }
  done();
}
