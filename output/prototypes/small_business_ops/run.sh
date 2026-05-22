#!/usr/bin/env bash
# Small Business Ops — demo runner
# Runs all 10 workflows with mock data (no API keys needed)
set -euo pipefail
cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "Running Small Business Ops demo (all 10 workflows)..."
echo ""
python3 small_business_ops.py all
