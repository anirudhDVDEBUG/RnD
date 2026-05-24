#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "  FigMirror: Paper Figure Style Replication"
echo "=========================================="
echo ""

# Install dependencies if needed
echo "[1/3] Checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q matplotlib numpy pandas seaborn Pillow 2>/dev/null || true

# Generate the reference figure (simulates a paper figure)
echo ""
echo "[2/3] Generating reference figure (simulates a paper's figure)..."
python generate_reference.py

# Apply the extracted style to user data
echo ""
echo "[3/3] Applying extracted style to your data..."
python figmirror_demo.py reference_style.json sample_data.csv output_figure

echo ""
echo "=========================================="
echo "  Results"
echo "=========================================="
echo ""
echo "  Reference:  reference_figure.png"
echo "  Output:     output_figure.png (300 DPI)"
echo "  Output:     output_figure.pdf (vector)"
echo ""
echo "  Compare them side-by-side to see the"
echo "  style replication in action."
echo "=========================================="
