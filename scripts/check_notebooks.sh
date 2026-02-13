#!/usr/bin/env bash
set -euo pipefail

FILES=$(find examples/notebooks -type f ! -name README.md)

for f in $FILES; do
  grep -q "Invariant" "$f"
done
