#!/bin/bash
# fixes/FIXES.md: rerun the inclusion check (observe/) against the fixed model.
# usage: bash fixes/check.sh <dir for TLC outputs>     (from site-isolation/)
# Generates AllowedRows.tla / Observed.tla into a scratch dir (observe/ is
# left untouched), patches w014 to the <img> operator, and runs TLC there.
set -eu
D=$(cd "$(dirname "$0")/.." && pwd)    # site-isolation/
J=$1
T=$(mktemp -d)
cp "$D/SpecIsolation.tla" "$D/observe/AllowedSets.tla" "$D/fixes/AllowedSetsFix.tla" "$D"/fixes/AllowedSetsFix*.cfg "$T/"
python3 -I "$D/observe/driver/mkallowed.py" "$D/wpt-cases.tsv" "$D/observe/observed.tsv" "$T"
python3 -I "$D/fixes/patch_w014.py" "$T/AllowedRows.tla"
for c in AllowedSetsFix AllowedSetsFix-both AllowedSetsFix-expected; do
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st -config "$c.cfg" AllowedSetsFix.tla > "$J/tlc-$c.out" 2>&1
  echo "== $c"
  tr -s ' \n' ' ' < "$J/tlc-$c.out" | grep -o '<< "fix-[a-z]*".*\|rror[^.]*' | sed 's/<< "fix-/\n<< "fix-/g' | grep -v '^$' | cut -c1-1500
done
rm -rf "$T"
