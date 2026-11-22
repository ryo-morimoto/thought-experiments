#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with
#   /wpt (WPT clone), /obs (observe/tests), /driver (observe/driver), /logs mounted.
# usage: incontainer.sh <product> <repeats> [obs|orig|both] [file-glob]
# One `wpt run` per observation file per repetition (fresh browser each time);
# the original WPT tests of the 109 rows run once, in one session.
set -u
P=$1; REP=${2:-2}; WHAT=${3:-both}; GLOB=${4:-*}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/observe-si && cp -r /obs /wpt/observe-si
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
mkdir -p /logs/obs /logs/orig
if [ "$WHAT" != orig ]; then
  for r in $(seq 1 "$REP"); do
    for f in /wpt/observe-si/$GLOB.html; do
      t=${f#/wpt/}; b=$(basename "$f" .html); n=$P-$b-r$r
      timeout 900 ./wpt run --yes --headless --log-raw=/logs/obs/$n-raw.log \
        --timeout-multiplier=4 $EXTRA $P "$t" > /logs/obs/$n-console.log 2>&1
      echo "rc=$? ($n)"
    done
  done
fi
if [ "$WHAT" != obs ]; then
  timeout 3000 ./wpt run --yes --headless --log-raw=/logs/orig/$P-raw.log \
    --log-wptreport=/logs/orig/$P.json --timeout-multiplier=4 $EXTRA $P \
    $(cat /driver/originals.txt) > /logs/orig/$P-console.log 2>&1
  echo "rc=$? (orig $P)"
fi
rm -rf /wpt/observe-si
echo ALL DONE OBSERVE $P
