#!/bin/bash
# Kill check of BugMutants!All on the four existing observation sets.
# Copies the models into a scratch dir, generates the row modules with the
# existing generators, writes the cfgs and runs TLC (podman
# localhost/veda-tlc:1.8.0). Nothing is written into the repository.
# usage: run.sh <dir for TLC outputs> [observe gen gen2 redirect]
set -eu
B=$(cd "$(dirname "$0")" && pwd)       # bugmut/
D=$(cd "$B/.." && pwd)                 # site-isolation/
J=$1; shift
PIPES=${*:-observe gen gen2 redirect}
mkdir -p "$J"
for p in $PIPES; do
  T=$(mktemp -d)
  cp "$D/SpecIsolation.tla" "$B/BugMutants.tla" "$T/"
  case $p in
    observe)  cp "$D"/observe/*.tla "$B/BugKillObserve.tla" "$T/"
              python3 -I "$D/observe/driver/mkallowed.py" "$D/wpt-cases.tsv" "$D/observe/observed.tsv" "$T" > /dev/null
              M=BugKillObserve ;;
    gen)      cp "$D"/gen/*.tla "$B/BugKillGen.tla" "$T/"
              python3 -I "$D/gen/driver/mkallowed.py" "$D/gen/scenarios.tsv" "$D/gen/observed.tsv" "$T" > /dev/null
              M=BugKillGen ;;
    gen2)     cp "$D"/gen2/*.tla "$B/BugKillGen2.tla" "$T/"
              python3 -I "$D/gen2/driver/mkrows.py" "$D/gen2/space.tsv" "$D/gen2/observed.tsv" "$T" > /dev/null
              M=BugKillGen2 ;;
    redirect) cp "$D"/redirect/*.tla "$B/BugKillRedirect.tla" "$T/"
              python3 -I "$D/redirect/gen.py" space "$T" > /dev/null
              python3 -I "$D/redirect/driver/mkrows.py" "$D/redirect/scenarios.tsv" "$D/redirect/observed.tsv" "$T" > /dev/null
              M=BugKillRedirect ;;
  esac
  for c in both concrete; do
    if [ $c = both ]; then cc='{"concrete", "logical"}'; else cc='{"concrete"}'; fi
    {
      echo "SPECIFICATION Spec"
      echo "CONSTANTS"
      echo "  COIChoices = $cc"
      [ $p = gen ] && echo "  WithPP = TRUE"
      [ $p = gen2 ] && echo '  OACParam = "spec"'
      echo "  CfgName = \"$c\""
      echo "INVARIANTS PrintK"
    } > "$T/$M-$c.cfg"
    s=$(date +%s)
    podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -Xmx${XMX:-3g} -XX:+UseParallelGC \
      -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st -config "$M-$c.cfg" "$M.tla" > "$J/tlc-$p-$c.out" 2>&1 || true
    grep -q "Finished in" "$J/tlc-$p-$c.out" || echo "INCOMPLETE: $p $c (TLC did not finish; rerun)"
    echo "== $p $c ($(( $(date +%s) - s ))s) $(grep -c '^<<"k"' "$J/tlc-$p-$c.out") lines"
    grep -E 'rror|violated' "$J/tlc-$p-$c.out" | head -5 || true
  done
  rm -rf "$T"
done
