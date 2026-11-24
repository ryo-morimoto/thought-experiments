#!/bin/bash
# Run TLC (podman localhost/veda-tlc:1.8.0, -Xmx2g) on gen3 cfgs in a scratch copy.
# usage: tlc.sh <dir for TLC outputs> <cfg stem>...
#   Gen3Enum-*    needs Gen3Space.tla and the cfgs (gen3.py space)
#   Gen3Allowed-* needs observed.tsv (driver/mkrows.py writes Gen3Rows.tla into the copy)
set -eu
G=$(cd "$(dirname "$0")/.." && pwd)    # gen3/
J=$1; shift
mkdir -p "$J"
T=$(mktemp -d)
cp "$G/../SpecIsolation.tla" "$G"/*.tla "$G"/*.cfg "$T/"
if [ -f "$G/observed.tsv" ]; then
  python3 -I "$G/driver/mkrows.py" "$G/space.tsv" "$G/observed.tsv" "$T"
fi
for c in "$@"; do
  m=${c%%-*}
  s=$(date +%s)
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx2g -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -workers 1 -metadir /tmp/st -config "$c.cfg" "$m.tla" > "$J/tlc-$c.out" 2>&1 || true
  grep -q "Finished in" "$J/tlc-$c.out" || echo "INCOMPLETE: $c"
  echo "== $c ($(( $(date +%s) - s ))s)"
  grep -E 'rror|violated' "$J/tlc-$c.out" | head -5 || true
done
rm -rf "$T"
