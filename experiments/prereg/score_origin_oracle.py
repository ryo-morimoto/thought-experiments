"""Score the pre-registered origin-oracle test (experiments/prereg/2026-11-21-origin-oracle.md).

Usage:
  python3 -I score_origin_oracle.py coderA.tsv coderB.tsv oracle-set.txt population.txt [final.tsv]

coder*.tsv columns: id, in_scope (Y/N), scope_reason, wrong_value, spec_algorithms
(semicolon-separated names, NONE, or OTHER:<spec>:<name>), test_time (Y/N/NA), confidence, note.
final.tsv (optional) has the same columns and holds the adjudicated row for each id.

Rule step 3 ("predicted"): the bug is in scope and every named spec algorithm is in the oracle set.
Baseline: the same test with 1000 random sets of algorithms of the oracle set's size, drawn
from the population (fixed seed 20261121).
"""
import csv
import random
import sys


def read(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    return {r["id"].strip(): r for r in rows if r.get("id", "").strip()}


def names(row):
    raw = (row.get("spec_algorithms") or "").strip()
    if not raw or raw.upper() == "NONE":
        return None
    return [n.strip().lower() for n in raw.split(";") if n.strip()]


def predicted(row, oracle):
    if (row.get("in_scope") or "").strip().upper() != "Y":
        return False
    ns = names(row)
    if not ns or any(n.startswith("other:") for n in ns):
        return False
    return all(n in oracle for n in ns)


def kappa(a, b):
    ids = sorted(set(a) & set(b))
    pairs = [((a[i].get("in_scope") or "").strip().upper(), (b[i].get("in_scope") or "").strip().upper()) for i in ids]
    n = len(pairs)
    if n == 0:
        return float("nan"), 0
    po = sum(x == y for x, y in pairs) / n
    labels = {x for p in pairs for x in p}
    pe = sum((sum(x == l for x, _ in pairs) / n) * (sum(y == l for _, y in pairs) / n) for l in labels)
    return ((po - pe) / (1 - pe) if pe < 1 else 1.0), n


def summary(label, rows, oracle, population, size):
    scope = [r for r in rows.values() if (r.get("in_scope") or "").strip().upper() == "Y"]
    named = [r for r in scope if names(r) and not any(n.startswith("other:") for n in names(r))]
    hit = [r for r in scope if predicted(r, oracle)]
    tt = [r for r in hit if (r.get("test_time") or "").strip().upper() == "Y"]
    rng = random.Random(20261121)
    pop = sorted(population)
    rates = []
    for _ in range(1000):
        s = set(rng.sample(pop, size))
        rates.append(sum(all(n in s for n in names(r)) for r in named) / len(scope) if scope else 0)
    rates.sort()
    real = len(hit) / len(scope) if scope else 0
    p_ge = sum(x >= real for x in rates) / len(rates)
    print(f"[{label}] candidates={len(rows)} in_scope={len(scope)} spec-named(HTML/Fetch)={len(named)} "
          f"NONE={sum(1 for r in scope if names(r) is None)} OTHER-spec={sum(1 for r in scope if names(r) and any(n.startswith('other:') for n in names(r)))}")
    print(f"[{label}] predicted={len(hit)}/{len(scope)} ({real:.0%}); predicted and test-time={len(tt)}/{len(scope)}")
    print(f"[{label}] random-set baseline: median={rates[500]:.0%} 95th={rates[949]:.0%} max={rates[-1]:.0%}; "
          f"P(random >= observed)={p_ge:.3f}")
    print(f"[{label}] predicted ids: {sorted(r['id'] for r in hit)}")


def main():
    a, b = read(sys.argv[1]), read(sys.argv[2])
    oracle = {l.strip().lower() for l in open(sys.argv[3], encoding="utf-8") if l.strip()}
    population = {l.strip().lower() for l in open(sys.argv[4], encoding="utf-8") if l.strip()}
    k, n = kappa(a, b)
    print(f"Cohen's kappa on in_scope over {n} shared ids: {k:.2f}")
    disagree = sorted(i for i in set(a) & set(b)
                      if (a[i].get("in_scope") or "").strip().upper() != (b[i].get("in_scope") or "").strip().upper())
    print("in_scope disagreements:", disagree)
    both_scope = [i for i in set(a) & set(b) if (a[i].get("in_scope") or "").strip().upper() == "Y" == (b[i].get("in_scope") or "").strip().upper()]
    pa = {i for i in both_scope if predicted(a[i], oracle)}
    pb = {i for i in both_scope if predicted(b[i], oracle)}
    print(f"both in scope: {len(both_scope)}; predicted by A's naming {len(pa)}, by B's {len(pb)}, by both {len(pa & pb)}")
    summary("A", a, oracle, population, len(oracle))
    summary("B", b, oracle, population, len(oracle))
    if len(sys.argv) > 5:
        summary("final", read(sys.argv[5]), oracle, population, len(oracle))


main()
