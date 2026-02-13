#!/usr/bin/env bash
set -euo pipefail

FILES=$(find examples -name "*.md")

for f in $FILES; do
  grep -q "Example:" "$f" || continue
  grep -q "Interpretation" "$f"
done
