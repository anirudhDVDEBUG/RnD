#!/usr/bin/env bash
# AI Media Prompt Generator — end-to-end demo
# Generates senior-director-level prompts for 14+ AI media platforms.
# No API keys required.

set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo "  AI Media Prompt Generator — Demo"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found."
  exit 1
fi

# Install deps (stdlib only, but keep the workflow consistent)
if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt 2>/dev/null || true
fi

python3 media_prompt_generator.py
