#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with
#   /wpt (WPT clone), /bcg/tests (probe tests), /driver, /logs mounted.
# usage: incontainer.sh <repeat> <tag>
set -u
REP=${1:-5}; TAG=${2:-r1}; PRODS=${3:-chrome firefox}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb git ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
rm -rf /wpt/bcg-observe && cp -r /bcg/tests /wpt/bcg-observe
run() { p=$1; n=$2; shift 2
  ./wpt run --yes --headless --repeat=$REP \
    --log-wptreport=/logs/$n.json --log-raw=/logs/$n-raw.log \
    --timeout-multiplier=4 "$@" $p bcg-observe/ > /logs/$n-console.log 2>&1
  echo "rc=$? ($n)"; }
[[ $PRODS == *chrome* ]] && run chrome  chrome-$TAG  --channel=stable --binary-arg=--no-sandbox --install-browser --install-webdriver
[[ $PRODS == *firefox* ]] && run firefox firefox-$TAG --channel=stable --install-browser --install-webdriver
rm -rf /wpt/bcg-observe
echo ALL DONE BCG
