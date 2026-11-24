"""Scenario generator for the bug-derived axes of tree node C11 (gen3/RESULTS.md).

usage:
  python3 -I gen3.py space <out dir>              full space -> space.tsv, Gen3Space.tla, cfgs
  python3 -I gen3.py select <out dir> <enum outs> pick scenarios -> selected.tsv
  python3 -I gen3.py tests <out dir>              tests/ for selected.tsv

Families (sid = family letter + index). The top page is https a in all.
  X  sandboxed frame calls window.open: sandbox {none, s, s p, s p e, s p so,
     s p e so, s so} x frame host {a, b} x popup host {a, b}              = 28
  Y  sandboxed frame sets top.location (top is a popup): sandbox {none, s,
     s t, s tu, s t tu, s so t, s p} x frame host {a, b}                  = 14
  R  fetch() through redirects: {cors, no-cors} x {GET, POST} x
     referrerPolicy {"", no-referrer, same-origin, unsafe-url} x URL list
     (1-3 URLs over {a, a1, b}) x Referrer-Policy of the first redirect
     {none, no-referrer, unsafe-url}                                      = 1776
  K  <img> through redirects in a document with CSP img-src 'self' [+ a1 | b]:
     URL list (1-3 URLs) x extra source {none, a1, b}                     = 117
  D  document.domain: child host {a, a1, b} x who sets {none, p, c, both} x
     child sandbox "allow-scripts allow-same-origin" {no, yes}            = 24
  N  Window reuse: target {a, a1, b} x creator document.domain {none, before
     creating the about:blank, after} x {iframe src after insertion, iframe
     src at insertion, window.open}                                       = 27
  W  workers: owner (COOP, COEP) {(un,un), (so,rc), (so,cl), (un,rc)} x
     {dedicated, shared} x script COEP {un, rc, cl}, or blob: dedicated   = 28
  F  cross-origin cors fetch(): COEP {un, rc, cl} x target {a1, b} x
     ACAO {none, *, origin, origin + ACAC} x credentials {omit,
     same-origin, include} x CORP {none, same-origin, cross-origin}       = 216
Hosts: a = web-platform.test, a1 = www1., b = not-web-platform.test.
s = allow-scripts, p = allow-popups, e = allow-popups-to-escape-sandbox,
so = allow-same-origin, t = allow-top-navigation, tu = ...-by-user-activation.
"""
import csv
import itertools
import json
import os
import random
import re
import sys

SEED, MIN_COVER = 20261124, 2
FRACTION = {"R": 0.25, "F": 0.40}       # other families are run whole
TOK = {"s": "allow-scripts", "p": "allow-popups", "e": "allow-popups-to-escape-sandbox",
       "so": "allow-same-origin", "t": "allow-top-navigation",
       "tu": "allow-top-navigation-by-user-activation"}
X_SB = ["none", "s", "s-p", "s-p-e", "s-p-so", "s-p-e-so", "s-so"]
Y_SB = ["none", "s", "s-t", "s-tu", "s-t-tu", "s-so-t", "s-p"]
HOSTS3 = ["a", "a1", "b"]
AB = {"unsafe-none": "un", "require-corp": "rc", "credentialless": "cl", "same-origin": "so"}
OWNERS = [("unsafe-none", "unsafe-none"), ("same-origin", "require-corp"),
          ("same-origin", "credentialless"), ("unsafe-none", "require-corp")]
COEP3 = ["unsafe-none", "require-corp", "credentialless"]


def toks(sb):
    return [] if sb == "none" else [TOK[t] for t in sb.split("-")]


def chains(n_max=3):
    for n in range(1, n_max + 1):
        for c in itertools.product(HOSTS3, repeat=n):
            yield list(c)


