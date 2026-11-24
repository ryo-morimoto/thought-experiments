"""Group the out-of-model N rows of a HoldAllowed output by structure.

usage: python3 -I outrows.py <tlc-HoldAllowed-N-*.out> <scenarios.tsv> <browser>
Key: top config, level, relation of the level to its parent (so / ss same
site / xs), relation of level 1 to the top (for level 2), the level's CORP,
and the level's scheme.
"""
import collections
import csv
import re
import sys

text = re.sub(r"\s+", " ", open(sys.argv[1], encoding="utf-8").read())
ids = re.findall(r'<< ?"out", "[^"]+", "%s", "([^"]+)"' % sys.argv[3], text)
sc = {r["sid"]: r for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"), delimiter="\t")}


def rel(a, b):
    if a == b:
        return "so"
    return "ss" if a.split(".")[-2:] == b.split(".")[-2:] else "xs"


c = collections.Counter()
for i in ids:
    sid, lvl, kind = i.split(".")
    r = sc[sid]
    o = [p for p in r["origins"].split("|") if not p.startswith("tgt")]
    lvl = int(lvl)
    cfg = r["config"].split()
    c[(kind, cfg[0], lvl, rel(o[lvl], o[lvl - 1]), rel(o[1], o[0]) if lvl == 2 else "-",
       cfg[lvl].split("/")[1], o[lvl].split("/")[0])] += 1
for k, v in sorted(c.items()):
    print(v, k)
