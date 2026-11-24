"""Generator of the frozen-holdout scenarios (holdout/RESULTS.md,
experiments/prereg/2026-11-24-frozen-holdout.md).

usage:
  python3 -I gen_holdout.py space <out dir>
        write HoldSpace.tla (origin tables and the whole pre-screen space of
        both families) and space.tsv
  python3 -I gen_holdout.py select <out dir> <enum output>...
        read the TLC class lines of HoldNestEnum / HoldRedirEnum, pick the
        scenarios, write scenarios.tsv and tests/ into <out dir>

Origins are records as in ../SpecIsolation.tla: (scheme, host, site), sites
a.test, b.test, c.test, d.test, hosts bare / www / www1 / www2. In the browser
a = web-platform.test, b = not-web-platform.test, c = web-platform-c.test,
d = web-platform-d.test (driver/incontainer.sh adds c and d).

Family N (nested frames, GenModel): top (level 0) at bare a, its scheme given
by the type; levels 1 and 2 any of 3 sites x 4 hosts x 2 schemes. For each of
the 66 coarse relational types of (top, l1, l2) (per element: scheme; per
pair: same origin, same site), one representative triple is drawn (seed).
Axes per representative: top COEP (3) x COOP (2) x l1 (COEP 3 x CORP 3) x l2
(COEP 3 x CORP 3) x fetch target (3: "xs" https bare d, a site no level has;
"ss" https, same site as l2, other host; "ht" http, same host as l2). The full
product is 66 x 6 x 243 = 96228. The pre-screen space takes, for each of the
396 (representative, top configuration) strata, 48 of the 243 child/target
combinations, assigned cyclically over a seeded permutation (each combination
occurs 78 or 79 times): 19008 scenarios.

Family R (popup redirect chains, RedirectSeq): opener fixed at https bare a
(SI!OA). Hop and final origins from 4 sites x 4 hosts x 2 schemes. One
representative per coarse type of (A, final) [5], (A, hop, final) [33] and
(A, hop1, hop2, final) [269]. Axes: opener COOP (4) x start (2) x hop codes
(4 each) x final COOP (3) x final COEP (2). 0 and 1 hop: every combination
(240 + 6336). 2 hops: 48 of the 768 combinations per representative,
assigned cyclically over a seeded permutation so each combination occurs 16
or 17 times (12912). Total 19488.
"""
import collections
import itertools
import os
import random
import re
import sys

SEED = 20261125          # new seed (gen/, gen2/ and redirect/ used 20261124)
SITES = ["a", "b", "c", "d"]
SUBS = ["", "www", "www1", "www2"]
SCHEMES = ["https", "http"]
COEPS = ["unsafe-none", "require-corp", "credentialless"]
COOPS = ["unsafe-none", "same-origin"]
CORPS = ["none", "same-origin", "cross-origin"]
TGTS = ["xs", "ss", "ht"]
TOPCFG = list(itertools.product(COEPS, COOPS))           # 6
CHILDCFG = list(itertools.product(COEPS, CORPS))          # 9
OP = ["unsafe-none", "same-origin-allow-popups", "same-origin", "so+rc"]
OPc = ["u", "p", "s", "c"]
ST = ["blank", "doc"]
FC = ["unsafe-none", "same-origin-allow-popups", "same-origin"]
FE = ["unsafe-none", "require-corp"]
K2 = 48
KN = 48
K_CLASS, K_NONE, K_STRATUM = 2, 12, 2
CHUNK_N, CHUNK_R = 200, 60
AB = {"unsafe-none": "un", "require-corp": "rc", "credentialless": "cl", "same-origin": "so",
      "cross-origin": "xo", "none": "no", "same-origin-allow-popups": "sap"}


def org(scheme, site, sub):
    return (scheme, (sub + "." if sub else "") + site + ".test", site + ".test")


def dom(sites):
    return [org(s, st, sub) for s in SCHEMES for st in sites for sub in SUBS]


A = org("https", "a", "")


