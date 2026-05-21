#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking Python version..."
python3 --version

echo ""
python3 tracker.py
