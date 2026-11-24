#!/bin/sh
# Run every cfg in selfcomp/ and keep the raw TLC output in selfcomp/out/.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/out"
for f in "$here"/*.cfg; do
  c="$(basename "$f" .cfg)"
  sh "$here/run.sh" "$c" > "$here/out/$c.txt" 2>&1 || true
done
