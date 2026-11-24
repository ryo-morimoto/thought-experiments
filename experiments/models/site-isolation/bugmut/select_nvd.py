"""Apply the fixed filter (RESULTS.md section 1) to NVD keyword results.
usage: python3 -I select_nvd.py <dir with k1..k12.json>"""
import json, sys, re, hashlib, os
D = sys.argv[1]
KW = ["Cross-Origin-Opener-Policy","Cross-Origin-Embedder-Policy","Cross-Origin-Resource-Policy",
      "crossOriginIsolated","SharedArrayBuffer","site isolation","origin-keyed","document.domain",
      "opener","sandbox iframe","redirect origin","navigation origin"]
BROWSER = re.compile(r"Google Chrome|Mozilla Firefox|Firefox ESR|Thunderbird|Firefox|Safari|WebKit", re.I)
BOUND = re.compile(r"cross-origin|cross origin|cross-site|site isolation|same-origin|same origin|origin|isolation|sandbox|opener", re.I)
MEM = re.compile(r"use after free|use-after-free|heap buffer overflow|type confusion|out of bounds|memory corruption|integer overflow", re.I)
out = {}
for i, k in enumerate(KW, 1):
    d = json.load(open(os.path.join(D, "k%d.json" % i)))
    rows = []
    for v in d.get("vulnerabilities", []):
        c = v["cve"]; pub = c["published"][:10]
        desc = next(x["value"] for x in c["descriptions"] if x["lang"] == "en")
        if not ("2018-01-01" <= pub <= "2026-11-24"): continue
        if not BROWSER.search(desc): continue
        if not BOUND.search(desc): continue
        if MEM.search(desc) and not re.search(r"site isolation|COOP|COEP|CORP|opener policy|embedder policy", desc, re.I): continue
        refs = [r["url"] for r in c.get("references", [])]
        rows.append((hashlib.sha256(c["id"].encode()).hexdigest(), c["id"], pub, desc, refs))
    rows.sort()
    out[k] = rows
    print(i, k, d.get("totalResults"), "kept", len(rows), file=sys.stderr)
json.dump(out, open(os.path.join(D, "filtered.json"), "w"))