def space():
    sc = []
    for sb, fh, ph in itertools.product(X_SB, ["a", "b"], ["a", "b"]):
        sc.append(dict(fam="X", sb=sb, fh=fh, ph=ph))
    for sb, fh in itertools.product(Y_SB, ["a", "b"]):
        sc.append(dict(fam="Y", sb=sb, fh=fh))
    for (mode, meth), rp, ch in itertools.product(
            [("cors", "GET"), ("cors", "POST"), ("no-cors", "GET"), ("no-cors", "POST")],
            ["", "no-referrer", "same-origin", "unsafe-url"], chains()):
        for hrp in ([""] if len(ch) == 1 else ["", "no-referrer", "unsafe-url"]):
            sc.append(dict(fam="R", mode=mode, meth=meth, rp=rp, urls="-".join(ch), hrp=hrp))
    for ch, ex in itertools.product(chains(), ["none", "a1", "b"]):
        sc.append(dict(fam="K", urls="-".join(ch), ex=ex))
    for ch, st, csb in itertools.product(HOSTS3, ["none", "p", "c", "both"], ["no", "yes"]):
        sc.append(dict(fam="D", ch=ch, set=st, csb=csb))
    for tgt, dd, how in itertools.product(HOSTS3, ["none", "before", "after"],
                                          ["ifr-after", "ifr-insert", "popup"]):
        sc.append(dict(fam="N", tgt=tgt, dd=dd, how=how))
    for (tc, te) in OWNERS:
        for kind, wc in [(k, c) for k in ("ded", "shared") for c in COEP3] + [("blob", "n/a")]:
            sc.append(dict(fam="W", tc=tc, te=te, kind=kind, wc=wc))
    for te, tg, acao, cred, corp in itertools.product(
            COEP3, ["a1", "b"], ["none", "*", "origin", "origin-acac"],
            ["omit", "same-origin", "include"], ["none", "same-origin", "cross-origin"]):
        sc.append(dict(fam="F", te=te, tg=tg, acao=acao, cred=cred, corp=corp))
    n = {}
    for s in sc:
        n[s["fam"]] = n.get(s["fam"], 0) + 1
        s["sid"] = "%s%04d" % (s["fam"], n[s["fam"]])
    return sc


def stratum(s):
    f = s["fam"]
    if f == "R":
        return ("R", s["mode"], s["meth"], s["rp"])
    if f == "F":
        return ("F", s["te"])
    return (f,)


def org(h):
    return '[scheme |-> "https", host |-> "%s", site |-> "%s"]' % (h, h[0])


def tset(xs):
    return "{" + ", ".join('"%s"' % x for x in xs) + "}"


def tla_record(s):
    f, A = s["fam"], org("a")
    if f == "X":
        return ('[fam |-> "X", to |-> %s, sbon |-> %s, sb |-> %s, fh |-> %s, ph |-> %s]'
                % (A, "FALSE" if s["sb"] == "none" else "TRUE", tset(toks(s["sb"])), org(s["fh"]), org(s["ph"])))
    if f == "Y":
        return ('[fam |-> "Y", to |-> %s, sbon |-> %s, sb |-> %s, fh |-> %s]'
                % (A, "FALSE" if s["sb"] == "none" else "TRUE", tset(toks(s["sb"])), org(s["fh"])))
    if f == "R":
        return ('[fam |-> "R", to |-> %s, mode |-> "%s", meth |-> "%s", rp |-> "%s", hrp |-> "%s", urls |-> <<%s>>]'
                % (A, s["mode"], s["meth"], s["rp"], s["hrp"], ", ".join(org(h) for h in s["urls"].split("-"))))
    if f == "K":
        allow = [A] + ([] if s["ex"] == "none" else [org(s["ex"])])
        return ('[fam |-> "K", to |-> %s, allow |-> {%s}, urls |-> <<%s>>]'
                % (A, ", ".join(allow), ", ".join(org(h) for h in s["urls"].split("-"))))
    if f == "D":
        return ('[fam |-> "D", to |-> %s, ch |-> %s, set |-> "%s", sbon |-> %s, sb |-> %s]'
                % (A, org(s["ch"]), s["set"], "TRUE" if s["csb"] == "yes" else "FALSE",
                   tset(toks("s-so"))))
    if f == "N":
        return ('[fam |-> "N", to |-> %s, tgt |-> %s, dd |-> "%s", how |-> "%s"]'
                % (A, org(s["tgt"]), s["dd"], s["how"]))
    if f == "W":
        return ('[fam |-> "W", to |-> %s, xo |-> %s, tc |-> "%s", te |-> "%s", kind |-> "%s", wc |-> "%s"]'
                % (A, org("b"), s["tc"], s["te"], s["kind"], s["wc"]))
    return ('[fam |-> "F", to |-> %s, te |-> "%s", tg |-> %s, acao |-> "%s", cred |-> "%s", corp |-> "%s"]'
            % (A, s["te"], org(s["tg"]), s["acao"], s["cred"], s["corp"]))


FIELDS = ["sid", "fam", "sb", "fh", "ph", "mode", "meth", "rp", "urls", "hrp", "ex", "ch", "set",
          "csb", "tgt", "dd", "how", "tc", "te", "kind", "wc", "tg", "acao", "cred", "corp"]


