"""Assemble the bug list by the fixed rule: up to 25 from A (prereg table, filtered, table order),
then NVD round-robin over keywords (ascending sha256 within keyword), dedupe, cap 60.
usage: python3 -I assemble.py <candidates-table.md> <filtered.json> <out.tsv>"""
import json, sys, re
tab, filt, outp = sys.argv[1:4]
KA = re.compile(r"site isolation|sandbox|opener|popup|redirect|coop|coep|corp|origin", re.I)
A = []
for line in open(tab):
    if not re.match(r"\| \d+ \|", line):
        continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    num, ids, br, fixed, comp, wrong = c[0], c[1], c[2], c[3], c[4], c[5]
    if KA.search(comp + " " + wrong):
        A.append(("A", num, ids, br, fixed, comp + " / " + wrong))
nA = len(A)
A = A[:25]
seen = set()
def cves(s):
    return set(re.findall(r"CVE-\d{4}-\d+", s))
for a in A:
    seen |= cves(a[2])
F = json.load(open(filt))
names = [k for k in F if F[k]]
lists = [F[k] for k in names]
B, idx = [], [0] * len(lists)
while len(A) + len(B) < 60 and any(idx[j] < len(lists[j]) for j in range(len(lists))):
    for j, L in enumerate(lists):
        if len(A) + len(B) >= 60:
            break
        while idx[j] < len(L) and L[idx[j]][1] in seen:
            idx[j] += 1
        if idx[j] < len(L):
            _, cid, pub, desc, refs = L[idx[j]]
            idx[j] += 1
            seen.add(cid)
            B.append(("B", names[j], cid, pub, desc, " ".join(refs)))
with open(outp, "w") as f:
    for a in A:
        f.write("\t".join(a) + "\n")
    for b in B:
        f.write("\t".join(b) + "\n")
print("A matched", nA, "taken", len(A), "B", len(B))
