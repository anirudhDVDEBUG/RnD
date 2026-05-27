#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════╗"
echo "║  AI Video Production Kit — run.sh            ║"
echo "║  No API keys needed · Pure demo mode         ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

python3 video_prompt_engine.py

echo ""
echo "Done. To try interactive mode:  python3 video_prompt_engine.py --interactive"
