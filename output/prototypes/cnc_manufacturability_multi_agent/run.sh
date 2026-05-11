#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================"
echo " CNC Manufacturability Multi-Agent Pipeline"
echo "============================================"
echo ""

# --- Demo 1: Steel bracket (CONDITIONAL — missing tap) ---
echo ">>> Demo 1: Steel 304 bracket, +/-0.05mm tolerance"
echo ""
python3 pipeline.py --part sample_bracket --material "Steel 304" --tolerance 0.05
echo ""

echo "============================================"
echo ""

# --- Demo 2: Aluminum plate (simpler part) ---
echo ">>> Demo 2: Aluminum 6061 plate, +/-0.05mm tolerance"
echo ""
python3 pipeline.py --part simple_plate --material "Aluminum 6061" --tolerance 0.05
echo ""

echo "============================================"
echo ""

# --- Demo 3: Titanium bracket (difficult material) ---
echo ">>> Demo 3: Titanium Grade 5 bracket, +/-0.01mm tight tolerance"
echo ""
python3 pipeline.py --part sample_bracket --material "Titanium Grade 5" --tolerance 0.01
