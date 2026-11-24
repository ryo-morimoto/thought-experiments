"""gen3 W worker script, with Cross-Origin-Embedder-Policy from query coep (none for
unsafe-none). Reports crossOriginIsolated and a no-cors fetch() of query fx. The same
code is in g3.js (WSRC) for blob: workers."""
import json

WSRC = """
async function g3run() {
  let fx;
  try { fx = (await fetch(FX, {mode: "no-cors"})).type; } catch (e) { fx = "error"; }
  return {coi: String(self.crossOriginIsolated).toUpperCase(), fx};
}
if (typeof SharedWorkerGlobalScope !== "undefined" && self instanceof SharedWorkerGlobalScope)
  onconnect = e => { const p = e.ports[0]; g3run().then(m => p.postMessage(m)); };
else g3run().then(m => postMessage(m));
"""


def main(request, response):
    coep = request.GET.first(b"coep", b"unsafe-none")
    fx = request.GET.first(b"fx", b"").decode("ascii", "replace")
    headers = [(b"Content-Type", b"text/javascript"), (b"Cache-Control", b"no-store")]
    if coep in (b"require-corp", b"credentialless"):
        headers.append((b"Cross-Origin-Embedder-Policy", coep))
    return 200, headers, ("const FX = %s;" % json.dumps(fx) + WSRC).encode("utf-8")
