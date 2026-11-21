#!/bin/bash
# Runs inside docker.io/library/python:3.12-bookworm. Installs deps + browsers and runs
# the search tests on current + pre-fix builds. Mirrors the prereg/repro driver.
set -u
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb git ca-certificates \
  libgtk-3-0 libasound2 libdbus-glib-1-2 libgirepository1.0-dev libcairo2-dev pkg-config >/dev/null 2>&1

cd /wpt
./wpt make-hosts-file >> /etc/hosts

# zipfile drops the exec bit on Chrome's crashpad handler -> no session without this.
chmod +x /dl/chrome134/chrome-linux64/chrome_crashpad_handler 2>/dev/null || true
chmod +x /dl/chrome134/chrome-linux64/chrome 2>/dev/null || true

A="search/search-a-origin-after-nav.sub.https.html"
B="search/search-b-redirect-origin.sub.https.html"
BOTH="$A $B"

# Current stable Chrome (158) and Firefox (160): both targets.
bash /driver/runsearch.sh chrome  chrome-cur  "$BOTH" --channel=stable --binary-arg=--no-sandbox --install-browser --install-webdriver
bash /driver/runsearch.sh firefox firefox-cur "$BOTH" --channel=stable --install-browser --install-webdriver

# Pre-fix Chrome for Testing 134 (CVE-2025-3071 pre-fix): Target A.
bash /driver/runsearch.sh chrome  chrome134 "$A" \
  --binary=/dl/chrome134/chrome-linux64/chrome \
  --webdriver-binary=/dl/chrome134/chromedriver-linux64/chromedriver --binary-arg=--no-sandbox

# Pre-fix Firefox 150 (CVE-2026-8950 fixed in 151): Target B.
bash /driver/runsearch.sh firefox firefox150 "$B" \
  --binary=/dl/ff150/firefox/firefox --webdriver-binary=/dl/geckodriver

echo ALL DONE SEARCH
