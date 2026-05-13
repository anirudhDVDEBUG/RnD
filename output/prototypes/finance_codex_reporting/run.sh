#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Finance Codex Reporting — Demo Run ==="
echo ""

# No external dependencies needed — pure Python stdlib
python3 finance_codex.py

echo "=== Done. See output/ for CSV export. ==="
