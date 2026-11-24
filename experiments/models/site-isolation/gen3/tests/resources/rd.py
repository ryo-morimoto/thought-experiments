"""gen3 redirect hop (gen3/RESULTS.md): 307 to query "to", ACAO *, optional Referrer-Policy (query rp)."""


def main(request, response):
    headers = [(b"Location", request.GET.first(b"to")), (b"Access-Control-Allow-Origin", b"*"),
               (b"Cache-Control", b"no-store")]
    rp = request.GET.first(b"rp", b"")
    if rp:
        headers.append((b"Referrer-Policy", rp))
    return 307, headers, b""
