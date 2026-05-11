#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Deliberate Wheel Reinvention — Demo ==="
echo ""

python3 wheel_reinvention.py

echo ""
echo "--- Generating a specific plan (databases / B-tree index) ---"
echo ""

python3 wheel_reinvention.py --plan databases "B-tree index"

echo ""
echo "Done. Try 'python3 wheel_reinvention.py --interactive' for guided mode."
