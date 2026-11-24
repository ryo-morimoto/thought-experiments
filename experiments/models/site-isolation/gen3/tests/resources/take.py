"""gen3: return what echo.py stored under query "key" ({} if nothing)."""


def main(request, response):
    v = request.server.stash.take(request.GET.first(b"key"), "/gen3-si/")
    return 200, [(b"Content-Type", b"application/json"), (b"Cache-Control", b"no-store")], v or "{}"
