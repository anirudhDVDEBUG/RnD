#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running Data Center Land Use Debunk skill demo..."
echo ""

python3 debunk.py
