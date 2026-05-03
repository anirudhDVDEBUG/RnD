#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================================="
echo "  Opus Compatibility Scanner — Demo Run"
echo "=============================================="
echo ""
echo "Scanning mock project with intentional Opus 4.6 patterns..."
echo ""

python3 scanner.py mock_project

echo ""
echo "Done. See HOW_TO_USE.md to scan your own project."
