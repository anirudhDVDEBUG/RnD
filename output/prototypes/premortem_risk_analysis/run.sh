#!/usr/bin/env bash
# Premortem Risk Analysis — end-to-end demo
# Runs without external API keys. Uses mock data to demonstrate
# the full premortem pipeline: prospective hindsight, multi-agent scan,
# mitigation triplets, reverse-premortem, and snapshot export.

set -euo pipefail
cd "$(dirname "$0")"

echo "=== Premortem Risk Analysis Demo ==="
echo ""
echo "Running premortem on sample plan: 'Migrate billing to event-driven architecture'"
echo ""

python3 premortem_demo.py

echo ""
echo "--- Generated artifacts ---"
echo "  premortem_snapshot.md   (markdown report)"
echo "  premortem_snapshot.json (structured data)"
echo ""
echo "To use the actual Claude Code skill, copy SKILL.md to:"
echo "  ~/.claude/skills/premortem_risk_analysis/SKILL.md"
echo "Then say 'premortem' or 'what could go wrong' in Claude Code."
