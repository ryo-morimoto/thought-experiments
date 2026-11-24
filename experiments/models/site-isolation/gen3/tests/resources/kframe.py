"""gen3 K frame: CSP img-src 'self' [ex]; loads <img src=img> and posts
{g3k, sid, img: load|error, bu: [blockedURI of each violation]} to its parent."""
import re

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
const p = new URLSearchParams(location.search);
const bu = [];
document.addEventListener("securitypolicyviolation", e => bu.push(e.blockedURI), true);
const fin = v => setTimeout(() => parent.postMessage({g3k: 1, sid: p.get("sid"), img: v, bu}, "*"), 500);
const img = document.createElement("img");
img.onload = () => fin("load");
img.onerror = () => fin("error");
document.body.appendChild(img);
img.src = p.get("img");
</script>
"""


def main(request, response):
    ex = request.GET.first(b"ex", b"")
    if not re.fullmatch(rb"[A-Za-z0-9.:/-]*", ex):
        ex = b""
    csp = b"img-src 'self'" + (b" " + ex if ex else b"")
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store"),
                 (b"Content-Security-Policy", csp)], BODY
