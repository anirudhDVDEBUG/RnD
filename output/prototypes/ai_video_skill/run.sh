#!/usr/bin/env bash
# AI Video Skill — end-to-end demo (mock mode, no API keys needed)
set -euo pipefail

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "=== Single Prompt Demo ==="
python3 video_skill.py --prompt "A dancer spinning under neon lights in slow motion"

echo ""
echo "=== Multi-Model Sweep ==="
python3 video_skill.py --all-models

echo ""
echo "Generated files:"
ls -lh output/ 2>/dev/null || echo "(no output dir)"
