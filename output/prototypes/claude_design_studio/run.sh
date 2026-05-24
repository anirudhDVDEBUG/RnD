#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================"
echo "  Claude Design Studio - Demo Run"
echo "============================================"
echo ""

mkdir -p output

# 1. Dark dashboard (flagship demo)
python3 design_studio.py \
  --layout dashboard --theme dark --accent "#6366f1" \
  --title "SaaS Analytics" \
  -o output/dashboard_dark.html

# 2. Light landing page
python3 design_studio.py \
  --layout landing --theme light --accent "#2563eb" \
  --title "Ship Faster" \
  --description "The modern platform for teams that build." \
  -o output/landing_light.html

# 3. Dark login form
python3 design_studio.py \
  --layout form --theme dark --accent "#8b5cf6" \
  --title "Welcome Back" \
  -o output/form_dark.html

# 4. JSON spec demo
cat > output/_spec.json <<'SPEC'
{
  "title": "Product Catalog",
  "layout": "card-grid",
  "theme": "light",
  "accent": "#059669",
  "description": "Browse our latest arrivals"
}
SPEC
python3 design_studio.py --json-spec output/_spec.json -o output/cards_light.html

echo ""
echo "--------------------------------------------"
echo "  4 designs generated in ./output/"
echo "  Open any .html file in a browser to view."
echo "--------------------------------------------"
ls -lh output/*.html
