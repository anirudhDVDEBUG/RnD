#!/usr/bin/env bash
set -e

echo "=== Simon Willison Newsletter AI Roundup - Demo ==="
echo ""

python3 roundup.py

echo ""
echo "--- JSON export ---"
python3 roundup.py --json --export
echo ""
echo "Done. See roundup_april_2026.json for structured output."
