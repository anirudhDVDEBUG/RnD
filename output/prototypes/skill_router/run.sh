#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Skill Router Demo ==="
echo ""

# Part 1: Built-in demo with mock skills (in-memory)
python3 skill_router.py --demo

echo ""
echo "─────────────────────────────────────────────────────────────"
echo "  Part 2: CLI mode — scanning mock_skills/ directory"
echo "─────────────────────────────────────────────────────────────"
echo ""

# Part 2: CLI mode scanning real SKILL.md files from disk
python3 skill_router.py "I want to check my site's SEO" --skills-dir mock_skills
echo ""
python3 skill_router.py "Generate Facebook ads for my product launch" --skills-dir mock_skills --auto
echo ""
python3 skill_router.py "Build a landing page for our new feature" --skills-dir mock_skills --json
