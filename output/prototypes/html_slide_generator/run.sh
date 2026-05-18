#!/usr/bin/env bash
set -euo pipefail

echo "=== HTML Slide Generator Demo ==="
echo ""

cd "$(dirname "$0")"
python3 generate_slides.py

echo ""
echo "=== Done! ==="
echo "To install the Claude Code skill:"
echo "  mkdir -p ~/.claude/skills/html_slide_generator"
echo "  cp SKILL.md ~/.claude/skills/html_slide_generator/SKILL.md"
