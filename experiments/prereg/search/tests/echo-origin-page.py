def main(request, response):
    # For navigation/iframe modes: a page that posts the received Origin header to its parent.
    o = request.headers.get(b"origin")
    o = o.decode("utf-8") if o is not None else "<no-origin-header>"
    rid = request.GET.first(b"rid", b"").decode("utf-8")
    body = ("<!doctype html><script>parent.postMessage({rid:" + repr(rid) +
            ",origin:" + repr(o) + "},'*');</script>").encode()
    return 200, [(b"Content-Type", b"text/html"), (b"Cache-Control", b"no-store")], body
