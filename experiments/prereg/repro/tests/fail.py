# Produces a response that becomes an error document in the browser:
# we drop the connection via an oversized Content-Length mismatch is unreliable,
# so instead return a 5xx-like via resetting is not portable. Use 204? not error.
# Reliable committed error: send a bogus Content-Length larger than body -> truncated/error.
def main(request, response):
    response.headers.set(b"Content-Type", b"text/html")
    response.headers.set(b"Content-Length", b"1000")
    response.headers.set(b"Cache-Control", b"no-store")
    response.content = b"x"  # fewer bytes than declared -> net error in many browsers
    return response
