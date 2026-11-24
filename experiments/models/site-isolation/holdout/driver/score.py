"""Summarize TLC outputs of the holdout (counts, out rows, kills vs K_prev).

usage: python3 -I score.py <dir with tlc-*.out and prev-*.out>
Prints, per cfg: counts per browser, out-of-model rows grouped by
(browser, kind, observed, allowed), the kill set per browser, the mutants
killed now and not in K_prev (union of gen/, gen2/, redirect/ for that
browser and COI set), and the mutants equivalent on the rows.
"""
import collections
import glob
import os
import re
import sys

d = sys.argv[1]


def sset(s):
    return {v.strip().strip('"') for v in s.strip("{}").split(",") if v.strip()}


prev = collections.defaultdict(set)     # (coi, browser) -> mutants
for p in glob.glob(os.path.join(d, "prev-*.out")):
    text = re.sub(r"\s+", " ", open(p, encoding="utf-8").read())
    for pipe, cfg, b, ms in re.findall(r'<< ?"prevkill", "(\w+)", "(\w+)", "(\w+)", \{([^}]*)\} ?>>', text):
        prev[(cfg, b)] |= sset(ms)
for p in sorted(glob.glob(os.path.join(d, "tlc-HoldAllowed-*.out"))):
    text = re.sub(r"\s+", " ", open(p, encoding="utf-8").read())
    cfg = re.search(r'<< ?"cfg", "([^"]+)"', text).group(1)
    coi = "concrete" if cfg.endswith("concrete") else "both"
    print("==", cfg, re.search(r'<< ?"cfg", [^>]*>>', text).group(0))
    for b, n, ins, out in re.findall(r'<< ?"counts", "[^"]+", "(\w+)", (\d+), (\d+), (\d+) ?>>', text):
        print("  counts", b, "observed", n, "inside", ins, "out", out)
    groups = collections.Counter()
    for b, rid, ob, al in re.findall(r'<< ?"out", "[^"]+", "(\w+)", "([^"]+)", (\{[^}]*\}), (\{[^}]*\}) ?>>', text):
        groups[(b, rid.rsplit(".", 1)[-1], ob, al)] += 1
    for k, v in sorted(groups.items()):
        print("  out", v, k)
    kills = collections.defaultdict(dict)
    for b, m, n in re.findall(r'<< ?"kill", "[^"]+", "(\w+)", "([^"]+)", (\d+) ?>>', text):
        if int(n):
            kills[b][m] = int(n)
    for b in sorted(kills):
        new = sorted(set(kills[b]) - prev[(coi, b)])
        print("  killed", b, len(kills[b]), "| not in K_prev:", new)
    eq = re.search(r'<< ?"equivalent", "[^"]+", \{([^}]*)\} ?>>', text)
    print("  equivalent-on-rows", len(sset(eq.group(1))) if eq else "?")
ALL = set()
for p in glob.glob(os.path.join(d, "tlc-HoldAllowed-*.out")):
    ALL |= set(re.findall(r'"kill", "[^"]+", "\w+", "([^"]+)"', re.sub(r"\s+", " ", open(p, encoding="utf-8").read())))
for k in sorted(prev):
    print("K_prev", k, len(prev[k]), "| not in K_prev:", sorted(ALL - prev[k]) if ALL else "")
