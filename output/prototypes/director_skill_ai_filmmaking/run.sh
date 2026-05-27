#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  Director SKILL — AI Filmmaking Demo                               ║"
echo "║  Generates shot lists, keyframe & video prompts in director styles  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# No external dependencies needed — pure Python 3 stdlib
python3 director_skill.py

echo ""
echo "── JSON export (first scene only) ─────────────────────────────────────"
echo ""
python3 -c "
from director_skill import process_scene, export_json
b = process_scene('A lone astronaut discovers a garden growing inside an abandoned space station.', 'tarkovsky', 'runway')
print(export_json(b))
" | head -30
echo "  ... (truncated)"

echo ""
echo "Done. See HOW_TO_USE.md for Claude Code skill installation."
