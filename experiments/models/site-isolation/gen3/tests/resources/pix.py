"""gen3 image target: a 1x1 GIF, no CORP, no-store."""
import base64

GIF = base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")


def main(request, response):
    return 200, [(b"Content-Type", b"image/gif"), (b"Cache-Control", b"no-store")], GIF
