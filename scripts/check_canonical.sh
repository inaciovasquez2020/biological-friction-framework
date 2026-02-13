#!/usr/bin/env bash
set -euo pipefail

test -f STATUS.md
test -d examples
test -d figures

grep -q "Status: Canonical" STATUS.md
