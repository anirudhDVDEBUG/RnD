#!/usr/bin/env bash
# x-twitter-scraper demo — runs with mock data, no API keys needed.
set -euo pipefail

cd "$(dirname "$0")"

echo ""
echo ">> Installing dependencies (if any)..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ">> Running x-twitter-scraper demo..."
echo ""
python3 demo_scraper.py

echo ">> Output files:"
ls -lh output/ 2>/dev/null || echo "   (no output directory found)"
echo ""
