"""Generate nested-frame scenarios along structural axes (gen/RESULTS.md).

usage: python3 -I gen.py <out dir>      (writes <out>/tests/top-*.html{,.headers}
                                          and <out>/scenarios.tsv)
Axes. Top (level 0): scheme {https, http} x COEP {unsafe-none, require-corp,
credentialless} x COOP {unsafe-none, same-origin} = 12 top configurations.
Each child level: scheme {https, http} x host relation to its parent
{same host, same site other host, other site} x COEP (3) x CORP of its response
{none, same-origin, cross-origin} = 54. Depth 0..2. The full space is
12 + 12*54 + 12*54*54 = 35652 scenarios. Run: depth 0 and 1 exhaustively
(12 + 648); depth 2 sampled with seed SEED: for each top configuration and each
child configuration, K2 grandchild configurations drawn without replacement
(12*54*K2). The fetch target is https, the other site's bare host, no CORP.
Hosts: a = web-platform.test, a1/a2 = www1./www2., b/b1/b2 the same under
not-web-platform.test. "Same host" with a different scheme is a different
origin (schemelessly same site); the relation axis is on hosts.
"""
import itertools
import os
import random
import sys

SEED, K2 = 20261124, 2
SCHEMES = ["https", "http"]
COEPS = ["unsafe-none", "require-corp", "credentialless"]
COOPS = ["unsafe-none", "same-origin"]
RELS = ["same-host", "same-site", "cross-site"]
CORPS = ["none", "same-origin", "cross-origin"]
AB = {"unsafe-none": "un", "require-corp": "rc", "credentialless": "cl", "same-origin": "so",
      "cross-origin": "xo", "none": "no", "same-host": "sh", "same-site": "ss", "cross-site": "xs"}
TOPS = list(itertools.product(SCHEMES, COEPS, COOPS))
CHILD = list(itertools.product(SCHEMES, RELS, COEPS, CORPS))


def rel_host(parent, rel):
    site, sub = parent[0], parent[1:]
    if rel == "same-host":
        return parent
    if rel == "same-site":
        return site + next(s for s in ["", "1", "2"] if s != sub)
    return ("b" if site == "a" else "a")


def other_site(h):
    return "b" if h[0] == "a" else "a"


def top_id(t):
    return "T-%s-%s-%s" % (t[0], AB[t[1]], AB[t[2]])


def levels(chain):
    """chain: list of child configs; returns list of dicts with hosts resolved."""
    out, parent = [], "a"
    for (s, rel, coep, corp) in chain:
        h = rel_host(parent, rel)
        out.append({"s": s, "rel": rel, "h": h, "coep": coep, "corp": corp})
        parent = h
    return out


def main(out):
    rng = random.Random(SEED)
    os.makedirs(os.path.join(out, "tests"), exist_ok=True)
    rows = []
    for ti, t in enumerate(TOPS):
        tid = top_id(t)
        scen = []
        for ci, c in enumerate(CHILD):
            scen.append(("d1-%d-%d" % (ti, ci), [c]))
        for ci, c in enumerate(CHILD):
            for gi in sorted(rng.sample(range(len(CHILD)), K2)):
                scen.append(("d2-%d-%d-%d" % (ti, ci, gi), [c, CHILD[gi]]))
        rows.append((tid, 0, t, []))
        js = []
        for sid, chain in scen:
            lv = levels(chain)
            rows.append((sid, len(chain), t, lv))
            js.append('{id:"%s",t:"%s",lv:[%s]}' % (sid, other_site(lv[-1]["h"]), ",".join(
                '{s:"%s",h:"%s",coep:"%s",corp:"%s"}' % (x["s"], x["h"], x["coep"], x["corp"])
                for x in lv)))
        name = "top-%s-%s-%s%s.sub.html" % (t[0], AB[t[1]], AB[t[2]], ".https" if t[0] == "https" else "")
        with open(os.path.join(out, "tests", name), "w", encoding="utf-8") as f:
            f.write("""<!doctype html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>generated scenarios, top %s</title>
<script src=/resources/testharness.js></script>
<script src=/resources/testharnessreport.js></script>
<script src=resources/gobs.js></script>
<body>
<script>
const HOSTS = {a: "{{host}}", a1: "{{hosts[][www1]}}", a2: "{{hosts[][www2]}}",
               b: "{{hosts[alt][]}}", b1: "{{hosts[alt][www1]}}", b2: "{{hosts[alt][www2]}}"};
const PORTS = {http: {{ports[http][0]}}, https: {{ports[https][0]}}};
const TOP_ID = "%s", TOP_TGT = "b";
const SCEN = [
%s
];
runGen();
</script>
""" % (tid, tid, ",\n".join(js)))
        hdr = []
        if t[1] != "unsafe-none":
            hdr.append("Cross-Origin-Embedder-Policy: " + t[1])
        if t[2] != "unsafe-none":
            hdr.append("Cross-Origin-Opener-Policy: " + t[2])
        if hdr:
            with open(os.path.join(out, "tests", name + ".headers"), "w", encoding="utf-8") as f:
                f.write("\n".join(hdr) + "\n")
    with open(os.path.join(out, "scenarios.tsv"), "w", encoding="utf-8") as f:
        f.write("sid\tdepth\ttop_scheme\ttop_coep\ttop_coop\tl1\tl2\n")
        for sid, d, t, lv in rows:
            cells = ["%s/%s/%s/%s/%s" % (x["s"], x["rel"], x["h"], x["coep"], x["corp"]) for x in lv]
            cells += [""] * (2 - len(cells))
            f.write("\t".join([sid, str(d), t[0], t[1], t[2]] + cells) + "\n")
    n = {d: sum(1 for r in rows if r[1] == d) for d in (0, 1, 2)}
    print("generated", n, "of full space", {0: 12, 1: 12 * 54, 2: 12 * 54 * 54})


if __name__ == "__main__":
    main(sys.argv[1])
