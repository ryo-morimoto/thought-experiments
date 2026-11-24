"""gen3 N target (Origin-Agent-Cluster: ?0): posts whether its Window has the expando g3x
that the creator put on the initial about:blank's Window (TRUE: the Window was reused)."""

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
const t = window.parent !== window ? window.parent : window.opener;
t.postMessage({g3n: 1, reuse: typeof window.g3x === "string" ? "TRUE" : "FALSE"}, "*");
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store"),
                 (b"Origin-Agent-Cluster", b"?0")], BODY
