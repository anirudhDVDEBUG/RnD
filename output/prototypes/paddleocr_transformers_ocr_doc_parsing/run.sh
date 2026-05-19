#!/usr/bin/env bash
# ---------------------------------------------------------------
# PaddleOCR 3.5 + Transformers Backend  --  Demo Runner
#
# Runs in mock mode by default (no GPU / model download needed).
# Set OCR_MODE=live to use real PaddleOCR models.
# ---------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "------------------------------------------------------------"
echo " PaddleOCR 3.5 + Transformers  --  run.sh"
echo "------------------------------------------------------------"
echo ""

# Default to mock mode for zero-dependency demo
export OCR_MODE="${OCR_MODE:-mock}"

python3 ocr_demo.py

echo ""
echo "Done. Output saved to output_results.json"
