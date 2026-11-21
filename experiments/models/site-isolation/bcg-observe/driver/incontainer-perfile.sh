#!/bin/bash
# Like incontainer.sh, but one `wpt run` per test file per repetition (fresh browser each),
# because Firefox's runner window broke (__wptrunner_process_next_event) after 2 files
# in a shared session.
# usage: incontainer-perfile.sh <repeat> <tag> <product>
set -u
REP=$1; TAG=$2; P=$3
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb git ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/bcg-observe && cp -r /bcg/tests /wpt/bcg-observe
EXTRA="--channel=stable --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
first=1
for r in $(seq 1 $REP); do
  for f in /wpt/bcg-observe/*.https.html; do
    b=$(basename $f .https.html); n=$P-$TAG-$b-$r
    IB="--install-browser"
    timeout 600 ./wpt run --yes --headless --log-raw=/logs/pf/$n-raw.log --timeout-multiplier=4 \
      $EXTRA $IB $P bcg-observe/$b.https.html > /logs/pf/$n-console.log 2>&1
    echo "rc=$? ($n)"
  done
done
rm -rf /wpt/bcg-observe
echo ALL DONE BCG PERFILE
