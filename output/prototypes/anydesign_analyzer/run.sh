#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo " AnyDesign Analyzer — Demo Run"
echo "============================================================"
echo ""

# Run in mock/demo mode (no external deps required)
python3 analyzer.py mock -o design.md

echo ""
echo "Done. Full output written to: design.md"
echo "Open design.md to see the complete design token system."
