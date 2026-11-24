#!/bin/bash
# Run TLC (podman localhost/veda-tlc:1.8.0) on gen2 cfgs in a scratch copy.
# usage: tlc.sh <dir for TLC outputs> <cfg stem>...
#   Gen2Enum-*   needs Gen2Space.tla (gen2.py space)
#   Gen2Allowed-* needs Gen2Rows.tla (driver/mkrows.py, written into the copy)
set -eu
G=$(cd "$(dirname "$0")/.." && pwd)    # gen2/
J=$1; shift
T=$(mktemp -d)
cp "$G/../SpecIsolation.tla" "$G"/*.tla "$G"/*.cfg "$T/"
if [ -f "$G/observed.tsv" ] && [ -f "$G/selected.tsv" ]; then
  python3 -I "$G/driver/mkrows.py" "$G/space.tsv" "$G/observed.tsv" "$T"
fi
for c in "$@"; do
  m=${c%%-*}
  s=$(date +%s)
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx8g -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st -config "$c.cfg" "$m.tla" > "$J/tlc-$c.out" 2>&1 || true
  echo "== $c ($(( $(date +%s) - s ))s)"
  grep -E 'rror|violated' "$J/tlc-$c.out" | head -5 || true
done
rm -rf "$T"
