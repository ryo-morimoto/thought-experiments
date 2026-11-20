def main(request, response):
    loc = request.GET.first(b"location")
    headers = [(b"Location", loc), (b"Cache-Control", b"no-store"),
               (b"Access-Control-Allow-Origin", request.headers.get(b"origin", b"*")),
               (b"Access-Control-Allow-Credentials", b"true")]
    return 307, headers, b""
