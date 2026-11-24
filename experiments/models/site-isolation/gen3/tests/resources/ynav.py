"""gen3 Y navigation target: sends "nav" through the dispatcher (query uuid)."""

BODY = b"""<!doctype html><meta charset=utf-8>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<body><script>
send(new URLSearchParams(location.search).get("uuid"), "nav");
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")], BODY
