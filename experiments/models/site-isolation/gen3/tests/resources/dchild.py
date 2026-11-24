"""gen3 D child (Origin-Agent-Cluster: ?0): sets document.domain (query dom) if set is c or
both, posts {g3d: ready, cset}; on "go" tries parent.document and posts {g3d: cp, cp}."""

BODY = b"""<!doctype html><meta charset=utf-8><title>c</title><body><script>
const p = new URLSearchParams(location.search);
let cset = "skip";
const set = p.get("set");
if (set === "c" || set === "both") {
  try { document.domain = p.get("dom"); cset = "ok"; }
  catch (e) { cset = e.name === "SecurityError" ? "threw" : "exc:" + e.name; }
}
addEventListener("message", e => {
  if (e.data !== "go") return;
  let cp;
  try { void parent.document.title; cp = "ok"; }
  catch (er) { cp = er.name === "SecurityError" ? "denied" : "exc:" + er.name; }
  parent.postMessage({g3d: "cp", cp}, "*");
});
parent.postMessage({g3d: "ready", cset}, "*");
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store"),
                 (b"Origin-Agent-Cluster", b"?0")], BODY
