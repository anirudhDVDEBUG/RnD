#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Prompt Cache Skills — Demo ==="
echo "Checking Python..."
python3 --version

echo ""
echo "Running prompt-cache analysis on 3 mock agent configs..."
echo ""

python3 demo.py
