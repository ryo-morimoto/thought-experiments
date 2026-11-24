#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with /wpt and /logs mounted:
# the original WPT tests used to classify out-of-model rows (gen/RESULTS.md).
# usage: originals.sh <product>
set -u
P=$1
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
./wpt run --yes --headless --log-raw=/logs/orig-$P-raw.log --log-wptreport=/logs/orig-$P.json \
  --timeout-multiplier=4 $EXTRA $P \
  /html/cross-origin-embedder-policy/cross-origin-isolated-permission-iframe.https.window.html \
  > /logs/orig-$P-console.log 2>&1
echo "rc=$? ALL DONE ORIG $P"
