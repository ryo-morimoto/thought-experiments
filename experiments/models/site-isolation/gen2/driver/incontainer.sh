#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with /wpt (WPT clone,
# overlay mount), /gen2 (gen2/tests) and /logs mounted. Adapted from
# gen/driver/incontainer.sh. One `wpt run` per repetition over all files.
# usage: incontainer.sh <product> <repeats> [file-glob]
set -u
P=$1; REP=${2:-2}; GLOB=${3:-*}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/gen2-si && cp -r /gen2 /wpt/gen2-si
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
TESTS=$(cd /wpt && ls gen2-si/$GLOB.html | sed 's|^|/|')
for r in $(seq 1 "$REP"); do
  n=$P-r$r; s=$(date +%s)
  timeout 5400 ./wpt run --yes --headless --log-raw=/logs/$n-raw.log \
    --timeout-multiplier=4 $EXTRA $P $TESTS > /logs/$n-console.log 2>&1
  echo "rc=$? ($n) $(( $(date +%s) - s ))s"
done
rm -rf /wpt/gen2-si
echo ALL DONE GEN2 $P
