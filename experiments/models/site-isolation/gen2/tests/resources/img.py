"""Image target of gen2 (gen2/RESULTS.md): a 1x1 PNG, optional CORP (query corp)."""
import base64

PNG = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")


def main(request, response):
    headers = [(b"Content-Type", b"image/png"), (b"Cache-Control", b"no-store")]
    corp = request.GET.first(b"corp", b"none")
    if corp != b"none":
        headers.append((b"Cross-Origin-Resource-Policy", corp))
    return 200, headers, PNG
