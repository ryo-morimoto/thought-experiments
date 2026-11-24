"""gen3 cors fetch target. Query acao: none | * | origin (echo the request Origin) |
origin-acac (echo, plus Access-Control-Allow-Credentials: true); corp: none or a CORP value."""


def main(request, response):
    headers = [(b"Content-Type", b"text/plain"), (b"Cache-Control", b"no-store")]
    acao = request.GET.first(b"acao", b"none")
    if acao == b"*":
        headers.append((b"Access-Control-Allow-Origin", b"*"))
    elif acao in (b"origin", b"origin-acac"):
        headers.append((b"Access-Control-Allow-Origin", request.headers.get(b"Origin", b"null")))
        if acao == b"origin-acac":
            headers.append((b"Access-Control-Allow-Credentials", b"true"))
    corp = request.GET.first(b"corp", b"none")
    if corp != b"none":
        headers.append((b"Cross-Origin-Resource-Policy", corp))
    return 200, headers, b"ok"
