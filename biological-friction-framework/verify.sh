#!/bin/sh
Ti=$1

if [ -z "$Ti" ]; then
  echo "Usage: ./verify.sh T1"
  exit 1
fi

cd "certs/$Ti" || exit 1

python -m json.tool manifest.json > /dev/null || exit 1
python -m json.tool witness.json > /dev/null || exit 1

STAT_HASH=$(jq -r '.statement_sha256' manifest.json)
WIT_HASH=$(jq -r '.witness_sha256' manifest.json)

printf "%s  %s\n" "$STAT_HASH" "../../statements/$Ti.txt" > /tmp/stat.check
printf "%s  %s\n" "$WIT_HASH" "witness.json" > /tmp/wit.check

sha256sum -c /tmp/stat.check || exit 1
sha256sum -c /tmp/wit.check || exit 1

rm -f /tmp/stat.check /tmp/wit.check

echo "Certificate $Ti hashes verified."

