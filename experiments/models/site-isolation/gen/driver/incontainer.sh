#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with /wpt (WPT clone),
# /gen (gen/tests) and /logs mounted. Adapted from observe/driver/incontainer.sh.
# usage: incontainer.sh <product> <repeats> [file-glob]
# One `wpt run` per repetition over all generated top-level files.
set -u
P=$1; REP=${2:-2}; GLOB=${3:-top-*}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/gen-si && cp -r /gen /wpt/gen-si
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
TESTS=$(cd /wpt && ls gen-si/$GLOB.html | sed 's|^|/|')
for r in $(seq 1 "$REP"); do
  n=$P-r$r; s=$(date +%s)
  timeout 5400 ./wpt run --yes --headless --log-raw=/logs/$n-raw.log \
    --timeout-multiplier=4 $EXTRA $P $TESTS > /logs/$n-console.log 2>&1
  echo "rc=$? ($n) $(( $(date +%s) - s ))s"
done
rm -rf /wpt/gen-si   # (the clone is an overlay mount; nothing reaches the host copy)
echo ALL DONE GEN $P
