"""Top-level page of a gen2 Origin-Agent-Cluster scenario (gen2/RESULTS.md).

Opened with noopener, so it starts a fresh browsing context group. Query: uuid,
h0 (its Origin-Agent-Cluster value: absent | ?0 | ?1), h1 and h2 (for child 1
and child 2, both on www1. of this host, same scheme and port), coi (1: COOP
same-origin + COEP require-corp here; the children send COEP require-corp and
CORP cross-origin). Child 2 is inserted after child 1 has loaded. The page sends
{g0, g1, g2, dd} to uuid via the WPT dispatcher: the three originAgentCluster
getters, and dd = TRUE if, after both this page and child 1 set document.domain
to this host, this page can read child 1's document.
"""

BODY = b"""<!doctype html><meta charset=utf-8>
<script src="/common/utils.js"></script>
<script src="/common/dispatcher/dispatcher.js"></script>
<body><script>
const p = new URLSearchParams(location.search);
const B = v => v === true ? "TRUE" : v === false ? "FALSE" : "raw:" + v;
function ask(w, msg) {
  return new Promise(resolve => {
    const h = e => { if (e.source === w) { removeEventListener("message", h); resolve(e.data); } };
    addEventListener("message", h);
    w.postMessage(msg, "*");
    setTimeout(() => resolve("timeout"), 10000);
  });
}
function child(h) {
  return new Promise(resolve => {
    const f = document.createElement("iframe");
    f.onload = () => resolve(f);
    f.src = location.protocol + "//www1." + location.host + "/gen2-si/resources/oac-child.py?coi=" +
            p.get("coi") + "&h=" + encodeURIComponent(h);
    document.body.appendChild(f);
  });
}
(async () => {
  const out = {};
  try {
    const f1 = await child(p.get("h1"));
    const f2 = await child(p.get("h2"));
    out.g0 = B(self.originAgentCluster);
    out.g1 = B(await ask(f1.contentWindow, {cmd: "get"}));
    out.g2 = B(await ask(f2.contentWindow, {cmd: "get"}));
    try { document.domain = location.hostname; } catch (e) {}
    await ask(f1.contentWindow, {cmd: "dd", value: location.hostname});
    try { f1.contentWindow.document.body; out.dd = "TRUE"; }
    catch (e) { out.dd = e.name === "SecurityError" ? "FALSE" : "exc:" + e.name; }
  } catch (e) { out.error = "exc:" + e.name; }
  await send(p.get("uuid"), JSON.stringify(out));
  setTimeout(() => window.close(), 200);
})();
</script>
"""


def main(request, response):
    headers = [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")]
    h0 = request.GET.first(b"h0", b"absent")
    if h0 != b"absent":
        headers.append((b"Origin-Agent-Cluster", h0))
    if request.GET.first(b"coi", b"0") == b"1":
        headers.append((b"Cross-Origin-Opener-Policy", b"same-origin"))
        headers.append((b"Cross-Origin-Embedder-Policy", b"require-corp"))
    return 200, headers, BODY
