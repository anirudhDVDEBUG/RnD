#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================================="
echo "Cosmos Predict 2.5 LoRA Fine-Tuning Demo"
echo "=============================================="
echo ""
echo "This demo runs the full pipeline in simulation mode."
echo "No GPU or API keys required."
echo ""

# Run the demo pipeline
python3 demo_cosmos_lora.py

echo ""
echo "Output files:"
ls -la output/demo_results.json 2>/dev/null || echo "  (no output files generated)"
echo ""
echo "Mock dataset structure:"
find gr1_dataset -type f | head -20
echo "  ..."
echo ""
echo "Done. For actual GPU training, see HOW_TO_USE.md"
