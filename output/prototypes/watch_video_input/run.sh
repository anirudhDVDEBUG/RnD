#!/usr/bin/env bash
# run.sh — Demo the Watch video-input pipeline with mock data.
# No network, GPU, or API keys required.
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

echo "Running Watch demo (mock mode — no downloads needed)..."
echo ""
python3 demo.py

echo ""
echo "Demo complete. To process a real video, install dependencies:"
echo "  pip install yt-dlp mlx-whisper Pillow"
echo "  brew install ffmpeg"
echo "  python3 watch.py '<VIDEO_URL>'"
