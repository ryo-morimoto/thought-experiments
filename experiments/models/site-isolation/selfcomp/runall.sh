#!/bin/sh
# Run cfgs in selfcomp/ (all, or those matching the glob in $1, e.g. 'SC-*')
# and keep the raw TLC output in selfcomp/out/<cfg>.txt.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/out"
for f in "$here"/${1:-*}.cfg; do
  c="$(basename "$f" .cfg)"
  sh "$here/run.sh" "$c" > "$here/out/$c.txt" 2>&1 || true
done
# TLC writes trace-exploration specs next to the module; they are not kept.
rm -f "$here"/SelfCompRun_TTrace_*
