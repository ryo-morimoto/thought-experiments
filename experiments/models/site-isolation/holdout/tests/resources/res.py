"""No-cors fetch target of the generated scenarios: no CORP, no CORS headers (gen/, copied into holdout/)."""


def main(request, response):
    return 200, [(b"Content-Type", b"text/plain"), (b"Cache-Control", b"no-store")], b"ok"
