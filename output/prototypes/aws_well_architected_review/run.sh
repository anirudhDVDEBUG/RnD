#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=========================================="
echo "  AWS Well-Architected Review — Demo Run"
echo "=========================================="
echo ""

# No external dependencies needed (stdlib only)
python3 wa_reviewer.py samples/

echo ""
echo "Done. See HOW_TO_USE.md for Claude Code skill installation."
