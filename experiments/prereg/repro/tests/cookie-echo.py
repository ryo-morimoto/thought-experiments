def main(request, response):
    c = request.headers.get(b"cookie")
    c = c.decode("utf-8") if c is not None else "<none>"
    headers = [(b"Content-Type", b"text/html"), (b"Cache-Control", b"no-store")]
    body = ("<!doctype html><script>parent.postMessage(" +
            repr(c) + ",'*');</script>" + c).encode("utf-8")
    return 200, headers, body
