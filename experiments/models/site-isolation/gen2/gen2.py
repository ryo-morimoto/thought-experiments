"""Scenario generator for the popup / sandbox / OAC / CORP axes (gen2/RESULTS.md).

usage:
  python3 -I gen2.py space <out dir>             full space -> space.tsv, Gen2Space.tla
  python3 -I gen2.py select <out dir> <enum out> pick scenarios -> selected.tsv
  python3 -I gen2.py tests <out dir>             tests/ for selected.tsv

Families (one row per scenario in space.tsv; sid = family letter + index):
  P  popup: opener COOP {un, sap, so} x popup COOP {un, sap, so} x popup origin
     {same-origin, same-site, cross-site, cross-site http} x mode {direct,
     about:blank then navigate, noopener}                                  = 108
  O  Origin-Agent-Cluster, in a noopener popup: top {https, https+COI, http}
     x header of top, of child 1 (same-site other host), of child 2 (same
     origin as child 1) in {absent, ?0, ?1}                                = 81
  S  sandboxed iframe: top COEP {un, rc, cl} x top COOP {un, so} x sandbox
     {none, allow-scripts, allow-scripts allow-same-origin} x child relation
     {same-host, same-site, cross-site} x child COEP {un, rc} x child CORP
     {none, same-origin, cross-origin}                                     = 324
  C  CORP at top level: top scheme {https, http} x COEP {un, rc, cl} x target
     relation {same-host, same-site, cross-site} x target scheme {https,
     http, http on the https port (https tops only)} x CORP {none,
     same-origin, same-site, cross-origin} x {fetch(), <img>}              = 360
Hosts: a = web-platform.test, a1 = www1., b = not-web-platform.test.
"""
import csv
import itertools
import os
import random
import sys

SEED, FRACTION, MIN_COVER = 20261124, 0.30, 2
COOP3 = ["unsafe-none", "same-origin-allow-popups", "same-origin"]
OAC3 = ["absent", "?0", "?1"]
AB = {"unsafe-none": "un", "same-origin-allow-popups": "sap", "same-origin": "so",
      "require-corp": "rc", "credentialless": "cl", "cross-origin": "xo", "same-site": "ss",
      "none": "no"}
POP_REL = {"so": ("https", "a"), "ss": ("https", "a1"), "xs": ("https", "b"), "xshttp": ("http", "b")}
REL = {"same-host": "a", "same-site": "a1", "cross-site": "b"}


def other(h):
    return "b" if h[0] == "a" else "a"


def space():
    sc = []
    for oc, pc, rel, mode in itertools.product(COOP3, COOP3, POP_REL, ["direct", "blank", "noopener"]):
        sc.append(dict(fam="P", oc=oc, pc=pc, rel=rel, mode=mode))
    for top, h0, h1, h2 in itertools.product(["https", "https-coi", "http"], OAC3, OAC3, OAC3):
        sc.append(dict(fam="O", top=top, h0=h0, h1=h1, h2=h2))
    for te, tc, sb, rel, ce, corp in itertools.product(
            ["unsafe-none", "require-corp", "credentialless"], ["unsafe-none", "same-origin"],
            ["none", "scripts", "scripts-so"], REL, ["unsafe-none", "require-corp"],
            ["none", "same-origin", "cross-origin"]):
        sc.append(dict(fam="S", te=te, tc=tc, sb=sb, rel=rel, ce=ce, corp=corp))
    for ts, te, rel, rs, corp, dest in itertools.product(
            ["https", "http"], ["unsafe-none", "require-corp", "credentialless"], REL,
            ["https", "http", "http-tls"], ["none", "same-origin", "same-site", "cross-origin"],
            ["fetch", "img"]):
        if ts == "http" and rs == "http-tls":
            continue
        sc.append(dict(fam="C", ts=ts, te=te, rel=rel, rs=rs, corp=corp, dest=dest))
    n = {}
    for s in sc:
        n[s["fam"]] = n.get(s["fam"], 0) + 1
        s["sid"] = "%s%03d" % (s["fam"], n[s["fam"]])
    return sc


def stratum(s):
    """Stratum of the random sample: family and top configuration."""
    return {"P": lambda: ("P", s["oc"], s["mode"]), "O": lambda: ("O", s["top"]),
            "S": lambda: ("S", s["te"], s["tc"]), "C": lambda: ("C", s["ts"], s["te"])}[s["fam"]]()