def ty(t):
    k = len(t)
    return (tuple(x[0] for x in t),
            tuple((t[i] == t[j], t[i][2] == t[j][2]) for i in range(k) for j in range(i + 1, k)))


def reps(tuples, rng):
    """One representative per type, drawn with rng; returns [(type, tuple)] sorted by type."""
    by = collections.defaultdict(list)
    for t in tuples:
        by[ty(t)].append(t)
    return [(k, rng.choice(sorted(by[k]))) for k in sorted(by)]


def hostkey(o):
    """Browser host key: site letter + last letter of the subdomain ('a', 'aw', 'a1', 'c2')."""
    sub, site = (o[1].split(".")[0], o[2][0]) if o[1].count(".") == 2 else ("", o[2][0])
    return site + (sub[-1] if sub else "")


def tla_o(o):
    return '[scheme |-> "%s", host |-> "%s", site |-> "%s"]' % o


def nest_tgts(trip):
    l2 = trip[2]
    xs = org("https", "d", "")
    sub = l2[1].split(".")[0] if l2[1].count(".") == 2 else ""
    ss = org("https", l2[2][0], "www1" if sub == "" else "")
    ht = ("http", l2[1], l2[2])
    return [xs, ss, ht]


def build(rng):
    # Family N: top at bare a (scheme free), l1, l2 over sites a, b, c.
    d3 = dom(["a", "b", "c"])
    trips = [(org(s, "a", ""), x, y) for s in SCHEMES for x in d3 for y in d3]
    nreps = reps(trips, rng)
    ncombos = list(itertools.product(range(9), range(9), range(3)))
    rng.shuffle(ncombos)
    strata = [(r, t) for r in range(len(nreps)) for t in range(6)]
    rng.shuffle(strata)
    nspace = []
    for pos, (r, t) in enumerate(strata):
        for j in range(KN):
            c1, c2, g = ncombos[(pos * KN + j) % len(ncombos)]
            nspace.append((r + 1, t + 1, c1 + 1, c2 + 1, g + 1))
    nspace.sort()
    # Family R: hop/final origins over 4 sites.
    d4 = dom(SITES)
    r0 = reps([(A, f) for f in d4], rng)
    r1 = reps([(A, h, f) for h in d4 for f in d4], rng)
    r2 = reps([(A, h1, h2, f) for h1 in d4 for h2 in d4 for f in d4], rng)
    rreps = [t[1:] for _, t in r0 + r1 + r2]      # (hops..., final)
    rspace = []
    for i, (_, t) in enumerate(r0):
        for op, st, fc, fe in itertools.product(range(4), range(2), range(3), range(2)):
            rspace.append((op + 1, st + 1, i + 1, (), fc + 1, fe + 1))
    base = len(r0)
    for i, (_, t) in enumerate(r1):
        for op, st, h, fc, fe in itertools.product(range(4), range(2), range(4), range(3), range(2)):
            rspace.append((op + 1, st + 1, base + i + 1, (h + 1,), fc + 1, fe + 1))
    base += len(r1)
    combos = list(itertools.product(range(4), range(2), range(4), range(4), range(3), range(2)))
    rng.shuffle(combos)
    order = list(range(len(r2)))
    rng.shuffle(order)
    for pos, i in enumerate(order):
        for j in range(K2):
            op, st, h1, h2, fc, fe = combos[(pos * K2 + j) % len(combos)]
            rspace.append((op + 1, st + 1, base + i + 1, (h1 + 1, h2 + 1), fc + 1, fe + 1))
    rspace.sort(key=lambda x: (x[2], x))
    return nreps, nspace, rreps, (len(r0), len(r1), len(r2)), rspace


