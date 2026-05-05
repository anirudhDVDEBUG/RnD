#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== MetalBear Skills Registry Demo ==="
echo ""

# Ensure clean state for demo
rm -rf .claude/skills

echo "--- Listing all available skills ---"
python3 skills_registry.py list

echo "--- Searching for 'kubernetes' ---"
python3 skills_registry.py search "kubernetes"

echo "--- Searching for 'test' ---"
python3 skills_registry.py search "test"

echo "--- Showing details for 'pytest-gen' ---"
python3 skills_registry.py show pytest-gen

echo "--- Installing 'pytest-gen' locally ---"
python3 skills_registry.py install pytest-gen

echo ""
echo "--- Verifying installation ---"
echo "Installed file:"
ls -la .claude/skills/pytest-gen.md
echo ""
echo "Contents:"
cat .claude/skills/pytest-gen.md

echo ""
echo "=== Demo Complete ==="
echo ""
echo "To install the registry skill into your Claude Code setup:"
echo "  mkdir -p ~/.claude/skills/metalbear_skills_registry"
echo "  cp SKILL.md ~/.claude/skills/metalbear_skills_registry/SKILL.md"
