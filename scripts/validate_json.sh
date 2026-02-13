#!/usr/bin/env bash
set -euo pipefail

command -v ajv >/dev/null 2>&1 || exit 0

for f in examples/*.json; do
  ajv validate -s schema/biological_friction.schema.json -d "$f"
done
