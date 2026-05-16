#!/usr/bin/env bash
# Anansi Self-Healing Scraper — end-to-end demo
# No API keys required. Uses mock HTML to demonstrate self-healing selectors.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null

echo "==> Running Anansi self-healing scraper demo..."
echo ""
python3 demo_scraper.py
