"""gen3 Y top (a popup): embeds the frame fu, with a sandbox attribute sb if sbon=1."""

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
const p = new URLSearchParams(location.search);
const f = document.createElement("iframe");
if (p.get("sbon") === "1") f.sandbox = p.get("sb");
f.src = p.get("fu");
document.body.appendChild(f);
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")], BODY
