"""gen3 X frame (gen3/RESULTS.md): sets document.domain to its own host, calls window.open(pu),
posts {g3x, sid, fdd, opened} to its parent, closes the popup after 6 s."""

BODY = b"""<!doctype html><meta charset=utf-8><body><script>
const p = new URLSearchParams(location.search);
let fdd;
try { document.domain = location.hostname; fdd = "ok"; }
catch (e) { fdd = e.name === "SecurityError" ? "threw" : "exc:" + e.name; }
let w = null, opened;
try { w = window.open(p.get("pu")); opened = w ? "TRUE" : "FALSE"; } catch (e) { opened = "exc:" + e.name; }
parent.postMessage({g3x: 1, sid: p.get("sid"), fdd, opened}, "*");
setTimeout(() => { try { if (w) w.close(); } catch (e) {} }, 6000);
</script>
"""


def main(request, response):
    return 200, [(b"Content-Type", b"text/html; charset=utf-8"), (b"Cache-Control", b"no-store")], BODY
