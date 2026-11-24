"""Fetch target of gen2 (gen2/RESULTS.md): text, optional CORP (query corp), no CORS headers."""


def main(request, response):
    headers = [(b"Content-Type", b"text/plain"), (b"Cache-Control", b"no-store")]
    corp = request.GET.first(b"corp", b"none")
    if corp != b"none":
        headers.append((b"Cross-Origin-Resource-Policy", corp))
    return 200, headers, b"ok"
