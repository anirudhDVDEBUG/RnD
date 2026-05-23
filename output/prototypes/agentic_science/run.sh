#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=============================================="
echo "  Agentic Science - Demo Pipeline"
echo "=============================================="
echo ""

# Install dependencies if needed
if ! python3 -c "import sklearn" 2>/dev/null; then
    echo "[setup] Installing Python dependencies..."
    pip install -q -r requirements.txt
fi

echo "--- Stage 1: Single-cell RNA-seq analysis ---"
echo ""
python3 demo_scrna.py
echo ""

echo "--- Stage 2: Bulk RNA-seq DE + pathway enrichment ---"
echo ""
python3 demo_bulk_de.py
echo ""

echo "=============================================="
echo "  All outputs saved to ./output/"
echo "=============================================="
ls -lh output/
echo ""
echo "Done. See output/ for plots and CSV tables."
