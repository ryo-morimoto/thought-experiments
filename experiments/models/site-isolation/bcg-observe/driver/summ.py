"""Summarise mozlog raw logs from bcg-observe runs.
usage: python3 -I summ.py <raw.log> [...]
Prints, per file, each repetition's verdict (noswap/SWAP/other) plus key observations."""
import json, sys, re, collections

for path in sys.argv[1:]:
    prod = None
    rows = collections.defaultdict(list)   # test -> [(verdict, obs)]
    cur = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("action") == "suite_start":
            ri = e.get("run_info", {})
            prod = f'{ri.get("product")} {ri.get("browser_version")}'
        if e.get("action") == "test_start":
            cur[e["test"]] = {"verdict": None, "obs": None}
        if e.get("action") == "test_status":
            c = cur.setdefault(e["test"], {"verdict": None, "obs": None})
            msg = e.get("message") or ""
            if "same BCG" in e["subtest"]:
                c["verdict"] = {"PASS": "noswap"}.get(e["status"],
                    "SWAP" if "SWAP-OBSERVED" in msg else e["status"] + ":" + msg[:600])
            if "observations" in e["subtest"]:
                m = re.search(r"OBS (\{.*\})", msg)
                c["obs"] = json.loads(m.group(1)) if m else msg[:200]
        if e.get("action") == "test_end":
            c = cur.pop(e["test"], {"verdict": None, "obs": None})
            if c["verdict"] is None:
                c["verdict"] = "harness:" + e.get("status", "?") + ":" + (e.get("message") or "")[:120]
            rows[e["test"]].append((c["verdict"], c["obs"]))
    print("==", path, "|", prod)
    for t in sorted(rows):
        verdicts = [v for v, _ in rows[t]]
        print(t.split("/")[-1], "->", collections.Counter(verdicts))
        for v, o in rows[t]:
            if isinstance(o, dict):
                b, a, p, af = o.get("before", {}), o.get("atB", {}), o.get("fromP", {}), o.get("after", {})
                print("   ", v, "| name A/B/back:", repr(b.get("name")), repr(a.get("name")), repr(af.get("name")),
                      "| hlen:", b.get("hlen"), a.get("hlen"), af.get("hlen"),
                      "| ss:", af.get("ss"), "| bfcache:", af.get("bfcacheRestored"),
                      "| P.opener:", p)
            else:
                print("   ", v, "|", o)
