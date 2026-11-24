"""Extract gen2 observations from mozlog raw logs.

usage: python3 -I extract.py <out observed.tsv> <raw.log>...
Log names are <product>-r<repeat>-raw.log. Subtests are "OBS <sid>.<kind> :: <value>"
and "LATE :: <sids>". Columns: row, browser, value (single value or "mixed"),
values, repeat_consistent, n_obs, note ("partial": not seen in every repeat).
Also prints per-file harness status, LATE lines and browser versions.
"""
import collections
import csv
import json
import re
import sys

out, logs = sys.argv[1], sys.argv[2:]
vals = collections.defaultdict(lambda: collections.defaultdict(list))
reps_of = collections.defaultdict(set)
versions, status, late = collections.defaultdict(set), collections.Counter(), []
for path in logs:
    m = re.search(r"([a-z]+)-r(\d+)-raw\.log$", path)
    prod, rep = m.group(1), int(m.group(2))
    reps_of[prod].add(rep)
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        a = e.get("action")
        if a == "suite_start":
            versions[prod].add(e.get("run_info", {}).get("browser_version"))
        elif a == "test_end":
            status[(prod, rep, e["test"].rsplit("/", 1)[-1], e["status"])] += 1
        elif a == "test_status":
            s = e["subtest"]
            mm = re.match(r"OBS (\S+) :: (.*)$", s)
            if mm:
                v = mm.group(2)
                v = v.upper() if v in ("true", "false") else v
                vals[(prod, mm.group(1))][rep].append(v)
            elif s.startswith("LATE ::") and s != "LATE :: none":
                late.append((prod, rep, e["test"], s))

with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["row", "browser", "value", "values", "repeat_consistent", "n_obs", "note"])
    for (prod, row) in sorted(vals):
        reps = vals[(prod, row)]
        allv = sorted({v for vs in reps.values() for v in vs})
        per = [tuple(sorted(set(vs))) for _, vs in sorted(reps.items())]
        cons = "yes" if len(set(per)) == 1 and len(per) >= 2 else ("single-run" if len(per) < 2 else "no")
        note = "partial" if len(reps) < len(reps_of[prod]) else ""
        w.writerow([row, prod, allv[0] if len(allv) == 1 else "mixed", "|".join(allv), cons,
                    sum(len(v) for v in reps.values()), note])
print("versions:", {k: sorted(v) for k, v in versions.items()})
for k in sorted(status):
    if k[3] != "OK":
        print("status:", k, status[k])
print("non-OK files:", sum(v for k, v in status.items() if k[3] != "OK"), "of", sum(status.values()))
print("late:", late)
