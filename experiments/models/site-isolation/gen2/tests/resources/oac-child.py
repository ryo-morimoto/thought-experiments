"""Child frame of a gen2 Origin-Agent-Cluster scenario (see oac-top.py).

Query: h (Origin-Agent-Cluster value or absent), coi (1: COEP require-corp and
CORP cross-origin). Answers {cmd: "get"} with its originAgentCluster getter and
{cmd: "dd", value} by setting document.domain to value.
"""

BODY = b"""<!doctype html><meta charset=utf-8><script>
addEventListener("message", e => {
  if (e.data.cmd === "get") e.source.postMessage(self.originAgentCluster, "*");
  if (e.data.cmd === "dd") {
    let r;
    try { document.domain = e.data.value; r = document.domain; } catch (x) { r = "exc:" + x.name; }
    e.source.postMessage(r, "*");
  }
});
</script>
"""


def main(request, response):
    headers = [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")]
    h = request.GET.first(b"h", b"absent")
    if h != b"absent":
        headers.append((b"Origin-Agent-Cluster", h))
    if request.GET.first(b"coi", b"0") == b"1":
        headers.append((b"Cross-Origin-Embedder-Policy", b"require-corp"))
        headers.append((b"Cross-Origin-Resource-Policy", b"cross-origin"))
    return 200, headers, BODY
