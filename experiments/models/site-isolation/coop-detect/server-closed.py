# Opener-side check (experiments/2026-11-21-toe-optional-feature.md, stage C):
# the opener on 127.0.0.1:P1 sends COOP (or not) and opens a cross-origin
# popup on localhost:P2 without COOP. After 2 s it reports its handle's
# `closed`. HTML: with "same-origin", a popup that does not match "will
# appear closed to the opener".
import sys, threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

P1, P2 = int(sys.argv[1]), int(sys.argv[2])

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, body, coop=None):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        if coop:
            self.send_header("Cross-Origin-Opener-Policy", coop)
        self.end_headers()
        self.wfile.write(body.encode())
    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        coop = q.get("coop", [""])[0]
        if u.path == "/opener":
            self.send(f"<script>const w = window.open('http://localhost:{P2}/popup');"
                      f"setTimeout(() => fetch('/report?coop={coop}&closed=' + w.closed), 2000)</script>",
                      coop or None)
        elif u.path == "/popup":
            self.send("popup")
        elif u.path == "/report":
            print("REPORT", coop, q["closed"][0], flush=True)
            self.send("ok")
        else:
            self.send_response(404); self.end_headers()

for p in (P1, P2):
    threading.Thread(target=ThreadingHTTPServer(("127.0.0.1", p), H).serve_forever, daemon=True).start()
threading.Event().wait()
