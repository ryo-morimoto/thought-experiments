#!/bin/bash
# K_prev of the registration: kill sets of the registered mutant sets on the
# committed rows of gen/, gen2/ and redirect/ (their own row writers, unedited).
# usage: prev.sh <out dir>      -> <out>/prev-<Module>-<cfg>.out
set -eu
D=$(cd "$(dirname "$0")/.." && pwd)    # holdout/
S=$(cd "$D/.." && pwd)                 # site-isolation/
J=$1
T=$(mktemp -d)
cp "$S/SpecIsolation.tla" "$S/gen/GenModel.tla" "$S/gen2/Gen2Model.tla" "$S/gen2/Gen2Space.tla" \
   "$S/redirect/RedirectSeq.tla" "$D"/HoldMutants.tla "$D"/HoldPrev*.tla "$D"/HoldPrev*.cfg "$T/"
python3 -I "$S/gen/driver/mkallowed.py" "$S/gen/scenarios.tsv" "$S/gen/observed.tsv" "$T"
python3 -I "$S/gen2/driver/mkrows.py" "$S/gen2/space.tsv" "$S/gen2/observed.tsv" "$T"
python3 -I "$S/redirect/gen.py" space "$T" > /dev/null
python3 -I "$S/redirect/driver/mkrows.py" "$S/redirect/scenarios.tsv" "$S/redirect/observed.tsv" "$T"
for m in HoldPrev HoldPrevGen2 HoldPrevRedir; do
  for c in both concrete; do
    s=$(date +%s)
    podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx3g -XX:+UseParallelGC \
      -cp /opt/tla2tools.jar tlc2.TLC -workers 1 -metadir /tmp/st -config "$m-$c.cfg" "$m.tla" \
      > "$J/prev-$m-$c.out" 2>&1 || true
    echo "== $m-$c ($(( $(date +%s) - s ))s)"; grep -E 'Error' "$J/prev-$m-$c.out" | head -3 || true
  done
done
rm -rf "$T"
