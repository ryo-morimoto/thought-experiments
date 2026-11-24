#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm with /wpt (WPT clone,
# overlay), /tests (holdout/tests), /driver and /logs mounted. Adapted from
# gen/driver and redirect/driver. Adds two alternate hosts (sites c and d) to
# the WPT server config (overlay only). The certificate is the
# pregenerated one: Chrome ignores its errors by SPKI and Firefox runs without
# certutil (acceptInsecureCerts), as for the two stock sites.
# usage: incontainer.sh <product> <repeats> <file-glob>
set -u
P=$1; REP=${2:-2}; GLOB=${3:-*}
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 >/dev/null 2>&1
cd /wpt
# config.json overrides cannot add keys (wptserve _merge_dict), so the default
# alternate_hosts of tools/serve/serve.py are edited in the overlay.
sed -i 's|"alt": "not-web-platform.test"|"alt": "not-web-platform.test", "alt2": "web-platform-c.test", "alt3": "web-platform-d.test"|' \
  tools/serve/serve.py
./wpt make-hosts-file >> /etc/hosts
grep -c "web-platform-c.test" /etc/hosts
rm -rf /wpt/holdout-si && cp -r /tests /wpt/holdout-si
EXTRA="--channel=stable --install-browser --install-webdriver"
[ "$P" = chrome ] && EXTRA="$EXTRA --binary-arg=--no-sandbox"
TESTS=$(cd /wpt && ls holdout-si/$GLOB.html | sed 's|^|/|')
for r in $(seq 1 "$REP"); do
  n=$P-r$r; s=$(date +%s)
  timeout 7200 ./wpt run --yes --headless --log-raw=/logs/$n-raw.log \
    --timeout-multiplier=4 $EXTRA $P $TESTS > /logs/$n-console.log 2>&1
  echo "rc=$? ($n) $(( $(date +%s) - s ))s"
done
rm -rf /wpt/holdout-si  # (overlay mount; nothing reaches the host copy)
echo ALL DONE HOLDOUT $P
