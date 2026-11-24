#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with /wpt (WPT clone,
# overlay), /tests (history/tests), /logs mounted. As redirect/driver.
# usage: incontainer.sh <product> <repeats> [file-glob] [file of upstream WPT tests]
set -u
P=$1; REP=${2:-2}; GLOB=${3:-h-*}; ORIG=${4:-}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/history-si && cp -r /tests /wpt/history-si
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
TESTS=$(cd /wpt && ls history-si/$GLOB.html | sed 's|^|/|')
for r in $(seq 1 "$REP"); do
  n=$P-r$r; s=$(date +%s)
  timeout 9000 ./wpt run --yes --headless --log-raw=/logs/$n-raw.log \
    --timeout-multiplier=10 --processes=${PROCS:-1} $EXTRA $P $TESTS > /logs/$n-console.log 2>&1
  echo "rc=$? ($n) $(( $(date +%s) - s ))s"
done
if [ -n "$ORIG" ]; then
  timeout 3000 ./wpt run --yes --headless --log-raw=/logs/orig-$P-raw.log \
    --log-wptreport=/logs/orig-$P.json --timeout-multiplier=4 $EXTRA $P \
    $(cat "/driver/$ORIG") > /logs/orig-$P-console.log 2>&1
  echo "rc=$? (orig $P)"
fi
rm -rf /wpt/history-si   # (the clone is an overlay mount; nothing reaches the host copy)
echo ALL DONE HISTORY $P
