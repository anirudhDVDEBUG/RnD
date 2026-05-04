#!/usr/bin/env bash
# run.sh — Demo the unslop text cleaner
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================"
echo "  UNSLOP TEXT — AI Slop Remover Demo"
echo "============================================"
echo ""

echo "--- ORIGINAL (sloppy AI-generated text) ---"
echo ""
cat sample_sloppy.txt
echo ""

echo "============================================"
echo "  Running unslop..."
echo "============================================"
echo ""
python3 unslop.py sample_sloppy.txt

echo ""
echo "============================================"
echo "  JSON output mode:"
echo "============================================"
echo ""
python3 unslop.py sample_sloppy.txt --json
