"""A frame of a generated scenario (gen/RESULTS.md).

Query: sid, lvl (1 or 2), coep (unsafe-none | require-corp | credentialless),
corp (none | same-origin | cross-origin), next (URL of the grandchild, or
empty), tgt (URL of the no-cors fetch target, given only to the deepest
frame). unsafe-none and none send no header. The page posts one message to
top: its crossOriginIsolated and isSecureContext, and the fetch results if it
is the deepest frame; then it creates the grandchild frame, if any.
"""

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
async function fo(url, init) {
  try { const r = await fetch(url, init); return r.type; }
  catch (e) { return e.name === "TypeError" ? "error" : "exc:" + e.name; }
}
(async () => {
  const p = new URLSearchParams(location.search);
  const msg = {gen: 1, sid: p.get("sid"), lvl: p.get("lvl"),
               coi: String(self.crossOriginIsolated), sec: String(self.isSecureContext)};
  const tgt = p.get("tgt");
  if (tgt) {
    msg.fetch = await fo(tgt + "&c=0", {mode: "no-cors"});
    msg.fetchc = await fo(tgt + "&c=1", {mode: "no-cors", credentials: "include"});
  }
  top.postMessage(msg, "*");
  const nxt = p.get("next");
  if (nxt) {
    const f = document.createElement("iframe");
    f.src = nxt;
    document.body.appendChild(f);
  }
})();
</script>
"""


def main(request, response):
    coep = request.GET.first(b"coep", b"unsafe-none")
    corp = request.GET.first(b"corp", b"none")
    headers = [(b"Content-Type", b"text/html; charset=utf-8"),
               (b"Cache-Control", b"no-store")]
    if coep != b"unsafe-none":
        headers.append((b"Cross-Origin-Embedder-Policy", coep))
    if corp != b"none":
        headers.append((b"Cross-Origin-Resource-Policy", corp))
    return 200, headers, BODY
