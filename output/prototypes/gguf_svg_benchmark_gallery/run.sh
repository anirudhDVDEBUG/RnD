#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[*] GGUF SVG Benchmark Gallery — Demo Mode"
echo "[*] Generating mock SVGs for 8 quantization levels..."
echo ""

# Generate mock SVGs (no GPU/model needed)
python3 mock_svgs.py

echo ""
echo "[*] Building HTML gallery..."

# Build the gallery
python3 gallery_builder.py --input-dir output --output gallery.html

echo "[*] Done! Open gallery.html in a browser to compare results."
echo ""
echo "    Files created:"
ls -la output/*.svg | awk '{print "      " $NF " (" $5 " bytes)"}'
echo "      gallery.html"
