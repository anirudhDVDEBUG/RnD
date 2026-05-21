#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "--- High-Quality Slides Demo ---"
echo ""

# Generate both available sample decks
python3 generate_slides.py ai-agents -o slides_ai_agents.html --json
echo ""
echo "========================================="
echo ""
python3 generate_slides.py claude-skills -o slides_claude_skills.html
echo ""
echo "========================================="
echo "Generated 2 sample slide decks."
echo "Open either HTML file in a browser to present."