def write_tsv(path, rows, extra=()):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS + list(extra), delimiter="\t", lineterminator="\n", restval="")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        return [{k: v for k, v in r.items() if v != "" or (r["fam"] == "R" and k in ("rp", "hrp"))}
                for r in csv.DictReader(f, delimiter="\t")]


CFGS = {"both-may": ('{"concrete", "logical"}', "may"), "concrete-may": ('{"concrete"}', "may"),
        "both-exact": ('{"concrete", "logical"}', "exact"), "concrete-exact": ('{"concrete"}', "exact")}


def write_cfgs(out):
    for name, (cc, rm) in CFGS.items():
        for mod, inv in (("Gen3Enum", "PrintEnum"), ("Gen3Allowed", "PrintGen")):
            with open(os.path.join(out, "%s-%s.cfg" % (mod, name)), "w", encoding="utf-8") as f:
                f.write('SPECIFICATION Spec\nCONSTANTS\n  COIChoices = %s\n  OShare = {"ref", "copy"}\n'
                        '  RefMay = "%s"\n  CfgName = "%s"\nINVARIANTS %s\n' % (cc, rm, name, inv))


def cmd_space(out):
    sc = space()
    write_tsv(os.path.join(out, "space.tsv"), sc)
    with open(os.path.join(out, "Gen3Space.tla"), "w", encoding="utf-8") as f:
        f.write("---- MODULE Gen3Space ----\n(* generated by gen3.py space; do not edit *)\n")
        f.write("Scen == <<\n  " + ",\n  ".join(tla_record(s) for s in sc) + ">>\n====\n")
    write_cfgs(out)
    print("space", len(sc), {k: sum(1 for s in sc if s["fam"] == k) for k in "XYRKDNWF"})


def parse_enum(path):
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
        fr = FRACTION.get(k[0], 1.0)
        for i in sorted(rng.sample(idx, max(1, round(fr * len(idx))))):
            chosen.setdefault(i, "sample" if fr < 1 else "whole")
    rows = []
    for i in sorted(chosen):
        r = dict(sc[i - 1])
        r["idx"], r["why"] = i, chosen[i]
        rows.append(r)
    write_tsv(os.path.join(out, "selected.tsv"), rows, extra=("idx", "why"))
    print("mutants", len(dist), "distinguishable", sum(1 for s in dist.values() if s))
    print("equivalent", sorted(m for m, s in dist.items() if not s))
    print("selected", len(rows), {k: sum(1 for r in rows if r["fam"] == k) for k in "XYRKDNWF"},
          "cover", sum(1 for r in rows if r["why"] == "cover"))


HEAD = """<!doctype html>
<meta charset=utf-8>
<meta name=timeout content=long>
<title>gen3 %s</title>
<script src=/resources/testharness.js></script>
<script src=/resources/testharnessreport.js></script>
<script src=/common/utils.js></script>
<script src=/common/dispatcher/dispatcher.js></script>
<script src=resources/g3.js></script>
<body>
<script>
const HOSTS = {a: "{{host}}", a1: "{{hosts[][www1]}}", b: "{{hosts[alt][]}}"};
const PORT = {{ports[https][0]}};
const SCEN = %s;
%s(SCEN);
</script>
"""


def cmd_tests(out):
    sel = read_tsv(os.path.join(out, "selected.tsv"))
    t = os.path.join(out, "tests")
    os.makedirs(t, exist_ok=True)
    files = {}
    for s in sel:
        f, hdr = s["fam"], {}
        item = {k: s[k] for k in FIELDS if k != "fam" and k in s}
        item["id"] = item.pop("sid")
        if f in "XYRKDN":
            name, runner = "%s.https.sub.html" % f.lower(), "run" + f
        elif f == "W":
            name = "w-%s-%s.https.sub.html" % (AB[s["tc"]], AB[s["te"]])
            hdr = {"Cross-Origin-Opener-Policy": s["tc"], "Cross-Origin-Embedder-Policy": s["te"]}
            runner = "runW"
        else:
            name = "f-%s.https.sub.html" % AB[s["te"]]
            hdr = {"Cross-Origin-Embedder-Policy": s["te"]}
            runner = "runF"
        e = files.setdefault(name, {"hdr": hdr, "runner": runner, "items": []})
        e["items"].append(item)
    for name, e in sorted(files.items()):
        with open(os.path.join(t, name), "w", encoding="utf-8") as f:
            f.write(HEAD % (name, "[\n" + ",\n".join(json.dumps(i, separators=(",", ":"))
                                                     for i in e["items"]) + "]", e["runner"]))
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
