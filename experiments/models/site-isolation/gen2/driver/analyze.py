"""Summarize Gen2Allowed TLC outputs against the gen/ and WPT baselines.

usage: python3 -I analyze.py <gen2 tlc dir> <gen tlc dir> <WPT baseline dir>
  gen2 tlc dir: tlc-Gen2Allowed-{spec,7617}-{both,concrete}.out
  gen tlc dir:  tlc-GenAllowed.out, tlc-GenAllowed-concrete.out, tlc-GenEnum.out (gen/RESULTS.md)
  WPT dir:      tlc-both.out, tlc-concrete.out (109 WPT rows, fixed model)
"""
import collections
import re
import sys

g2, gd, wd = sys.argv[1:4]
norm = lambda p: re.sub(r"\s+", " ", open(p, encoding="utf-8").read())


def section(t, start, stop):
    i = t.index(start)
    j = t.find(stop, i + len(start))
    return t[i:j if j >= 0 else len(t)]


def killed_old(path, b):
    """mutant names in the "killed" line of browser b (gen/ or WPT baseline output)."""
    t = norm(path)
    s = re.search(r'<< ?"killed", "%s", \{' % b, t)
    body = t[s.end():]
    body = body[:re.search(r'<< ?"(survived-nonequivalent|out-of-model|rescuing|counts)"', body).start()]
    return set(re.findall(r'<< ?"([^"]+)", (?:\d+|\{)', body))


old_equiv = set(re.findall(r'"([^"]+)"', section(norm(gd + "/tlc-GenEnum.out"), '"equivalent-on-space"', ">>")))
old_equiv.discard("equivalent-on-space")
base = {}
for cc, gf, wf in [("both", "tlc-GenAllowed.out", "tlc-both.out"),
                   ("concrete", "tlc-GenAllowed-concrete.out", "tlc-concrete.out")]:
    base[cc] = {b: (killed_old(gd + "/" + gf, b), killed_old(wd + "/" + wf, b)) for b in ("chrome", "firefox")}

for p in ("spec", "7617"):
    for cc in ("both", "concrete"):
        cfg = "%s-%s" % (p, cc)
        t = norm("%s/tlc-Gen2Allowed-%s.out" % (g2, cfg))
        ms = int(re.search(r'<< ?"cfg", "%s", "rows", (\d+), "mutants", (\d+)' % cfg, t).group(2))
        eq = set(re.findall(r'"([^"]+)"', section(t, '"equivalent", "%s"' % cfg, ">>")))
        eq -= {"equivalent", cfg}
        print("== %s: mutants %d, equivalent on rows %d %s" % (cfg, ms, len(eq), sorted(eq)))
        for b in ("chrome", "firefox"):
            c = re.search(r'<< ?"counts", "%s", "%s", (\d+), (\d+), (\d+) ?>>' % (cfg, b), t).groups()
            kills = {m: set(re.findall(r'"([^"]+)"', ids))
                     for m, ids in re.findall(r'<< ?"kill", "%s", "%s", "([^"]+)", \{([^}]*)\} ?>>' % (cfg, b), t)}
            k = {m for m, s in kills.items() if s}
            g2old = {m for m in k if not m.startswith(("neg:g2-", "false:g2-"))}
            gk, wk = base[cc][b]
            out = re.findall(r'<< ?"out", "%s", "%s", "([^"]+)", (\{[^}]*\}), (\{[^}]*\}) ?>>' % (cfg, b), t)
            fam = collections.Counter(r.split(".")[0][0] + "." + r.split(".")[1] for r, _, _ in out)
            print("  %s rows %s inside %s out %s %s" % (b, c[0], c[1], c[2], dict(sorted(fam.items()))))
            print("    killed: all %d, old-55 %d, g2 %d; gen %d, WPT %d, gen|WPT %d, gen2|gen|WPT %d"
                  % (len(k), len(g2old), len(k) - len(g2old), len(gk), len(wk), len(gk | wk), len(g2old | gk | wk)))
            print("    old-24 killed %d: %s" % (len(old_equiv & k), sorted(old_equiv & k)))
            print("    old-24 not killed: %s" % sorted(old_equiv - k))
            print("    new beyond gen|WPT: %s" % sorted(g2old - gk - wk))
            print("    not killed, any: %s" % sorted(m for m in kills if m not in k))
            fk = {m: collections.Counter(r.split(".")[0][0] for r in kills[m]) for m in k}
            print("    kill rows per family:", {m: dict(fk[m]) for m in sorted(old_equiv & k)})
            for r, ob, al in out[:400]:
                print("    OUT", r, ob, al)
