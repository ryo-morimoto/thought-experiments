#!/bin/bash
set -u
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq chromium firefox-esr fonts-liberation xvfb git ca-certificates libgtk-3-0 libasound2 libdbus-glib-1-2 libgirepository1.0-dev libcairo2-dev pkg-config >/dev/null 2>&1
cd /wpt
./wpt make-hosts-file >> /etc/hosts
bash /driver/runwpt.sh chrome  chrome-cur3  --channel=stable --binary-arg=--no-sandbox --install-browser --install-webdriver
bash /driver/runwpt.sh firefox firefox-cur3 --channel=stable --install-browser --install-webdriver
bash /driver/runwpt.sh chrome  chrome134b --binary=/dl/chrome134/chrome-linux64/chrome --webdriver-binary=/dl/chrome134/chromedriver-linux64/chromedriver --binary-arg=--no-sandbox
bash /driver/runwpt.sh firefox firefox150b --binary=/dl/ff150/firefox/firefox --webdriver-binary=/dl/geckodriver
bash /driver/runwpt.sh firefox firefox127 --binary=/dl/ff127/firefox/firefox --webdriver-binary=/dl/geckodriver
echo ALL DONE3
