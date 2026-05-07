#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "=== MarkPDF Demo: Markdown → Styled HTML ==="
echo ""

# Install dependencies
if [ ! -d "node_modules" ]; then
  echo "[1/3] Installing dependencies..."
  npm install --quiet 2>&1 | tail -1
else
  echo "[1/3] Dependencies already installed."
fi

# Convert sample document
echo "[2/3] Converting sample.md → styled document..."
node convert.js sample.md

# Convert sample slides
echo "[3/3] Converting sample_slides.md → slide deck..."
node convert.js sample_slides.md --slides

echo "─────────────────────────────────────────────"
echo ""
echo "Generated files in output/:"
ls -lh output/
echo ""
echo "Open output/sample.html in a browser to see the styled document."
echo "Open output/sample_slides.html to see the slide deck."
echo "Print either to PDF (Ctrl+P) for a premium PDF result."
echo ""
