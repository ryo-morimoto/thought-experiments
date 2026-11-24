#!/bin/bash
# Generate GenRows.tla from scenarios.tsv + observed.tsv into a scratch dir and
# run TLC (podman localhost/veda-tlc:1.8.0) on the given cfgs.
# usage: check.sh <dir for TLC outputs> [cfg...]   (default: the three GenAllowed cfgs)
set -eu
G=$(cd "$(dirname "$0")/.." && pwd)    # gen/
J=$1; shift
CFGS=${*:-GenAllowed GenAllowed-concrete GenAllowed-noPP}
T=$(mktemp -d)
cp "$G/../SpecIsolation.tla" "$G"/*.tla "$G"/*.cfg "$T/"
python3 -I "$G/driver/mkallowed.py" "$G/scenarios.tsv" "$G/observed.tsv" "$T"
for c in $CFGS; do
  m=GenAllowed; case $c in GenEnum*) m=GenEnum;; esac
  s=$(date +%s)
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx8g -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st -config "$c.cfg" $m.tla > "$J/tlc-$c.out" 2>&1 || true
  echo "== $c ($(( $(date +%s) - s ))s)"
  grep -E '^<<|rror|violated' "$J/tlc-$c.out" | grep -v '"out-of-model"' | cut -c1-2500
done
rm -rf "$T"
