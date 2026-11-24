"""Per-family kill comparison (prereg rule 4, R3 second part).

usage: python3 -I famkill.py <score dir>
N vs gen/ (prev-HoldPrev-*), R vs redirect/ (prev-HoldPrevRedir-*), per COI set
and browser: killed now and not by the previous family, and the reverse.
"""
import os
import re
import sys

d = sys.argv[1]


def norm(p):
    return re.sub(r"\s+", " ", open(os.path.join(d, p), encoding="utf-8").read())


def prev(p, b):
    m = re.search(r'<< ?"prevkill", "\w+", "\w+", "%s", \{([^}]*)\} ?>>' % b, norm(p))
    return {v.strip().strip('"') for v in m.group(1).split(",") if v.strip()}


def now(p, b):
    return {m for m, n in re.findall(r'<< ?"kill", "[^"]+", "%s", "([^"]+)", (\d+) ?>>' % b, norm(p)) if int(n)}


for fam, pv in (("N", "HoldPrev"), ("R", "HoldPrevRedir")):
    for c in ("both", "concrete"):
        for b in ("chrome", "firefox"):
            a, p = now("tlc-HoldAllowed-%s-%s.out" % (fam, c), b), prev("prev-%s-%s.out" % (pv, c), b)
            print(fam, c, b, "now", len(a), "prev family", len(p), "| new:", sorted(a - p), "| lost:", sorted(p - a))
