#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== uni1-image-ad Demo (Mock Mode) ==="
echo ""

# Install dependencies quietly
pip install -q -r requirements.txt 2>/dev/null || pip install -q requests pyyaml Pillow 2>/dev/null || true

# Clean previous output
rm -rf output/
mkdir -p output

echo "--- Step 1: Reverse-engineer a reference ad ---"
python reverse_engineer.py \
  --reference "https://example.com/sample-competitor-ad.png" \
  --output-template ./output/template.yaml \
  --mock

echo ""
echo "--- Step 2: Generate ad from template ---"
python generate_ad.py \
  --brand "AcmeCoffee" \
  --product "Single-origin dark roast beans" \
  --tone "dark, moody, premium, warm golden accents" \
  --cta "Shop Now" \
  --ratio "1:1" \
  --template ./output/template.yaml \
  --output ./output \
  --mock

echo ""
echo "--- Step 3: Generate Story variant ---"
python generate_ad.py \
  --brand "AcmeCoffee" \
  --product "Single-origin dark roast beans" \
  --tone "dark, moody, premium" \
  --cta "Swipe Up" \
  --platform "instagram_stories" \
  --output ./output \
  --mock

echo ""
echo "=== Output Files ==="
ls -la output/
echo ""
echo "--- prompt_log.json ---"
python -m json.tool output/prompt_log.json
echo ""
echo "--- template.yaml ---"
cat output/template.yaml
echo ""
echo "=== Done. In production, replace --mock with LUMALABS_API_KEY for real generation. ==="
