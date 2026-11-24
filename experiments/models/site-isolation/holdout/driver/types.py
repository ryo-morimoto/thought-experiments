"""Relational types realized by the run scenarios (prereg rule 5).

usage: python3 -I types.py <scenarios.tsv> [observed.tsv]
Coarse type as in adequacy/types.py: per element the scheme, per pair same
origin and same site. N: (top, l1, l2), 66 possible. R: (A, [hops], final)
with A = https a.test: 5 + 33 + 269 possible. With observed.tsv, a type counts
as observed only if some scenario of that type has a mapped row in both browsers.
"""
import collections
import csv
import sys


def o(s):
    sch, host = s.split("/")
    return (sch, host, ".".join(host.split(".")[-2:]))


def ty(t):
    k = len(t)
    return (tuple(x[0] for x in t),
            tuple((t[i] == t[j], t[i][2] == t[j][2]) for i in range(k) for j in range(i + 1, k)))


A = ("https", "a.test", "a.test")
seen = collections.defaultdict(lambda: collections.defaultdict(set))
if len(sys.argv) > 2:
    with open(sys.argv[2], encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            seen[r["row"].split(".")[0]][r["browser"]].add(r["row"])
types = collections.defaultdict(set)
obs_types = collections.defaultdict(set)
with open(sys.argv[1], encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        parts = [p for p in r["origins"].split("|") if not p.startswith("tgt=")]
        t = tuple(o(p) for p in parts)
        key = "N" if r["family"] == "N" else "R%d" % (len(t) - 1)
        if key != "N":
            t = (A,) + t
        types[key].add(ty(t))
        if len(seen[r["sid"]]) == 2:
            obs_types[key].add(ty(t))
for k in sorted(types):
    print(k, "types in run", len(types[k]), "observed in both browsers", len(obs_types[k]) if len(sys.argv) > 2 else "-")
