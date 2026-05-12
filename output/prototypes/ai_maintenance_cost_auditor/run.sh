#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================================="
echo "  AI Maintenance Cost Auditor — Demo Run"
echo "=============================================="
echo ""

echo "--- Auditing CLEAN sample (good_code.py) at 3x speed ---"
python3 auditor.py samples/good_code.py --speed 3
echo ""

echo "--- Auditing MESSY sample (bad_code.py) at 3x speed ---"
python3 auditor.py samples/bad_code.py --speed 3
echo ""

echo "--- JSON output for bad_code.py ---"
python3 auditor.py samples/bad_code.py --speed 3 --json
