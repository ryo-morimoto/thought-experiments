#!/bin/bash
# Host side: run the generated scenarios for one product inside podman.
# usage: run.sh <wpt clone> <log dir> <product>   (env: REP, GLOB, ORIG, TDIR)
D=$(cd "$(dirname "$0")/.." && pwd)    # history/
W=$1; L=$2; p=$3; REP=${REP:-2}; GLOB=${GLOB:-h-*}
mkdir -p "$L"
s=$(date +%s)
timeout 20000 podman run --rm -e PROCS="${PROCS:-1}" -v "$W":/wpt:O -v "${TDIR:-$D/tests}":/tests:Z -v "$D/driver":/driver:Z -v "$L":/logs:Z \
  docker.io/library/python:3.12-bookworm bash /driver/incontainer.sh "$p" "$REP" "$GLOB" "${ORIG:-}" \
  > "$L/run-$p.out" 2>&1
echo "$p: $(( $(date +%s) - s ))s"; tail -4 "$L/run-$p.out"
