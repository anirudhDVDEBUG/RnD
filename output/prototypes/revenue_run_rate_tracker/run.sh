#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
python3 revenue_tracker.py

echo ""
echo "Done. Open run_rate_revenue.png to see the result."
