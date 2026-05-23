#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo " Build Ship Grow -- Content Strategy Demo"
echo "=========================================="
echo ""

# Run the demo with the built-in mock product
python3 content_strategy.py

echo ""
echo "--- JSON output mode (truncated) ---"
echo ""
python3 content_strategy.py --json | head -40
echo "  ... (truncated, run with --json for full output)"

echo ""
echo "--- Custom product example ---"
echo ""
python3 content_strategy.py \
  --name "VoiceBot Pro" \
  --tagline "Add voice AI to any app in 5 lines of code" \
  --audience "SaaS developers" \
  --stage grow \
  | head -50
echo "  ... (truncated)"

echo ""
echo "Done. See HOW_TO_USE.md for Claude Code skill installation."