def write_space(out):
    rng = random.Random(SEED)
    nreps, nspace, rreps, rn, rspace = build(rng)
    with open(os.path.join(out, "HoldSpace.tla"), "w", encoding="utf-8") as f:
        f.write("---- MODULE HoldSpace ----\n(* generated by holdout/gen_holdout.py space, seed %d *)\n" % SEED)
        f.write("TopCfg == <<%s>>\n" % ", ".join('[e |-> "%s", coop |-> "%s"]' % c for c in TOPCFG))
        f.write("ChildCfg == <<%s>>\n" % ", ".join('[e |-> "%s", corp |-> "%s"]' % c for c in CHILDCFG))
        f.write("NestRep == <<\n  " + ",\n  ".join(
            "[o |-> <<%s>>, tg |-> <<%s>>]" % (", ".join(tla_o(o) for o in t), ", ".join(tla_o(o) for o in nest_tgts(t)))
            for _, t in nreps) + ">>\n")
        f.write("NestSpace == <<\n  " + ",\n  ".join("<<%d, %d, %d, %d, %d>>" % x for x in nspace) + ">>\n")
        f.write("RedirRep == <<\n  " + ",\n  ".join(
            "[hops |-> <<%s>>, fin |-> %s]" % (", ".join(tla_o(o) for o in t[:-1]), tla_o(t[-1])) for t in rreps) + ">>\n")
        f.write("RedirSpace == <<\n  " + ",\n  ".join(
            "<<%d, %d, %d, <<%s>>, %d, %d>>" % (x[0], x[1], x[2], ", ".join(map(str, x[3])), x[4], x[5])
            for x in rspace) + ">>\n====\n")
    with open(os.path.join(out, "space.tsv"), "w", encoding="utf-8") as f:
        f.write("family\tindex\trep\tcode\torigins\n")
        for i, x in enumerate(nspace):
            f.write("N\t%d\t%d\t%s\t%s\n" % (i + 1, x[0], ",".join(map(str, x)), "|".join(
                "/".join(o[:2]) for o in nreps[x[0] - 1][1])))
        for i, x in enumerate(rspace):
            f.write("R\t%d\t%d\t%s\t%s\n" % (i + 1, x[2], "%d,%d,%s,%d,%d" % (x[0], x[1], "-".join(map(str, x[3])) or "0", x[4], x[5]),
                                             "|".join("/".join(o[:2]) for o in rreps[x[2] - 1])))
    print("seed", SEED, "N reps", len(nreps), "N space", len(nspace), "R reps", rn, "R space", len(rspace))


# ---------------------------------------------------------------- selection
def parse_classes(paths, fam):
    """Lines <<"class", fam, lo, DL, DC, members>> from the TLC outputs."""
    cl = collections.defaultdict(set)
    for p in paths:
        text = re.sub(r"\s+", " ", open(p, encoding="utf-8").read())
        for dl, dc, mem in re.findall(r'<< ?"class", "%s", \d+, \{([^}]*)\}, \{([^}]*)\}, \{([^}]*)\} ?>>' % fam, text):
            key = (tuple(sorted(v.strip() for v in dl.split(",") if v.strip())),
                   tuple(sorted(v.strip() for v in dc.split(",") if v.strip())))
            cl[key].update(int(v) for v in mem.replace(" ", "").split(",") if v)
    return cl


def pick(classes, stratum_of, rng):
    chosen = set()
    for key in sorted(classes):
        idx = sorted(classes[key])
        k = K_CLASS if (key[0] or key[1]) else K_NONE
        chosen.update(rng.sample(idx, min(k, len(idx))))
    return chosen


def select(out, enum_outs):
    rng = random.Random(SEED)
    nreps, nspace, rreps, rn, rspace = build(rng)
    rng = random.Random(SEED + 1)
    ncl, rcl = parse_classes(enum_outs, "N"), parse_classes(enum_outs, "R")
    assert sum(len(v) for v in ncl.values()) == len(nspace), "N classes do not cover the space"
    assert sum(len(v) for v in rcl.values()) == len(rspace), "R classes do not cover the space"
    nch = pick(ncl, None, rng)
    strata = collections.defaultdict(list)          # N: (rep, top cfg)
    for i, x in enumerate(nspace):
        strata[(x[0], x[1])].append(i + 1)
    for k in sorted(strata):
        have = [i for i in strata[k] if i in nch]
        rest = sorted(set(strata[k]) - nch)
        nch.update(rng.sample(rest, min(len(rest), max(0, K_STRATUM - len(have)))))
    rch = pick(rcl, None, rng)
    rstr = collections.defaultdict(list)            # R: origin representative
    for i, x in enumerate(rspace):
        rstr[x[2]].append(i + 1)
    for k in sorted(rstr):
        if not any(i in rch for i in rstr[k]):
            rch.add(rng.choice(rstr[k]))
    print("N classes", len(ncl), "chosen", len(nch), "| R classes", len(rcl), "chosen", len(rch))
    write_selected(out, sorted(nch), sorted(rch), nreps, nspace, rreps, rspace)


