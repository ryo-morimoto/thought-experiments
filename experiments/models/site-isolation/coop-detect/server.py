# Two origins: opener on 127.0.0.1:P1, popup on localhost:P2 (both secure contexts).
# The popup reports whether window.opener is null; reports are printed to stdout.
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
        if u.path == "/opener":
            coop = q.get("coop", [""])[0]
            self.send(f"<script>window.open('http://localhost:{P2}/popup?coop={coop}')</script>")
        elif u.path == "/popup":
            coop = q.get("coop", [""])[0]
            self.send("<script>fetch('/report?coop=" + coop +
                      "&opener=' + (window.opener === null ? 'null' : 'present'))</script>",
                      coop or None)
        elif u.path == "/report":
            print("REPORT", q["coop"][0] if "coop" in q else "", q["opener"][0], flush=True)
            self.send("ok")
        else:
            self.send_response(404); self.end_headers()

for p in (P1, P2):
    threading.Thread(target=ThreadingHTTPServer(("127.0.0.1", p), H).serve_forever, daemon=True).start()
threading.Event().wait()
