#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "--- IBKR Trading Data Integration Demo ---"
echo ""

python3 demo.py
