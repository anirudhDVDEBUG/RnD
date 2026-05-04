#!/usr/bin/env bash
# Anthropic Grade Optimizer — Demo run
# Audits a sample CLAUDE.md against Anthropic best-practice rules.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Anthropic Grade Optimizer"
echo "========================="
echo ""
echo "Auditing sample_claude.md against 189 Anthropic rules..."
echo ""

python3 audit.py sample_claude.md

echo ""
echo "---"
echo "JSON output mode:"
echo ""
python3 audit.py sample_claude.md --json
