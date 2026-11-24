"""A redirect hop of a generated scenario (redirect/RESULTS.md; copied unchanged into holdout/).

Query: coop, coep (unsafe-none sends no header), next (absolute URL, the
Location). Answers 302 with the COOP/COEP headers on the redirect response.
"""


def main(request, response):
    coop = request.GET.first(b"coop", b"unsafe-none")
    coep = request.GET.first(b"coep", b"unsafe-none")
    nxt = request.GET.first(b"next")
    headers = [(b"Location", nxt), (b"Cache-Control", b"no-store"),
               (b"Content-Type", b"text/plain")]
    if coop != b"unsafe-none":
        headers.append((b"Cross-Origin-Opener-Policy", coop))
    if coep != b"unsafe-none":
        headers.append((b"Cross-Origin-Embedder-Policy", coep))
    return 302, headers, b"redirect"
