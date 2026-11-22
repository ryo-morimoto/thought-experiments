#!/bin/bash
# Regenerate AllowedRows.tla / Observed.tla and run the three AllowedSets cfgs.
# usage: check.sh <dir for TLC outputs>
set -u
H=$(cd "$(dirname "$0")/.." && pwd)    # observe/
J=$1
cd "$H"
python3 -I driver/mkallowed.py ../wpt-cases.tsv observed.tsv .
for c in AllowedSets AllowedSets-concrete AllowedSets-logical AllowedSets-expected; do
  bash driver/tlc.sh $c.cfg "$J/tlc-$c.out" > /dev/null
  echo "== $c"
  tr -s ' \n' ' ' < "$J/tlc-$c.out" | grep -o '<< "counts"[^>]*>>\|<<"survived-nonequivalent"[^>]*>>\|"out-of-model", "[a-z]*", {[^}]*}\|rror[^.]*\|No error has been found'
done
