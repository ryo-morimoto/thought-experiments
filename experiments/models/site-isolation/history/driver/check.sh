#!/bin/bash
# Copy the modules into a scratch dir, generate HistorySpace.tla (and, if
# observed.tsv exists, HistoryRows.tla), and run TLC (podman
# localhost/veda-tlc:1.8.0) on the given cfgs. As redirect/driver/check.sh.
# usage: check.sh <dir for TLC outputs> cfg...
set -eu
D=$(cd "$(dirname "$0")/.." && pwd)    # history/
J=$1; shift
T=$(mktemp -d)
cp "$D/../SpecIsolation.tla" "$D"/*.tla "$D"/*.cfg "$T/"
python3 -I "$D/gen.py" space "$T" > /dev/null
[ -f "$D/observed.tsv" ] && python3 -I "$D/driver/mkrows.py" "$D/scenarios.tsv" "$D/observed.tsv" "$T"
for c in "$@"; do
  m=${c%%-*}
  s=$(date +%s)
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx${XMX:-6g} -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -workers 2 -metadir /tmp/st -config "$c.cfg" $m.tla > "$J/tlc-$c.out" 2>&1 || true
  echo "== $c ($(( $(date +%s) - s ))s)"
  grep -E '^<<|rror|violated|states generated|No error' "$J/tlc-$c.out" | grep -v '"class"' | cut -c1-3000
done
rm -rf "$T"