def tla_origin(scheme, host):
    return '[scheme |-> "%s", host |-> "%s", site |-> "%s"]' % (scheme, host, host[0])


def tla_record(s):
    f = s["fam"]
    if f == "P":
        sch, h = POP_REL[s["rel"]]
        return ('[fam |-> "P", oc |-> "%s", pc |-> "%s", mode |-> "%s", oo |-> %s, po |-> %s]'
                % (s["oc"], s["pc"], s["mode"], tla_origin("https", "a"), tla_origin(sch, h)))
    if f == "O":
        sch = "http" if s["top"] == "http" else "https"
        return ('[fam |-> "O", coi |-> %s, h |-> <<"%s", "%s", "%s">>, o0 |-> %s, o1 |-> %s]'
                % ("TRUE" if s["top"] == "https-coi" else "FALSE", s["h0"], s["h1"], s["h2"],
                   tla_origin(sch, "a"), tla_origin(sch, "a1")))
    if f == "S":
        ch = REL[s["rel"]]
        return ('[fam |-> "S", te |-> "%s", tc |-> "%s", sb |-> "%s", ce |-> "%s", corp |-> "%s", '
                'to |-> %s, co |-> %s, xo |-> %s, xh |-> %s]'
                % (s["te"], s["tc"], s["sb"], s["ce"], s["corp"], tla_origin("https", "a"),
                   tla_origin("https", ch), tla_origin("https", other(ch)), tla_origin("http", other(ch))))
    h = REL[s["rel"]]
    sch = "http" if s["rs"] == "http-tls" else s["rs"]
    return ('[fam |-> "C", te |-> "%s", dest |-> "%s", served |-> %s, to |-> %s, r |-> [origin |-> %s, '
            'corp |-> "%s", creds |-> FALSE]]'
            % (s["te"], s["dest"], "FALSE" if s["rs"] == "http" else "TRUE",
               tla_origin(s["ts"], "a"), tla_origin(sch, h), s["corp"]))


FIELDS = ["sid", "fam", "oc", "pc", "rel", "mode", "top", "h0", "h1", "h2", "te", "tc", "sb", "ce",
          "corp", "ts", "rs", "dest"]


def write_tsv(path, rows, extra=()):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS + list(extra), delimiter="\t", lineterminator="\n", restval="")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        return [{k: v for k, v in r.items() if v != ""} for r in csv.DictReader(f, delimiter="\t")]


def cmd_space(out):
    sc = space()
    write_tsv(os.path.join(out, "space.tsv"), sc)
    with open(os.path.join(out, "Gen2Space.tla"), "w", encoding="utf-8") as f:
        f.write("---- MODULE Gen2Space ----\n(* generated by gen2.py space; do not edit *)\n")
        f.write("Scen == <<\n  " + ",\n  ".join(tla_record(s) for s in sc) + ">>\n====\n")
    print("space", len(sc), {k: sum(1 for s in sc if s["fam"] == k) for k in "POSC"})


def parse_enum(path):
    """<<"dist", cfg, mutant, {indices}>> lines of Gen2Enum's output -> {mutant: set(index)}."""
    import re
    t = re.sub(r"\s+", " ", open(path, encoding="utf-8").read())
    d = {}
    for m, body in re.findall(r'<< ?"dist", "[^"]*", "([^"]+)", \{([0-9, ]*)\} ?>>', t):
        d.setdefault(m, set()).update(int(x) for x in body.replace(" ", "").split(",") if x)
    return d


