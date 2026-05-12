#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Running ChatGPT Adoption Trends Q1 2026 analysis..."
echo ""
python3 analyze_trends.py --json
echo ""
echo ">>> Done. See output.json for structured data."
