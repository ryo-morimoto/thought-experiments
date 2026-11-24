#!/bin/bash
# Host side: run the holdout tests for one product inside podman.
# usage: run.sh <wpt clone> <log dir> <product> [tests dir]   (env: REP, GLOB)
D=$(cd "$(dirname "$0")/.." && pwd)    # holdout/
W=$1; L=$2; p=$3; TD=${4:-$D/tests}; REP=${REP:-2}; GLOB=${GLOB:-*}
mkdir -p "$L"
s=$(date +%s)
timeout 14000 podman run --rm -v "$W":/wpt:O -v "$TD":/tests:Z -v "$D/driver":/driver:Z -v "$L":/logs:Z \
  docker.io/library/python:3.12-bookworm bash /driver/incontainer.sh "$p" "$REP" "$GLOB" \
  > "$L/run-$p.out" 2>&1
echo "$p: $(( $(date +%s) - s ))s"; tail -4 "$L/run-$p.out"
