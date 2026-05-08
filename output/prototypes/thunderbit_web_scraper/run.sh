#!/usr/bin/env bash
# Thunderbit Web Scraper – end-to-end demo
# No API key needed; uses mock data to show tool output shapes.
set -euo pipefail
cd "$(dirname "$0")"

echo "Running Thunderbit Web Scraper demo..."
echo ""
node demo.js
