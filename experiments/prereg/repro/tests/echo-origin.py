def main(request, response):
    origin = request.headers.get(b"origin")
    origin = origin.decode("utf-8") if origin is not None else "<no-origin-header>"
    headers = [(b"Content-Type", b"text/plain"),
               (b"Access-Control-Allow-Origin", request.headers.get(b"origin", b"*")),
               (b"Access-Control-Allow-Credentials", b"true"),
               (b"Cache-Control", b"no-store")]
    return 200, headers, origin
