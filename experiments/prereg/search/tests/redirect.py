def main(request, response):
    # Generic redirect hop for the Origin-header search. Params:
    #   status:   301|302|303|307|308 (default 307)
    #   location: URL-encoded next hop (already a full absolute URL)
    status = request.GET.first(b"status", b"307")
    try:
        code = int(status)
    except ValueError:
        code = 307
    loc = request.GET.first(b"location")
    origin = request.headers.get(b"origin", b"*")
    headers = [
        (b"Location", loc),
        (b"Cache-Control", b"no-store"),
        (b"Access-Control-Allow-Origin", origin),
        (b"Access-Control-Allow-Credentials", b"true"),
    ]
    return code, headers, b""
