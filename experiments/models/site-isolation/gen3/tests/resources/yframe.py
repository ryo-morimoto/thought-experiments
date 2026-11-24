"""gen3 Y frame: sets top.location.href to nav (no user activation); sends "noexc" or
"threw:<name>" through the dispatcher (query uuid)."""

BODY = b"""<!doctype html><meta charset=utf-8>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<body><script>
const p = new URLSearchParams(location.search);
(async () => {
  try { top.location.href = p.get("nav"); await send(p.get("uuid"), "noexc"); }
  catch (e) { await send(p.get("uuid"), "threw:" + e.name); }
})();
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")], BODY
