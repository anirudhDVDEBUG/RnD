#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "  Mythos Skill Forge — Demo"
echo "============================================================"
echo ""

# Clean previous demo output
rm -rf demo_output

# 1. List available presets
echo "--- Available Preset Templates ---"
python3 skill_forge.py list-presets

# 2. Forge a skill from a preset (code_review)
echo "--- Forging from preset: code_review ---"
python3 skill_forge.py forge --preset code_review --output demo_output/skills

# 3. Forge a custom skill from CLI args
echo "--- Forging custom skill: lead_scorer ---"
python3 skill_forge.py forge \
  --name lead_scorer \
  --title "Lead Scorer" \
  --desc "Scores and ranks inbound leads based on engagement signals and ICP fit." \
  --triggers "score these leads,rank my leads,evaluate lead quality" \
  --steps "Ingest lead data from CSV or CRM export,Score each lead on engagement and ICP fit,Rank leads by composite score,Generate a prioritized outreach list" \
  --hooks --templates \
  --output demo_output/skills

# 4. Run the full demo (all presets + custom + audit)
echo "--- Full Demo (forge all presets + audit) ---"
python3 skill_forge.py demo

# 5. Show generated files
echo ""
echo "--- Generated File Tree ---"
find demo_output -type f | sort
echo ""
echo "--- Sample SKILL.md (code_review_agent) ---"
cat demo_output/skills/code_review_agent/SKILL.md
echo ""
echo "============================================================"
echo "  Demo complete. All skills forged and audited."
echo "============================================================"