def cmd_select(out, enum_paths):
    sc = space()
    dist = {}
    for p in enum_paths.split(","):
        for m, s in parse_enum(p).items():
            dist.setdefault(m, set()).update(s)
    rng = random.Random(SEED)
    chosen = {}
    # Cover: each distinguishable mutant by MIN_COVER scenarios, greedily
    # (scenarios that distinguish the most still-uncovered mutants first).
    need = {m: MIN_COVER for m, s in dist.items() if s}
    while any(v > 0 for v in need.values()):
        best = max((i for i in range(1, len(sc) + 1) if i not in chosen),
                   key=lambda i: (sum(1 for m in need if need[m] > 0 and i in dist[m]), -i))
        gain = [m for m in need if need[m] > 0 and best in dist[m]]
        if not gain:
            break
        chosen[best] = "cover"
        for m in gain:
            need[m] -= 1
    strata = {}
    for i, s in enumerate(sc, 1):
        strata.setdefault(stratum(s), []).append(i)
    for k in sorted(strata):
        idx = strata[k]
        for i in sorted(rng.sample(idx, max(1, round(FRACTION * len(idx))))):
            chosen.setdefault(i, "sample")
    rows = []
    for i in sorted(chosen):
        r = dict(sc[i - 1])
        r["idx"], r["why"] = i, chosen[i]
        rows.append(r)
    write_tsv(os.path.join(out, "selected.tsv"), rows, extra=("idx", "why"))
    print("distinguishable", sum(1 for s in dist.values() if s), "equivalent", sorted(m for m, s in dist.items() if not s))
    print("selected", len(rows), {k: sum(1 for r in rows if r["fam"] == k) for k in "POSC"},
          "cover", sum(1 for r in rows if r["why"] == "cover"))


HEAD = """<!doctype html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>gen2 %s</title>
<script src=/resources/testharness.js></script>
<script src=/resources/testharnessreport.js></script>
<script src=/common/get-host-info.sub.js></script>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<script src=/html/cross-origin-opener-policy/resources/popup-test.js></script>
<script src=resources/gobs2.js></script>
<body>
<script>
const HOSTS = {a: "{{host}}", a1: "{{hosts[][www1]}}", b: "{{hosts[alt][]}}", b1: "{{hosts[alt][www1]}}"};
const PORTS = {http: {{ports[http][0]}}, https: {{ports[https][0]}}};
const SCEN = %s;
%s(SCEN);
</script>
"""


def js(o):
    import json
    return json.dumps(o, separators=(",", ":"))


def cmd_tests(out):
    sel = read_tsv(os.path.join(out, "selected.tsv"))
    t = os.path.join(out, "tests")
    os.makedirs(t, exist_ok=True)
    files = {}
    for s in sel:
        f = s["fam"]
        if f == "P":
            name, hdr = "popup-%s.https.sub.html" % AB[s["oc"]], {"Cross-Origin-Opener-Policy": s["oc"]}
            sch, h = POP_REL[s["rel"]]
            item = {"id": s["sid"], "s": sch, "h": h, "pc": s["pc"], "mode": s["mode"]}
            runner = "runPopup"
        elif f == "O":
            name, hdr = "oac.https.sub.html", {}
            item = {"id": s["sid"], "s": "http" if s["top"] == "http" else "https",
                    "coi": s["top"] == "https-coi", "h": [s["h0"], s["h1"], s["h2"]]}
            runner = "runOAC"
        elif f == "S":
            name = "sb-%s-%s.https.sub.html" % (AB[s["te"]], AB[s["tc"]])
            hdr = {"Cross-Origin-Embedder-Policy": s["te"], "Cross-Origin-Opener-Policy": s["tc"]}
            ch = REL[s["rel"]]
            item = {"id": s["sid"], "sb": s["sb"], "h": ch, "o": other(ch), "coep": s["ce"], "corp": s["corp"]}
            runner = "runSandbox"
        else:
            name = "corp-%s-%s%s.sub.html" % (s["ts"], AB[s["te"]], ".https" if s["ts"] == "https" else "")
            hdr = {"Cross-Origin-Embedder-Policy": s["te"]}
            item = {"id": s["sid"], "h": REL[s["rel"]], "rs": s["rs"], "corp": s["corp"], "dest": s["dest"]}
            runner = "runCorp"
        e = files.setdefault(name, {"hdr": hdr, "runner": runner, "items": []})
        e["items"].append(item)
    for name, e in sorted(files.items()):
        with open(os.path.join(t, name), "w", encoding="utf-8") as f:
            f.write(HEAD % (name, "[\n" + ",\n".join(js(i) for i in e["items"]) + "]", e["runner"]))
        lines = ["%s: %s" % (k, v) for k, v in e["hdr"].items() if v != "unsafe-none"]
        if lines:
            with open(os.path.join(t, name + ".headers"), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
    print({k: len(v["items"]) for k, v in sorted(files.items())})


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "space":
        cmd_space(sys.argv[2])
    elif c == "select":
        cmd_select(sys.argv[2], sys.argv[3])
    elif c == "tests":
        cmd_tests(sys.argv[2])
