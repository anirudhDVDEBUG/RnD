#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Granite Embedding Multilingual R2 — run.sh ==="
echo ""

# Install minimal deps (numpy only needed for mock mode)
pip install --quiet numpy

# Run demo in mock mode (no model download, instant results)
# Use --live to download and run the real 97M model (~380 MB)
python3 demo.py --mock

echo ""
echo "To run with the REAL model (requires ~380 MB download):"
echo "  pip install sentence-transformers"
echo "  python3 demo.py --live"
echo ""
echo "To try the larger 311M model with Matryoshka support:"
echo "  python3 demo.py --live --model ibm-granite/granite-embedding-311m-multilingual-r2"
