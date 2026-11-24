#!/bin/bash
# Pre-screen (HistoryEnum) over the whole space in P parallel index ranges.
# Writes <out>/tlc-enum-<k>.out; gen.py select merges them.
# usage: enum.sh <out dir> [P]
set -eu
D=$(cd "$(dirname "$0")/.." && pwd)    # history/
J=$1; P=${2:-3}
T=$(mktemp -d)
cp "$D/../SpecIsolation.tla" "$D"/*.tla "$T/"
N=$(python3 -I "$D/gen.py" space "$T" | awk '{print $2}')
step=$(( (N + P - 1) / P ))
for k in $(seq 1 "$P"); do
  lo=$(( (k - 1) * step + 1 )); hi=$(( k * step ))
  printf 'SPECIFICATION Spec\nCONSTANTS\n  Lo = %d\n  Hi = %d\nINVARIANTS PrintEnum PrintProps\n' $lo $hi > "$T/E$k.cfg"
  ( s=$(date +%s)
    podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx2500m -XX:+UseParallelGC \
      -cp /opt/tla2tools.jar tlc2.TLC -workers 1 -metadir /tmp/st$k -config "E$k.cfg" HistoryEnum.tla \
      > "$J/tlc-enum-$k.out" 2>&1 || true
    echo "range $k ($lo..$hi): $(( $(date +%s) - s ))s" ) &
done
wait
rm -rf "$T"
