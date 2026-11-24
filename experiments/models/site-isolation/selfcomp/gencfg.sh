#!/bin/sh
# Write the SC-*.cfg files (self-composition runs, N = 3).
# Each line: control policy K mechanism.
set -eu
cd "$(dirname "$0")"
while read -r ctl pol k mech; do
  name="SC-$ctl-$pol-k$k"
  if [ "$mech" = sniffonly ]; then name="$name-sniffonly"; fi
  printf 'SPECIFICATION SCSpec\nCONSTANTS Mutant = "none"\n          N = 3\n          Mech = "%s"\n          K = %s\n          Ctl = "%s"\n          Policy = "%s"\nINVARIANT SCNI\nVIEW scview\nCHECK_DEADLOCK FALSE\n' \
    "$mech" "$k" "$ctl" "$pol" > "$name.cfg"
done <<EOF
none nothing 1 pr
all nothing 1 pr
none fixedverdict 3 pr
ends fixedverdict 3 pr
all fixedverdict 3 pr
none sniffparse 3 pr
all sniffparse 3 pr
all kernel 3 pr
ends kernel 3 pr
all nothing 3 sniffonly
EOF
