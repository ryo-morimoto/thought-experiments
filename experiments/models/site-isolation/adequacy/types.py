"""Relational-type coverage of the origin domains (adequacy/RESULTS.md).

usage: python3 -I adequacy/types.py      (from site-isolation/)

An origin is (scheme, host, site) as in SpecIsolation.tla. The type of a
k-tuple of origins is, per element, its scheme and, per pair, whether the two
are equal (SameOrigin) and same site (SameSite): the "coarse" type, all that
SameOrigin/SameSite/Secure can see. The "fine" type adds same host (what
HttpsTwin and Key can see). A domain realizes a type if some k-tuple over it
has that type. The possible types are those of a domain with k sites x k hosts
x 2 schemes (enough for any k-tuple).
"""
import importlib.util
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def og(s, h, st):
    return (s, h, st)


def dom(sites, subs):
    return {og(s, st if sub == "" else sub + "." + st, st)
            for s in ("https", "http") for st in sites for sub in subs}


OA = og("https", "a.test", "a.test")
OAwww = og("https", "www1.a.test", "a.test")
OB = og("https", "b.test", "b.test")
OAhttp = og("http", "a.test", "a.test")
OAwww2 = og("https", "www2.a.test", "a.test")
OAwwwhttp = og("http", "www1.a.test", "a.test")
OBhttp = og("http", "b.test", "b.test")
ORIGINS = {OA, OAwww, OB, OAhttp}
ALL = ORIGINS | {OAwww2, OAwwwhttp, OBhttp}
D12 = dom(["a.test"], ["", "www1", "www2"]) | dom(["b.test"], ["", "www1"]) | dom(["c.test"], [""])
D18 = dom(["a.test", "b.test", "c.test"], ["", "www1", "www2"])


def ty(t, fine):
    k = len(t)
    pairs = tuple((t[i] == t[j], t[i][2] == t[j][2]) + ((t[i][1] == t[j][1],) if fine else ())
                  for i in range(k) for j in range(i + 1, k))
    return tuple(x[0] for x in t), pairs


def universe(k):
    sites = ["s%d" % i for i in range(k)]
    return dom(sites, [""] + ["h%d" % i for i in range(1, k)])


def types_over(tuples, fine):
    return {ty(t, fine) for t in tuples}


def possible(k, fine):
    return types_over(itertools.product(sorted(universe(k)), repeat=k), fine)


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gen_tuples():
    """(top, level 1, level 2, fetch target) over gen.py's whole depth-2 space."""
    g = load("gen", "gen/gen.py")
    H = {"a": "a.test", "a1": "www1.a.test", "a2": "www2.a.test",
         "b": "b.test", "b1": "www1.b.test", "b2": "www2.b.test"}
    o = lambda s, h: og(s, H[h], H[h[0]])
    for t in g.TOPS:
        for c1 in g.CHILD:
            for c2 in g.CHILD:
                lv = g.levels([c1, c2])
                yield (o(t[0], "a"), o(lv[0]["s"], lv[0]["h"]), o(lv[1]["s"], lv[1]["h"]),
                       o("https", g.other_site(lv[1]["h"])))


def gen2_tuples():
    rec = re.compile(r'\[scheme \|-> "(\w+)", host \|-> "(\w+)", site \|-> "(\w+)"\]')
    fam = re.compile(r'fam \|-> "(\w)"')
    out = {}
    with open(os.path.join(ROOT, "gen2/Gen2Space.tla"), encoding="utf-8") as f:
        for line in f:
            m = fam.search(line)
            if m:
                out.setdefault(m.group(1), set()).add(tuple(rec.findall(line)))
    return out


def redirect_tuples(n):
    """(opener A, hop 1..n, final) of redirect/gen.py's space, as RedirectSeq's Org."""
    org = [OA, OAwww, OB]
    for hs in itertools.product(org, repeat=n + 1):
        yield (OA,) + hs


def report(label, tuples, k):
    tuples = list(tuples)
    for fine in (False, True):
        have, want = types_over(tuples, fine), possible(k, fine)
        print("%-34s k=%d %-6s %4d / %4d types%s" % (label, k, "fine" if fine else "coarse",
              len(have & want), len(want), "" if have <= want else " (!)"))


def main():
    for name, d in (("Origins (4)", ORIGINS), ("AllOrigins (7)", ALL), ("D12", D12), ("D18", D18)):
        for k in (2, 3):
            report("domain " + name, itertools.product(sorted(d), repeat=k), k)
    report("gen depth 2 (top,l1,l2,tgt)", gen_tuples(), 4)
    report("gen depth 2 (top,l1,l2)", (t[:3] for t in gen_tuples()), 3)
    for fam, ts in sorted(gen2_tuples().items()):
        k = len(next(iter(ts)))
        report("gen2 family %s" % fam, ts, k)
    for n in (1, 2):
        report("redirect (A, %d hops, final)" % n, redirect_tuples(n), n + 2)
    # Pair types missing from Origins (k = 2, coarse).
    miss = possible(2, False) - types_over(itertools.product(sorted(ORIGINS), repeat=2), False)
    print("pair types missing from Origins:", sorted(miss))
    miss3 = possible(3, False) - types_over(itertools.product(sorted(ORIGINS), repeat=3), False)
    print("triple types missing from Origins:", len(miss3))
    miss3a = possible(3, False) - types_over(itertools.product(sorted(ALL), repeat=3), False)
    print("triple types missing from AllOrigins:", len(miss3a), sorted(miss3a)[:6])


if __name__ == "__main__":
    sys.exit(main())
