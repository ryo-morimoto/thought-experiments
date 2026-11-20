"""Merge two codings and an adjudication into the final coding.

Usage: python3 -I merge_codings.py coderA.tsv coderB.tsv adjudication.tsv final.tsv

For each id: the adjudicated row if there is one; otherwise coder A's row, after checking
that A and B agree on in_scope (the script stops if an unadjudicated disagreement remains).
"""
import csv
import sys


def read(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return reader.fieldnames, {r["id"].strip(): r for r in reader if r.get("id", "").strip()}


fields, a = read(sys.argv[1])
_, b = read(sys.argv[2])
_, adj = read(sys.argv[3])
out = []
for i in sorted(a, key=lambda x: int(x) if x.isdigit() else x):
    if i in adj:
        row = dict(adj[i])
        row["note"] = (row.get("note") or "") + " [adjudicated]"
    else:
        sa = (a[i].get("in_scope") or "").strip().upper()
        sb = (b.get(i, {}).get("in_scope") or "").strip().upper()
        if sa != sb:
            sys.exit(f"unadjudicated in_scope disagreement on {i}")
        row = a[i]
    out.append(row)
with open(sys.argv[4], "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
    w.writeheader()
    w.writerows(out)
print(len(out), "rows")
