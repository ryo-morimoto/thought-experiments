def main(request, response):
    headers = [(b"Content-Type", b"text/html"),
               (b"Set-Cookie", b"ss_strict=1; SameSite=Strict; Path=/; Secure"),
               (b"Set-Cookie", b"ss_lax=1; SameSite=Lax; Path=/; Secure"),
               (b"Set-Cookie", b"ss_none=1; SameSite=None; Path=/; Secure"),
               (b"Cache-Control", b"no-store")]
    body = b"<!doctype html><script>(window.opener||parent).postMessage('cookies-set','*');</script>set"
    return 200, headers, body
