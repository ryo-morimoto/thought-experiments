#!/bin/bash
# Run TLC (podman localhost/veda-tlc:1.8.0) for the holdout. Copies the frozen
# modules (../SpecIsolation.tla, ../gen/GenModel.tla, ../redirect/RedirectSeq.tla)
# and this directory's modules into a scratch dir, writes HoldSpace.tla
# (gen_holdout.py space) and, if observed.tsv exists, HoldRows.tla.
# usage: tlc.sh <out dir> enum <Fam> <Lo> <Hi>     pre-screen chunk -> <out>/enum-<Fam>-<Lo>.out
#        tlc.sh <out dir> allowed <cfg>...         HoldAllowed cfgs -> <out>/tlc-<cfg>.out
set -eu
D=$(cd "$(dirname "$0")/.." && pwd)    # holdout/
S=$(cd "$D/.." && pwd)                 # site-isolation/
J=$1; mode=$2; shift 2
T=$(mktemp -d)
cp "$S/SpecIsolation.tla" "$S/gen/GenModel.tla" "$S/redirect/RedirectSeq.tla" "$D"/*.tla "$D"/*.cfg "$T/"
python3 -I "$D/gen_holdout.py" space "$T" > "$T/space.log"
run() {  # cfg module out
  podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx3g -XX:+UseParallelGC \
    -cp /opt/tla2tools.jar tlc2.TLC -workers 1 -metadir /tmp/st -config "$1.cfg" "$2.tla" > "$3" 2>&1 || true
}
if [ "$mode" = enum ]; then
  c=enum-$1-$2
  printf 'SPECIFICATION Spec\nCONSTANTS\n  Fam = "%s"\n  Lo = %s\n  Hi = %s\nINVARIANTS PrintEnum\n' "$1" "$2" "$3" > "$T/$c.cfg"
  s=$(date +%s); run "$c" HoldEnum "$J/$c.out"
  echo "== $c ($(( $(date +%s) - s ))s)"; grep -E '"enum"|Error' "$J/$c.out" | head -3
else
  python3 -I "$D/driver/mkrows.py" "$D" "$T"
  for c in "$@"; do
    s=$(date +%s); run "$c" HoldAllowed "$J/tlc-$c.out"
    echo "== $c ($(( $(date +%s) - s ))s)"; grep -E '"counts"|Error' "$J/tlc-$c.out" | head -6
  done
fi
rm -rf "$T"
