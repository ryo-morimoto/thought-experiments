#!/bin/sh
# originstruct/RESULTS.md: run TLC on one cfg of this directory.
# usage: sh originstruct/tlc.sh <cfg> [target]   (from site-isolation/)
# With a target (an OriginStruct property name), the cfg's invariant is
# replaced by PrintTarget with Target <- <target>.
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
cmd="cp /spec/originstruct/*.tla /spec/SpecIsolation.tla /tmp/w/ && cp /spec/originstruct/$1 /tmp/w/run.cfg"
if [ $# -ge 2 ]; then
  cmd="$cmd && sed -i 's/^INVARIANTS .*/INVARIANTS PrintTarget/' /tmp/w/run.cfg && echo 'CONSTANT Target <- $2' >> /tmp/w/run.cfg"
fi
podman run --rm -v "$here":/spec:Z,ro --entrypoint sh localhost/veda-tlc:1.8.0 \
  -c "mkdir -p /tmp/w && $cmd && cd /tmp/w && java -Xmx2g -XX:+UseParallelGC -cp /opt/tla2tools.jar tlc2.TLC -nowarning -metadir /tmp/st-x -config run.cfg OriginStruct.tla 2>&1" \
  | grep -v -e '^Starting' -e '^Running' -e '^Parsing' -e '^Semantic' -e '^Implied' -e '^Progress' \
            -e '^Computing' -e '^Checking' -e '^Model checking' -e '^The depth' -e '^The average' \
            -e 'fingerprint' -e '^Loading' -e '^TLC2 Version' -e 'states generated' -e '^Finished computing'
