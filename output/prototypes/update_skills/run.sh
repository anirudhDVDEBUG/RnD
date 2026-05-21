#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  update-skills demo"
echo "  Keep Claude Code skills up-to-date"
echo "============================================"
echo ""

# Run the demo with mock skills data (no API keys or network needed)
python3 "$SCRIPT_DIR/update_skills.py" --demo

echo "--------------------------------------------"
echo "  Demo complete."
echo "  In real usage, install the SKILL.md into"
echo "  ~/.claude/skills/update-skills/ and say"
echo "  'update my skills' in Claude Code."
echo "--------------------------------------------"
