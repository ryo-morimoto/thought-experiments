def main(request, response):
    o = request.headers.get(b"origin")
    o = o.decode("utf-8") if o is not None else "<no-origin-header>"
    body = ("<!doctype html><script>parent.postMessage({origin:" + repr(o) + "},'*');</script>").encode()
    return 200, [(b"Content-Type", b"text/html"), (b"Cache-Control", b"no-store")], body
