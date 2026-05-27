#!/usr/bin/env bash
# AI Policy Influence Analyst — end-to-end demo
# No API keys required. Uses mock policy data.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Running AI Policy Influence Analyst demo..."
echo ""

python3 analyst.py
