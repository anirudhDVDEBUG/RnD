#!/usr/bin/env bash
# Social Media Scraper — end-to-end demo
# Runs with mock data; no API keys or external tools required.

set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Social Media Scraper Demo"
echo ""

# Run demo with mock data (no dependencies needed beyond Python 3)
python3 demo.py

echo ""
echo ">>> To scrape a real post, install dependencies and run:"
echo "    pip install yt-dlp openai-whisper requests"
echo "    python3 demo.py https://www.youtube.com/watch?v=VIDEO_ID"
