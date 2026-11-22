"""Patch a generated AllowedRows.tla so that row w014 (an <img>, mixed
content) uses ImageResult with served = FALSE (no TLS at wptserve's :8000).
usage: python3 -I patch_w014.py <AllowedRows.tla>   (fixes/FIXES.md)"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old = ('[] r = "w014" -> ProjSet({S(m)!FetchResult(OA, "unsafe-none", "no-cors", '
       '[origin |-> OAwwwhttp, corp |-> "same-site", creds |-> FALSE])})')
new = ('[] r = "w014" -> ProjSet({S(m)!ImageResult(OA, "unsafe-none", '
       '[origin |-> OAwwwhttp, corp |-> "same-site", creds |-> FALSE], FALSE)})')
if s.count(old) != 1:
    raise SystemExit("w014 line not found once")
open(p, "w", encoding="utf-8").write(s.replace(old, new))
print("patched w014")
