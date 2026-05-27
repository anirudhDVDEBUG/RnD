#!/usr/bin/env bash
# End-to-end demo of Hermes Dreaming staged self-improvement engine.
# No API keys needed — uses built-in mock interaction data.

set -euo pipefail
cd "$(dirname "$0")"

# Clean previous demo data
rm -rf .hermes_data

echo "============================================"
echo " Hermes Dreaming  —  Staged Self-Improvement"
echo "============================================"
echo

# Step 1: Dream — analyze interactions, generate proposals
echo "--- STEP 1: Dream (analyze mock interactions, propose updates) ---"
echo
python -m hermes_dreaming dream
echo

# Step 2: Review — inspect all staged proposals
echo "--- STEP 2: Review (inspect staged proposals) ---"
echo
python -m hermes_dreaming review
echo

# Step 3: Approve all proposals
echo "--- STEP 3: Approve all proposals ---"
echo
python -m hermes_dreaming approve --all
echo

# Step 4: Apply approved changes to knowledge base
echo "--- STEP 4: Apply (write approved changes to knowledge base) ---"
echo
python -m hermes_dreaming apply
echo

# Step 5: Show final status
echo "--- STEP 5: Final status ---"
echo
python -m hermes_dreaming status
echo

echo "============================================"
echo " Done. Data stored in .hermes_data/"
echo "============================================"
echo
echo "Try it interactively:"
echo "  python -m hermes_dreaming dream"
echo "  python -m hermes_dreaming review"
echo "  python -m hermes_dreaming approve <id>"
echo "  python -m hermes_dreaming discard <id>"
echo "  python -m hermes_dreaming apply"
