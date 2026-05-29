#!/usr/bin/env bash
# run.sh — Run the brain.md MCP demo end-to-end
# Produces visible output without any external API keys or dependencies.
set -euo pipefail
cd "$(dirname "$0")"

echo "brain.md MCP Server — Demo Mode"
echo "================================"
echo ""

python3 demo_brain_md.py

echo ""
echo "--- Vault contents created by demo ---"
find demo_vault -type f -name '*.md' | sort
echo ""
echo "Done. See HOW_TO_USE.md for real install instructions."
