#!/bin/sh
# Run the havoc checks (experiments/2026-11-23-havoc-unmodeled-steps.md).
# Usage: sh havoc/run.sh <cfg name without .cfg> ...   (from site-isolation/)
# Prints only the PrintT lines this module emits ("havoc-...").
set -eu
cd "$(dirname "$0")/.."
for c in "$@"; do
  echo "== $c"
  podman run --rm -v "$PWD":/spec:Z -w /spec --entrypoint sh localhost/veda-tlc:1.8.0 -c \
    "java -XX:+UseParallelGC -DTLA-Library=/spec -cp /opt/tla2tools.jar tlc2.TLC -workers 1 \
       -metadir /tmp/st-$c -config havoc/$c.cfg havoc/HavocSpec.tla 2>&1" \
    | if [ "${RAW:-0}" = 1 ]; then cat; else python3 -I havoc/extract.py; fi
done
