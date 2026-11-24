#!/bin/sh
# adequacy/RESULTS.md: run TLC on one module/cfg of this directory.
# usage: sh adequacy/tlc.sh <cfg> <module>   (from site-isolation/)
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
podman run --rm -v "$here":/spec:Z -w /spec/adequacy --entrypoint sh localhost/veda-tlc:1.8.0 \
  -c "java -XX:+UseParallelGC -DTLA-Library=/spec -cp /opt/tla2tools.jar tlc2.TLC -workers 4 -metadir /tmp/st-x -config $1 $2.tla 2>&1" \
  | grep -v -e '^Starting' -e '^Running' -e '^Parsing' -e '^Semantic' -e '^Implied' -e '^Progress' \
            -e '^Computing' -e '^Checking' -e '^Model checking' -e '^The depth' -e '^The average' \
            -e 'fingerprint' -e '^Loading' -e '^TLC2 Version' -e 'states generated' -e '^Finished computing'
