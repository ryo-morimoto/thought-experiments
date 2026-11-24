#!/bin/bash
# Host side: run the gen2 tests for each product inside podman, in parallel.
# usage: run.sh <wpt clone> <log dir>   (env: PRODS, REP, GLOB)
G=$(cd "$(dirname "$0")/.." && pwd)    # gen2/
W=$1; L=$2; REP=${REP:-2}; GLOB=${GLOB:-*}
mkdir -p "$L"
for p in ${PRODS:-chrome firefox}; do
  ( s=$(date +%s)
    timeout 12000 podman run --rm -v "$W":/wpt:O -v "$G/tests":/gen2:Z -v "$G/driver":/driver:Z \
      -v "$L":/logs:Z docker.io/library/python:3.12-bookworm bash /driver/incontainer.sh $p $REP "$GLOB" \
      > "$L/run-$p.out" 2>&1
    echo "$p: $(( $(date +%s) - s ))s" >> "$L/run-$p.out" ) &
done
wait
tail -4 "$L"/run-*.out
