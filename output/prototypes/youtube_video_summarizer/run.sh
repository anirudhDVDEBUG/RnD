#!/usr/bin/env bash
# YouTube Video Summarizer - end-to-end demo
# Uses mock data by default (no network, no API keys needed)
set -e

cd "$(dirname "$0")"

echo "=== YouTube Video Summarizer ==="
echo ""

# Run with mock data for reproducible demo
python3 summarizer.py --mock --output notes

echo ""
echo "--- Generated Summary Preview ---"
echo ""
cat notes/*.md
echo ""
echo "=== Done. See notes/ directory for output. ==="
