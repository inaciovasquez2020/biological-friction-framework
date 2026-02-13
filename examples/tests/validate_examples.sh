#!/usr/bin/env bash
set -euo pipefail

for f in examples/*.md; do
  grep -q "Example:" "$f"
  grep -q "Interpretation" "$f"
done
