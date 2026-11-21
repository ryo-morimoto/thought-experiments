#!/bin/bash
# usage: runsearch.sh <product> <logname> <tests> [extra wpt-run args...]
set -u
cd /wpt
p=$1; n=$2; tests=$3; shift 3
./wpt run --yes --headless \
  --log-wptreport=/logs/$n.json --log-mach=/logs/$n-mach.log --log-raw=/logs/$n-raw.log \
  --timeout-multiplier=4 \
  "$@" $p $tests > /logs/$n-console.log 2>&1
echo "rc=$? ($n)"
