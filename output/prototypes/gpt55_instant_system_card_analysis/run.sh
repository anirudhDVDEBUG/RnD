#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "Running GPT-5.5 Instant System Card Analysis..."
echo ""

python3 analyzer.py
