#!/usr/bin/env bash
set -euo pipefail

test -d examples/notebooks
for f in examples/notebooks/*; do
  grep -q "Invariant" "$f"
done
