"""gen3 last URL of a redirect chain (gen3/RESULTS.md): stores the Origin and Referer request
headers under query "key" (a UUID) in the stash, path /gen3-si/; take.py returns them."""
import json


def main(request, response):
    o = request.headers.get(b"Origin")
    r = request.headers.get(b"Referer")
    d = {"origin": None if o is None else o.decode("latin-1"),
         "referer": None if r is None else r.decode("latin-1"),
         "method": request.method, "recorded": True}
    try:
        request.server.stash.put(request.GET.first(b"key"), json.dumps(d), "/gen3-si/")
    except Exception:
        pass
    return 200, [(b"Access-Control-Allow-Origin", b"*"), (b"Cache-Control", b"no-store"),
                 (b"Content-Type", b"text/plain")], b"ok"
