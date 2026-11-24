"""Summarize bugs.tsv and the TLC outputs of run.sh.

usage: python3 -I summarize.py <bugs.tsv> <dir with tlc-*.out> <SpecIsolation.tla>

Prints counts by type and mapping, then, per cfg (both / concrete), kill rates
of the bug-derived mutants (BugMutants!New) and of the author's mutants
(BugMutants!Author) over the union of the four observation sets. A mutant is
killed if some browser kills it on some set (an observation inside the
unmutated set and outside the mutant's). It is equivalent if its allowed sets
equal the unmutated ones on the rows of every set.
"""
import collections
import csv
import glob
import os
import re
import sys

bugs_path, tlc_dir, spec_path = sys.argv[1:4]
rows = list(csv.DictReader(open(bugs_path), delimiter="\t"))
inc = [r for r in rows if r["maps"] != "out"]
print("bugs", len(rows), "counted", len(inc), "out", len(rows) - len(inc))
tc = collections.Counter(r["type"] for r in inc)
print("by type", sorted(tc.items()))
print("by mapping", sorted(collections.Counter(r["maps"] for r in inc).items()))
m_n = sum(v for k, v in tc.items() if k.startswith("M"))
print("model-step types (M*)", m_n, "non-model (N*)", len(inc) - m_n)
print("missing axes ranked", collections.Counter(r["type"] for r in inc if r["type"].startswith("N")).most_common())
print("steps the model lacks", sorted(collections.Counter(r["new_mutant_id"] for r in inc if r["maps"] == "step").items()))
print("bug-instance mutants", sorted(collections.Counter(r["new_mutant_id"] for r in inc if r["maps"] == "existing").items()))

spec = open(spec_path).read()
fix = set(re.findall(r'"([a-z-]+)"', re.search(r"FixIds == \{([^}]*)\}", spec).group(1)))


def is_new(m):
    if m.startswith("true:"):
        return True
    if m.startswith("false:"):
        d = m[len("false:"):]
        return d not in fix and not d.startswith("g2-")
    return False


LINE = re.compile(r'<<"k", "(\w+)", "(\w+)", "(\w+)", "([^"]+)", (\d+), (TRUE|FALSE)>>')
kill = collections.defaultdict(lambda: collections.defaultdict(int))
sets = collections.defaultdict(lambda: collections.defaultdict(set))
same = collections.defaultdict(dict)
for f in sorted(glob.glob(os.path.join(tlc_dir, "tlc-*.out"))):
    for line in open(f):
        g = LINE.search(line)
        if not g:
            continue
        pipe, cfg, browser, m, n, eq = g.groups()
        kill[cfg][m] += int(n)
        if int(n):
            sets[cfg][m].add(pipe + ":" + browser)
        same[cfg][m] = same[cfg].get(m, True) and eq == "TRUE"

for cfg in sorted(kill):
    for label, pred in (("bug-derived (New)", is_new), ("author", lambda m: not is_new(m))):
        ms = sorted(m for m in kill[cfg] if pred(m))
        k = [m for m in ms if kill[cfg][m] > 0]
        eq = [m for m in ms if kill[cfg][m] == 0 and same[cfg][m]]
        surv = [m for m in ms if kill[cfg][m] == 0 and not same[cfg][m]]
        print("cfg", cfg, label, "total", len(ms), "killed", len(k), "equivalent-on-all-rows", len(eq),
              "survived-nonequivalent", len(surv))
        if label.startswith("bug"):
            print("  equivalent:", " ".join(eq))
            print("  survived:", " ".join(surv))
            only = collections.Counter(
                ",".join(sorted({s.split(":")[0] for s in sets[cfg][m]})) for m in k)
            print("  killing sets:", sorted(only.items()))
        else:
            print("  survived:", " ".join(surv))
    inst = ["false:mc-ancestor", "neg:hop-update", "first-hop-only", "false:g2-sb-opaque", "false:g2-pp-self"]
    print("cfg", cfg, "bug-instance", [(m, kill[cfg][m], sorted(sets[cfg][m])) for m in inst])
