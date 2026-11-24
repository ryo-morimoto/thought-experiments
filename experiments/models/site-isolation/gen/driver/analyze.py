"""Summaries for gen/RESULTS.md from scenarios.tsv, observed.tsv and a TLC output.

usage: python3 -I analyze.py <scenarios.tsv> <observed.tsv> <tlc-GenAllowed*.out>
Prints: coverage per axis value (scenarios run, scenarios whose level 1 loaded
per browser), repeat consistency, and the out-of-model rows grouped by
(browser, level, kind, observed, allowed) with the axis values they share.
"""
import collections
import csv
import re
import sys

scen_tsv, obs_tsv, tlc = sys.argv[1:4]
scen = {}
with open(scen_tsv, encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        scen[r["sid"]] = r
obs = collections.defaultdict(dict)
cons = collections.Counter()
with open(obs_tsv, encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        obs[r["browser"]][r["row"]] = r
        if not r["row"].endswith(".onload"):
            cons[(r["browser"], r["repeat_consistent"], r["note"])] += 1
print("repeat consistency:", dict(cons))


def axes(sid):
    r = scen[sid]
    a = {"depth": r["depth"], "top": "%s/%s/%s" % (r["top_scheme"], r["top_coep"], r["top_coop"])}
    for i, c in enumerate(("l1", "l2"), 1):
        if r[c]:
            s, rel, h, coep, corp = r[c].split("/")
            a.update({"L%d.scheme" % i: s, "L%d.rel" % i: rel, "L%d.coep" % i: coep, "L%d.corp" % i: corp})
    return a


cov = collections.defaultdict(collections.Counter)
for sid in scen:
    for k, v in axes(sid).items():
        cov[(k, v)]["run"] += 1
        for b in obs:
            if sid.startswith("T-") or obs[b].get(sid + ".1.load", {}).get("value") == "loaded":
                cov[(k, v)]["L1-loaded-" + b] += 1
print("coverage per axis value (scenarios; with level 1 loaded per browser):")
for (k, v), c in sorted(cov.items()):
    print("  %-10s %-34s %s" % (k, v, dict(c)))

text = re.sub(r"\s+", " ", open(tlc, encoding="utf-8").read())
groups = collections.defaultdict(list)
for b, body in re.findall(r'<< ?"out-of-model", "(\w+)", \{(.*?)\} >>(?= ?<<)', text):
    for rid, o, a in re.findall(r'<< ?"([^"]+)", \{([^}]*)\}, \{([^}]*)\} ?>>', body):
        sid, lvl, kind = rid.rsplit(".", 2)
        groups[(b, lvl, kind, o.replace('"', "").strip(), a.replace('"', "").strip())].append(sid)
print("out-of-model groups:")
for g, sids in sorted(groups.items()):
    common = None
    for sid in sids:
        s = set(axes(sid).items())
        common = s if common is None else common & s
    print("  %s n=%d common=%s e.g. %s" % (g, len(sids), sorted(common), sids[:3]))
