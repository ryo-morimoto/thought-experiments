"""gen3 D/N top (a noopener popup, Origin-Agent-Cluster: ?0). Runs one scenario and sends
its values as JSON through the dispatcher (query uuid), then closes itself.
D: sets document.domain (query dom) if set is p or both, embeds cu (sandbox
   "allow-scripts allow-same-origin" if csb=yes), then tries child.document
   (pc) and asks the child to try parent.document (cp).
N: sets document.domain before (dd=before) or after (dd=after) creating an
   about:blank (iframe without src, iframe with src at insertion, or
   window.open(cu)), puts an expando g3x on its Window, navigates it to cu
   and gets whether the new document sees g3x (reuse)."""

BODY = b"""<!doctype html><meta charset=utf-8>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<body><script>
const p = new URLSearchParams(location.search);
const msg = (pred, ms) => new Promise(res => {
  const h = e => { if (e.data && pred(e.data)) { removeEventListener("message", h); res(e.data); } };
  addEventListener("message", h);
  setTimeout(() => res(null), ms);
});
const nm = e => e.name === "SecurityError" ? "denied" : "exc:" + e.name;
(async () => {
  const out = {};
  try {
    if (p.get("fam") === "D") {
      const set = p.get("set");
      if (set === "p" || set === "both") {
        try { document.domain = p.get("dom"); out.pset = "ok"; } catch (e) { out.pset = "threw"; }
      }
      const f = document.createElement("iframe");
      if (p.get("csb") === "yes") f.sandbox = "allow-scripts allow-same-origin";
      const ready = msg(m => m.g3d === "ready", 10000);
      f.src = p.get("cu");
      document.body.appendChild(f);
      const r = await ready;
      out.cset = r ? r.cset : "noreport";
      try { void f.contentWindow.document.title; out.pc = "ok"; } catch (e) { out.pc = nm(e); }
      const cp = msg(m => m.g3d === "cp", 5000);
      f.contentWindow.postMessage("go", "*");
      const c = await cp;
      out.cp = c ? c.cp : "noreport";
    } else {
      const dd = p.get("dd"), how = p.get("how"), cu = p.get("cu"), dom = p.get("dom");
      if (dd === "before") document.domain = dom;
      const got = msg(m => m.g3n, 10000);
      let w = null, f = null;
      if (how === "popup") {
        w = window.open(cu);
        try { w.g3x = "x"; } catch (e) { out.setx = nm(e); }
      } else {
        f = document.createElement("iframe");
        if (how === "ifr-insert") f.src = cu;
        document.body.appendChild(f);
        try { f.contentWindow.g3x = "x"; } catch (e) { out.setx = nm(e); }
      }
      if (dd === "after") document.domain = dom;
      if (how === "ifr-after") f.src = cu;
      const r = await got;
      out.reuse = r ? r.reuse : "noreport";
      if (w) w.close();
    }
  } catch (e) { out.error = "exc:" + e.name; }
  await send(p.get("uuid"), JSON.stringify(out));
  window.close();
})();
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store"),
                 (b"Origin-Agent-Cluster", b"?0")], BODY
