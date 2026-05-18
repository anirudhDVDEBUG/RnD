#!/usr/bin/env bash
# Runa Digital Being Agent — end-to-end demo
# Runs without external API keys (uses mock LLM)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing dependencies..."
pip install -q -r requirements.txt

# Clean previous run state
rm -f logs/memory.json logs/goals.json logs/agent.log

echo ""
python main.py
