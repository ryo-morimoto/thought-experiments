"""Stronger baseline for the pre-registered origin-oracle test: closures from random roots.

Usage: python3 -I baseline_random_roots.py callgraph.json final.tsv

callgraph.json is dumped from the extraction's analyze.py (algorithm id -> name, calls; and the
18 pre-registered roots). For each trial, draw k random roots among all HTML/Fetch algorithms,
take their call-graph closure (plus "window open steps", as in the registered set), and count how
many in-scope bugs in final.tsv have every named spec algorithm inside that closure. Reported
for k = 18 (same number of roots) and k = 1, with 1000 trials each (seed 20261121), together
with the closure sizes, and for a few named single roots.
"""
import csv
import json
import random
import sys

g = json.load(open(sys.argv[1]))
algos = g["algos"]
name = {a: v["name"].strip().lower() for a, v in algos.items()}


def closure(starts):
    seen, stack = set(), list(starts)
    while stack:
        a = stack.pop()
        if a in seen:
            continue
        seen.add(a)
        stack.extend(c for c in algos[a]["calls"] if c in algos and c not in seen)
    return seen


rows = [r for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"), delimiter="\t")
        if (r.get("in_scope") or "").strip().upper() == "Y"]


def needed(r):
    ns = [n.strip().lower() for n in (r.get("spec_algorithms") or "").split(";") if n.strip()]
    return ns if ns and not any(n.startswith("other:") or n == "none" for n in ns) else None


def score(cl):
    names = {name[a] for a in cl} | {"window open steps"}
    return sum(1 for r in rows if needed(r) and all(n in names for n in needed(r)))


registered = closure(g["roots"])
obs = score(registered)
print(f"in-scope bugs: {len(rows)}; registered closure: {len(registered)} algorithms, predicted {obs}/{len(rows)}")
for label, key in [("navigate only", "navigate"), ("main fetch only", "main fetch")]:
    ids = [a for a in algos if name[a] == key]
    if ids:
        cl = closure(ids[:1])
        print(f"{label}: {len(cl)} algorithms, predicted {score(cl)}/{len(rows)}")
pop = sorted(algos)
rng = random.Random(20261121)
for k in (18, 1):
    res = []
    for _ in range(1000):
        cl = closure(rng.sample(pop, k))
        res.append((score(cl), len(cl)))
    scores = sorted(s for s, _ in res)
    sizes = sorted(n for _, n in res)
    ge = sum(1 for s, _ in res if s >= obs) / len(res)
    print(f"k={k}: predicted median={scores[500]}/{len(rows)} 95th={scores[949]} max={scores[-1]}; "
          f"closure size median={sizes[500]} 95th={sizes[949]}; P(random >= {obs})={ge:.3f}")
    big = [s for s, n in res if n >= len(registered) * 0.9]
    if big:
        print(f"  among trials whose closure is at least 90% of the registered size ({len(big)} trials): "
              f"median predicted={sorted(big)[len(big) // 2]}, P(>= {obs})={sum(1 for s in big if s >= obs) / len(big):.3f}")
