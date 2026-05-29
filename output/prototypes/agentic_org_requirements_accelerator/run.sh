#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Agentic Organization Requirements Accelerator ==="
echo ""

# Install dependencies
if ! python3 -c "import yaml, rich" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run the accelerator
python3 accelerator.py --input sample_requirements.yaml --output output

echo ""
echo "--- Report preview (first 40 lines) ---"
head -40 output/analysis_report.md
