#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  AI Short Film Prompt Generator — Demo"
echo "============================================================"
echo ""

# 1. List supported models
echo "--- Supported Models ---"
python3 generate_prompts.py --list-models
echo ""

# 2. Full Markdown output (default model: Veo)
echo "--- Full Prompt Document (Veo, Markdown) ---"
python3 generate_prompts.py --format markdown
echo ""

# 3. Re-target to Sora — show raw prompts only
echo "============================================================"
echo "--- Raw Prompts Re-targeted to Sora ---"
echo "============================================================"
python3 generate_prompts.py --format prompts --model sora
echo ""

# 4. Single scene as JSON
echo "============================================================"
echo "--- Scene 4 as JSON (Kling) ---"
echo "============================================================"
python3 generate_prompts.py --format json --model kling --scene 4
echo ""

echo "============================================================"
echo "  Done. 10 shots, 5 models supported, 3 output formats."
echo "  See HOW_TO_USE.md for Claude Code skill installation."
echo "============================================================"
