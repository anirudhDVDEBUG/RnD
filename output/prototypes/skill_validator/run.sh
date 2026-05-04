#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "============================================"
echo "  Skill Validator — SKILL.md Audit Tool"
echo "============================================"
echo ""

echo "▶ Auditing samples/good_skill.md (well-structured skill)..."
echo "--------------------------------------------"
python3 skill_validator.py samples/good_skill.md || true
echo ""

echo "▶ Auditing samples/medium_skill.md (decent but improvable)..."
echo "--------------------------------------------"
python3 skill_validator.py samples/medium_skill.md || true
echo ""

echo "▶ Auditing samples/bad_skill.md (poor quality)..."
echo "--------------------------------------------"
python3 skill_validator.py samples/bad_skill.md || true
echo ""

echo "▶ JSON output mode (good_skill.md)..."
echo "--------------------------------------------"
python3 skill_validator.py --json samples/good_skill.md || true
echo ""

echo "============================================"
echo "  Done. Run on your own skill:"
echo "  python3 skill_validator.py path/to/SKILL.md"
echo "============================================"
