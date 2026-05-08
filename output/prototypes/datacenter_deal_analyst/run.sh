#!/usr/bin/env bash
# Run the Data Center Deal Analyst demo
# No API keys required — uses mock data from public reporting.

set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Installing dependencies (if any)..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ">>> Running deal analysis demo..."
echo ""
python3 demo.py
