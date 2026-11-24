"""Summarize Gen3Allowed TLC outputs, against bugmut/'s kill counts on the four earlier sets.

usage: python3 -I analyze.py <gen3 tlc dir> <bugmut tlc dir>
  gen3 tlc dir:   tlc-Gen3Allowed-{both,concrete}-{may,exact}.out
  bugmut tlc dir: tlc-{observe,gen,gen2,redirect}-{both,concrete}.out (bugmut/run.sh)
Prints, per cfg and browser: row counts, out-of-model rows by family and kind,
kills of the G3 mutants and of bugmut's bug-type mutants, and the mutants that
no earlier set killed and gen3 kills.
"""
import collections
import glob
import os
import re
import sys

g3, bm = sys.argv[1:3]
norm = lambda p: re.sub(r"\s+", " ", open(p, encoding="utf-8").read())
LINE = re.compile(r'<<"k", "(\w+)", "(\w+)", "(\w+)", "([^"]+)", (\d+), (TRUE|FALSE)>>')
prior = collections.defaultdict(lambda: collections.defaultdict(int))
for f in glob.glob(os.path.join(bm, "tlc-*.out")):
    for line in open(f, encoding="utf-8"):
        g = LINE.search(line)
        if g:
            prior[g.group(2)][g.group(4)] += int(g.group(5))
is_g3 = lambda m: m.startswith(("neg:g3-", "false:g3-", "true:g3-")) or m == "od-as-origin"
FIX = ("secure-ctx-top", "nav-corp-check", "nav-coep-adherence", "mc-ancestor", "mc-upgrade", "mc-block")
is_bug = lambda m: not is_g3(m) and (m.startswith("true:") or
                                     (m.startswith("false:") and m.split(":", 1)[1] not in FIX))
for cfg in ("both-may", "concrete-may", "both-exact", "concrete-exact"):
    p = os.path.join(g3, "tlc-Gen3Allowed-%s.out" % cfg)
    if not os.path.exists(p):
        continue
    t = norm(p)
    cc = cfg.split("-")[0]
    ms = int(re.search(r'<< ?"cfg", "%s", "rows", (\d+), "mutants", (\d+)' % cfg, t).group(2))
    eq = set(re.findall(r'"([^"]+)"', re.search(r'"equivalent", "%s", \{([^}]*)\}' % cfg, t).group(1)))
    print("== %s: mutants %d, equivalent on rows %d" % (cfg, ms, len(eq)))
    print("   equivalent G3:", sorted(m for m in eq if is_g3(m)))
    allk = {}
    for b in ("chrome", "firefox"):
        c = re.search(r'<< ?"counts", "%s", "%s", (\d+), (\d+), (\d+) ?>>' % (cfg, b), t).groups()
        kills = {m: set(re.findall(r'"([^"]+)"', ids))
                 for m, ids in re.findall(r'<< ?"kill", "%s", "%s", "([^"]+)", \{([^}]*)\} ?>>' % (cfg, b), t)}
        allk[b] = kills
        k = {m for m, s in kills.items() if s}
        out = re.findall(r'<< ?"out", "%s", "%s", "([^"]+)", (\{[^}]*\}), (\{[^}]*\}) ?>>' % (cfg, b), t)
        fam = collections.Counter(r[0] + "." + r.split(".")[1] for r, _, _ in out)
        g3m = {m for m in kills if is_g3(m)}
        bug = {m for m in kills if is_bug(m)}
        print("  %s rows %s inside %s out %s %s" % (b, c[0], c[1], c[2], dict(sorted(fam.items()))))
        print("    G3 killed %d/%d (non-equivalent %d)" % (len(g3m & k), len(g3m), len(g3m - eq)))
        print("    G3 not killed, non-equivalent:", sorted(g3m - k - eq))
        print("    bug-type killed %d/%d; not killed before, killed now: %s"
              % (len(bug & k), len(bug), sorted(m for m in bug & k if prior[cc].get(m, 0) == 0)))
        print("    any mutant not killed before (bugmut sets), killed now:",
              sorted(m for m in k if not is_g3(m) and prior[cc].get(m, 0) == 0))
        for r, ob, al in out:
            print("    OUT", r, ob, al)
    both = {m for m in allk["chrome"] if allk["chrome"][m] or allk["firefox"][m]}
    print("  either browser: G3 killed %d, all killed %d of %d" %
          (len({m for m in both if is_g3(m)}), len(both), ms))
