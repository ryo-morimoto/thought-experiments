"""Extract observed values from mozlog raw logs into observed.tsv.

usage: python3 -I extract.py <wpt-cases.tsv> <out observed.tsv> <raw.log>...
Log names are <product>-<file>-r<repeat>-raw.log. Subtests are
"OBS <row>[#k] :: <value>" (k = sub-variant, e.g. the 7 bad header values).
Columns: row, browser, value (the single value, or "mixed"), values (all
distinct values, "|"-separated), repeat_consistent (same values in every
repeat), n_obs, note (errors, or "unmapped: <reason>").
"""
import collections
import csv
import json
import re
import sys

cases, out, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
rows = ["w%03d" % i for i in range(1, 1 + sum(1 for _ in open(cases, encoding="utf-8")) - 1)]
vals = collections.defaultdict(lambda: collections.defaultdict(list))  # (b,row) -> rep -> [v]
errs = collections.defaultdict(list)
versions = {}
for path in logs:
    m = re.search(r"([a-z]+)-(.+)-r(\d+)-raw\.log$", path)
    prod, rep = m.group(1), int(m.group(3))
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("action") == "suite_start":
            versions[prod] = e.get("run_info", {}).get("browser_version")
        if e.get("action") != "test_status":
            continue
        s = e["subtest"]
        mm = re.match(r"OBS (w\d{3})(?:#\d+)? :: (.*)$", s)
        if mm:
            v = mm.group(2)
            v = v.upper() if v in ("true", "false") else v
            vals[(prod, mm.group(1))][rep].append(v)
        elif s.startswith("OBS-ERROR"):
            errs[(prod, s.split()[1])].append((e["status"], (e.get("message") or "")[:200]))

with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["row", "browser", "value", "values", "repeat_consistent", "n_obs", "note"])
    for prod in sorted(versions):
        for r in rows:
            reps = vals.get((prod, r), {})
            allv = sorted({v for vs in reps.values() for v in vs})
            note = "; ".join("%s %s" % x for x in errs.get((prod, r), []))
            if not allv:
                w.writerow([r, prod, "unmapped", "", "", 0, note or "unmapped: no observation"])
                continue
            per = [tuple(sorted(set(vs))) for _, vs in sorted(reps.items())]
            cons = "yes" if len(set(per)) == 1 and len(per) >= 2 else ("single-run" if len(per) < 2 else "no")
            n = sum(len(vs) for vs in reps.values())
            w.writerow([r, prod, allv[0] if len(allv) == 1 else "mixed", "|".join(allv), cons, n, note])
print("versions:", versions)
