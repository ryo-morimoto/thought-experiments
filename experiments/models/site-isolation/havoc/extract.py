#!/usr/bin/env python3
"""Keep only this module's PrintT blocks ("havoc-...") and TLC errors from
TLC output on stdin. A block runs from a line starting with '<< "havoc-' to
the next line at column 0."""
import sys

keep = False
for line in sys.stdin:
    if not line.startswith(" "):
        keep = line.startswith('<< "havoc-') or line.startswith('<<"havoc-')
        if not keep and ("Error" in line or "Exception" in line or "line " in line
                         or line.startswith("Finished") or line.startswith("==")):
            print(line, end="")
    if keep:
        print(line, end="")
