"""gen3 no-cors fetch target: text, no CORP, no CORS headers."""


def main(request, response):
    return 200, [(b"Content-Type", b"text/plain"), (b"Cache-Control", b"no-store")], b"ok"