def nsid(i):
    return "n%05d" % i


def rsid(i):
    return "r%05d" % i


def write_selected(out, nch, rch, nreps, nspace, rreps, rspace):
    tdir = os.path.join(out, "tests")
    os.makedirs(tdir, exist_ok=True)
    with open(os.path.join(out, "scenarios.tsv"), "w", encoding="utf-8") as f:
        f.write("sid\tfamily\tindex\tcode\torigins\tconfig\n")
        for i in nch:
            x = nspace[i - 1]
            trip = nreps[x[0] - 1][1]
            tc, c1, c2 = TOPCFG[x[1] - 1], CHILDCFG[x[2] - 1], CHILDCFG[x[3] - 1]
            tg = nest_tgts(trip)[x[4] - 1]
            f.write("%s\tN\t%d\t%s\t%s\t%s\n" % (nsid(i), i, ",".join(map(str, x)),
                    "|".join("/".join(o[:2]) for o in trip) + "|tgt=" + "/".join(tg[:2]),
                    "top=%s/%s l1=%s/%s l2=%s/%s" % (tc + c1 + c2)))
        for i in rch:
            x = rspace[i - 1]
            f.write("%s\tR\t%d\t%s\t%s\t%s\n" % (rsid(i), i, "%d,%d,%d,%s,%d,%d" % (
                x[0], x[1], x[2], "-".join(map(str, x[3])) or "0", x[4], x[5]),
                "|".join("/".join(o[:2]) for o in rreps[x[2] - 1]),
                "op=%s st=%s hops=%s fin=%s/%s" % (OP[x[0] - 1], ST[x[1] - 1], ",".join(OP[h - 1] for h in x[3]) or "-",
                                                    FC[x[4] - 1], FE[x[5] - 1])))
    # N test files: one per top (scheme, COEP, COOP), chunks of CHUNK_N.
    groups = collections.defaultdict(list)
    for i in nch:
        x = nspace[i - 1]
        trip = nreps[x[0] - 1][1]
        tc = TOPCFG[x[1] - 1]
        lv = [(trip[1], CHILDCFG[x[2] - 1]), (trip[2], CHILDCFG[x[3] - 1])]
        tg = nest_tgts(trip)[x[4] - 1]
        js = '{id:"%s",t:{s:"%s",h:"%s"},lv:[%s]}' % (nsid(i), tg[0], hostkey(tg), ",".join(
            '{s:"%s",h:"%s",coep:"%s",corp:"%s"}' % (o[0], hostkey(o), c[0], c[1]) for o, c in lv))
        groups[(trip[0][0],) + tc].append(js)
    for key in sorted(groups):
        rows = groups[key]
        for n in range(0, len(rows), CHUNK_N):
            stem = "n-%s-%s-%s-%02d%s.sub.html" % (key[0], AB[key[1]], AB[key[2]], n // CHUNK_N,
                                                   ".https" if key[0] == "https" else "")
            with open(os.path.join(tdir, stem), "w", encoding="utf-8") as f:
                f.write(NPAGE % (stem, stem, ",\n".join(rows[n:n + CHUNK_N])))
            hdr = []
            if key[1] != "unsafe-none":
                hdr.append("Cross-Origin-Embedder-Policy: " + key[1])
            if key[2] != "unsafe-none":
                hdr.append("Cross-Origin-Opener-Policy: " + key[2])
            if hdr:
                with open(os.path.join(tdir, stem + ".headers"), "w", encoding="utf-8") as f:
                    f.write("\n".join(hdr) + "\n")
    # R test files: one per opener COOP, chunks of CHUNK_R.
    for op in range(4):
        rows = []
        for i in rch:
            x = rspace[i - 1]
            if x[0] != op + 1:
                continue
            t = rreps[x[2] - 1]
            hops = ", ".join('{s: "%s", h: "%s", coop: "%s", coep: "%s"}' % ((o[0], hostkey(o)) + hdr2(OP[c - 1]))
                             for o, c in zip(t[:-1], x[3]))
            fo = t[-1]
            rows.append('  {id: "%s", st: "%s", hops: [%s], fin: {s: "%s", h: "%s", coop: "%s", coep: "%s"}},' % (
                rsid(i), ST[x[1] - 1], hops, fo[0], hostkey(fo), FC[x[4] - 1], FE[x[5] - 1]))
        for n in range(0, len(rows), CHUNK_R):
            stem = "r-%s-%02d.sub.https.html" % (OPc[op], n // CHUNK_R)
            coop, coep = hdr2(OP[op])
            with open(os.path.join(tdir, stem), "w", encoding="utf-8") as f:
                f.write(RPAGE.replace("{label}", OP[op]).replace(
                    "{opener}", '{coop: "%s", coep: "%s"}' % (coop, coep)).replace("{rows}", "\n".join(rows[n:n + CHUNK_R])))
            h = ([] if coop == "unsafe-none" else ["Cross-Origin-Opener-Policy: " + coop]) + \
                ([] if coep == "unsafe-none" else ["Cross-Origin-Embedder-Policy: " + coep])
            if h:
                with open(os.path.join(tdir, stem + ".headers"), "w", encoding="utf-8") as f:
                    f.write("\n".join(h) + "\n")


def hdr2(v):
    return ("same-origin", "require-corp") if v == "so+rc" else (v, "unsafe-none")


HOSTS_JS = """const HOSTS = {
  a: "{{host}}", aw: "{{hosts[][www]}}", a1: "{{hosts[][www1]}}", a2: "{{hosts[][www2]}}",
  b: "{{hosts[alt][]}}", bw: "{{hosts[alt][www]}}", b1: "{{hosts[alt][www1]}}", b2: "{{hosts[alt][www2]}}",
  c: "{{hosts[alt2][]}}", cw: "{{hosts[alt2][www]}}", c1: "{{hosts[alt2][www1]}}", c2: "{{hosts[alt2][www2]}}",
  d: "{{hosts[alt3][]}}", dw: "{{hosts[alt3][www]}}", d1: "{{hosts[alt3][www1]}}", d2: "{{hosts[alt3][www2]}}"};
const PORTS = {http: {{ports[http][0]}}, https: {{ports[https][0]}}};"""

NPAGE = """<!doctype html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>holdout nested scenarios %s</title>
<script src=/resources/testharness.js></script>
<script src=/resources/testharnessreport.js></script>
<script src=resources/hobs.js></script>
<body>
<script>
""" + HOSTS_JS + """
const TOP_ID = "%s";
const SCEN = [
%s
];
runNest();
</script>
"""

RPAGE = """<!DOCTYPE html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>holdout redirect chains, opener COOP {label}</title>
<script src="/resources/testharness.js"></script>
<script src="/resources/testharnessreport.js"></script>
<script src="/common/dispatcher/dispatcher.js"></script>
<script src="/common/utils.js"></script>
<script src="resources/hrobs.js"></script>
<body>
<script>
""" + HOSTS_JS + """
const OPENER = {opener};
const SCEN = [
{rows}
];
runRedirect(SCEN).then(done);
</script>
"""

if __name__ == "__main__":
    if sys.argv[1] == "space":
        write_space(sys.argv[2])
    else:
        select(sys.argv[2], sys.argv[3:])
