#!/bin/bash
# usage: runwpt.sh <product> <logname> [extra wpt-run args...]
# Runs the repro tests inside the mounted wpt clone. Mirrors scripts/run.sh.
set -u
cd /wpt
p=$1; n=$2; shift 2
TESTS="repro/cve-2026-8950-form-post-origin-after-xsite-redirect.sub.https.html repro/cve-2026-8950-origin-after-xsite-redirect.sub.https.html repro/cve-2024-6611-samesite-cookie-xsite-iframe.sub.https.html repro/cve-2025-3071-aboutblank-back-origin.sub.https.html"
./wpt run --yes --headless \
  --log-wptreport=/logs/$n.json --log-mach=/logs/$n-mach.log --log-raw=/logs/$n-raw.log \
  "$@" $p $TESTS > /logs/$n-console.log 2>&1
echo "rc=$? ($n)"
