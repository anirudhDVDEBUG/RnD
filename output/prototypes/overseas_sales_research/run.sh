#!/usr/bin/env bash
# Overseas Sales Research – Demo Runner
# Generates a sample 五看六定 report for Siemens AG in Southeast Asia
set -euo pipefail
cd "$(dirname "$0")"

echo "=============================================="
echo " Overseas Sales Research Report Generator"
echo " Framework: 五看六定 (Five Perspectives,"
echo "            Six Decisions)"
echo "=============================================="
echo ""

python3 generate_report.py \
  --company "Siemens AG" \
  --industry "Industrial Automation & Digitalization" \
  --market "Southeast Asia" \
  --purpose "Distributor Evaluation" \
  --lang zh

echo ""
echo "Done. Full report saved to the .md file above."
