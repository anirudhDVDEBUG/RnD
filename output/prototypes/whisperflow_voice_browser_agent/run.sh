#!/usr/bin/env bash
# WhisperFlow Voice Browser Agent — mock demo
# Runs end-to-end without API keys, mic, or browser install.
set -euo pipefail

cd "$(dirname "$0")"

echo "==> WhisperFlow Voice Browser Agent — Demo"
echo ""

# Force mock mode so no external deps are needed
export WHISPERFLOW_MOCK=1
export WHISPERFLOW_MAX_COMMANDS=5

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.10+."
    exit 1
fi

echo "==> Running mock demo (no API keys / hardware required)..."
echo ""

python3 main.py

echo ""
echo "==> Demo complete. See HOW_TO_USE.md for live mode instructions."
