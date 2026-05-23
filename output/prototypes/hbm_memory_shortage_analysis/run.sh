#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== HBM Memory Shortage Analysis ==="
echo ""
echo "Running analysis (no API keys required)..."
echo ""

python3 hbm_analysis.py

echo ""
echo "--- JSON output ---"
python3 hbm_analysis.py --json | python3 -m json.tool | head -30
echo "  ... (truncated, run 'python3 hbm_analysis.py --json' for full output)"
