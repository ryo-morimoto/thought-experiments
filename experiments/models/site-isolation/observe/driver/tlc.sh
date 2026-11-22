#!/bin/bash
# Run TLC (podman image localhost/veda-tlc:1.8.0) on AllowedSets with a cfg.
# usage: tlc.sh <cfg> <out file>
# Copies the modules into a scratch dir so TLC writes nothing into the repo.
set -u
D=$(cd "$(dirname "$0")/../.." && pwd)   # experiments/models/site-isolation
T=$(mktemp -d)
cp "$D/SpecIsolation.tla" "$D"/observe/*.tla "$D/observe/$1" "$T/"
podman run --rm -v "$T":/w:Z -w /w localhost/veda-tlc:1.8.0 java -XX:+UseParallelGC \
  -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st -config "$1" AllowedSets.tla > "$2" 2>&1
rm -rf "$T"
grep -E '^<<|Error|error|violated|No error' "$2" | cut -c1-3000
