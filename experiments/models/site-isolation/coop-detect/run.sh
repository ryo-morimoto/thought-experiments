#!/bin/sh
# usage: CHROME=<chromium binary> [SERVER=server.py|server-closed.py] [WORK=<dir>] sh run.sh
# Runs 4 cases: {COOP same-origin, no COOP} x {default, --disable-features=CrossOriginOpenerPolicy}
D=${WORK:-$(mktemp -d)}; S=$(cd "$(dirname "$0")" && pwd)
CH=${CHROME:?set CHROME to a Chromium binary}
P1=18431; P2=18432
python3 -I $S/${SERVER:-server.py} $P1 $P2 >> $D/server.log 2>&1 &
SP=$!
sleep 1
"$CH" --version
for flags in "" "--disable-features=CrossOriginOpenerPolicy"; do
  for coop in same-origin ""; do
    rm -rf $D/profile
    : > $D/server.log
    timeout 10 "$CH" --headless=new --no-sandbox --disable-popup-blocking --user-data-dir=$D/profile \
      $flags "http://127.0.0.1:$P1/opener?coop=$coop" > /dev/null 2>&1
    echo "flags=[$flags] coop=[$coop] -> $(grep -a REPORT $D/server.log || echo 'no report')"
  done
done
kill $SP
