#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
python3 data_craft.py

echo ""
echo "Generated files:"
ls -lh "$SCRIPT_DIR"/*.html 2>/dev/null || echo "  (no HTML files found)"
