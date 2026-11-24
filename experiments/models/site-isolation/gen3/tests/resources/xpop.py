"""gen3 X popup: reports whether its origin is opaque and whether document.domain (own host)
throws, through the dispatcher (query uuid), then tries to close itself."""

BODY = b"""<!doctype html><meta charset=utf-8>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<body><script>
(async () => {
  const u = new URLSearchParams(location.search).get("uuid");
  let pdd;
  try { document.domain = location.hostname; pdd = "ok"; }
  catch (e) { pdd = e.name === "SecurityError" ? "threw" : "exc:" + e.name; }
  await send(u, JSON.stringify({porig: self.origin === "null" ? "opaque" : "tuple", pdd}));
  window.close();
})();
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")], BODY
