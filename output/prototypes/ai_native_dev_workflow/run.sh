#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== AI-Native 4-Phase Workflow Demo ==="
echo ""

# Clean previous output
rm -rf demo_output

# Run the demo (stdlib only — no pip install needed)
python3 demo.py

echo ""
echo "Done. Inspect demo_output/ for all generated artifacts."
