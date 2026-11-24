#!/bin/sh
# Run the self-composition checks (experiments/2026-11-24-selfcomp-orb-leak.md).
# Usage: sh selfcomp/run.sh <cfg name without .cfg> ...   (from site-isolation/)
# Count-* cfgs use SelfCompORB.tla, SC-* cfgs use SelfCompRun.tla.
set -eu
cd "$(dirname "$0")/.."
for c in "$@"; do
  case "$c" in SC-*) m=SelfCompRun ;; *) m=SelfCompORB ;; esac
  echo "== $c"
  podman run --rm -v "$PWD":/spec:Z -w /spec --entrypoint sh localhost/veda-tlc:1.8.0 -c \
    "java -XX:+UseParallelGC -DTLA-Library=/spec -cp /opt/tla2tools.jar tlc2.TLC -workers 1 \
       -metadir /tmp/st-$c -config selfcomp/$c.cfg selfcomp/$m.tla 2>&1"
done
