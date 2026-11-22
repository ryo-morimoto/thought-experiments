#!/usr/bin/env python3
"""Baselines for the havoc experiment (experiments/2026-11-23-havoc-unmodeled-steps.md).

    python3 -I baseline.py writesets.tsv <number of closure steps>

Breaking points per property come from Singles-none (TLC, see RESULTS.md).
Sets.cfg checked that the union of the non-breaking points holds for each
property, so by monotonicity a havoc set breaks a property iff it contains a
singly-breaking point; the probabilities below are therefore exact
(hypergeometric), not sampled.
"""
import csv
import sys
from math import comb

TYPEWIDE = ["h-ecoep-inherit", "h-secure", "h-creds-mode", "h-coop", "h-respurl",
            "h-coimode", "h-sw", "h-coicap", "h-ecoep-insecure", "h-creds-cl",
            "h-tainting", "h-mode", "h-coicap-mono", "h-reqorigin", "h-reqorigin-any"]
BREAKS = {  # from Singles-none, Omit = "none"
    "OptInOnlySecure": {"h-ecoep-inherit", "h-secure", "h-respurl", "h-sw",
                        "h-tainting", "h-reqorigin-any"},
    "COIOptIn": {"h-ecoep-inherit", "h-coop", "h-respurl", "h-coimode", "h-sw",
                 "h-coicap", "h-tainting", "h-reqorigin-any"},
}
UNMODELED_POINTS = 8   # 7 unmodeled + h-coicap (boundary)


def p_hit(pop, good, k):
    """P(a uniform k-subset of pop items contains at least one of good)."""
    return 1 - comb(pop - good, k) / comb(pop, k)


def main(ws_path, nsteps):
    rows = list(csv.DictReader(open(ws_path, encoding="utf-8"), delimiter="\t"))
    unmod = [r for r in rows if r["status"] == "unmodeled"]
    n = len(unmod)
    read = {"coep", "coop", "corp", "creds", "secure", "origin", "akey", "coimode",
            "coicap", "tainting", "mode", "bcgswitch", "response"}
    pools = {
        "all closure steps": nsteps,
        "write rows": len(rows),
        "rows writing model-read concepts": sum(1 for r in rows if r["concept"] in read),
    }
    print(f"unmodeled write rows: {n}")
    print(f"point level: random {UNMODELED_POINTS}-subsets of {len(TYPEWIDE)} type-wide points")
    for prop, b in BREAKS.items():
        print(f"  {prop}: {len(b)}/{len(TYPEWIDE)} points break singly; "
              f"P(break) = {p_hit(len(TYPEWIDE), len(b), UNMODELED_POINTS):.4f}")
    print(f"step level: random {n}-subsets of steps, each step havocs its row's point")
    for prop, b in BREAKS.items():
        good = sum(1 for r in rows if r["havoc_point"] in b)
        for name, pop in pools.items():
            print(f"  {prop}: {good} rows map to a breaking point; pool {name} ({pop}): "
                  f"P(break) = {p_hit(pop, good, n):.4f}")
        real = sum(1 for r in unmod if r["havoc_point"] in b)
        print(f"  {prop}: real unmodeled set: {real}/{n} rows map to a breaking point")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
