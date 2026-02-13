#!/usr/bin/env bash
set -euo pipefail

test -d examples
./examples/tests/validate_examples.sh
