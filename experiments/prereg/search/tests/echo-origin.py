def main(request, response):
    # Echo the Origin header (or a sentinel if absent) as text/plain, CORS-readable.
    o = request.headers.get(b"origin")
    body = o.decode("utf-8") if o is not None else "<no-origin-header>"
    origin = request.headers.get(b"origin", b"*")
    headers = [
        (b"Content-Type", b"text/plain"),
        (b"Access-Control-Allow-Origin", origin),
        (b"Access-Control-Allow-Credentials", b"true"),
        (b"Cache-Control", b"no-store"),
    ]
    return 200, headers, body
