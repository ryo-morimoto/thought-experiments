"""Child frame of the gen2 sandbox family (gen2/RESULTS.md).

Query: sid, coep (unsafe-none | require-corp), corp (none | same-origin |
cross-origin), fx (https no-cors target, other site), fh (http target, other
site), ih (image at an http URL on the https port, CORP cross-origin). The page
posts {g2alive} to its parent first, then: crossOriginIsolated, isSecureContext, whether self.origin
is opaque, a no-cors fetch to its own URL's origin (no CORP), and the results
for fx, fh and ih. unsafe-none and none send no header.
"""

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
async function fo(url, init) {
  try { const r = await fetch(url, init); return r.type; }
  catch (e) { return e.name === "TypeError" ? "error" : "exc:" + e.name; }
}
function img(url) {
  return Promise.race([new Promise(res => {
    const el = document.createElement("img");
    el.onload = () => res("load"); el.onerror = () => res("error");
    el.src = url; document.body.appendChild(el);
  }), new Promise(res => setTimeout(() => res("timeout"), 8000))]);
}
(async () => {
  const p = new URLSearchParams(location.search);
  const sid = p.get("sid");
  parent.postMessage({g2alive: 1, sid}, "*");
  const m = {g2: 1, sid, coi: String(self.crossOriginIsolated).toUpperCase(),
             sec: String(self.isSecureContext).toUpperCase(),
             orig: self.origin === "null" ? "opaque" : "tuple"};
  m.fself = await fo(new URL("res.py?k=self&sid=" + sid, location.href).href, {mode: "no-cors"});
  m.fx = await fo(p.get("fx"), {mode: "no-cors"});
  m.fhttp = await fo(p.get("fh"), {mode: "no-cors"});
  m.ihttp = await img(p.get("ih"));
  parent.postMessage(m, "*");
})();
</script>
"""


def main(request, response):
    coep = request.GET.first(b"coep", b"unsafe-none")
    corp = request.GET.first(b"corp", b"none")
    headers = [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")]
    if coep != b"unsafe-none":
        headers.append((b"Cross-Origin-Embedder-Policy", coep))
    if corp != b"none":
        headers.append((b"Cross-Origin-Resource-Policy", corp))
    return 200, headers, BODY
