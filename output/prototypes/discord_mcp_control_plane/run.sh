#!/usr/bin/env bash
# Discord MCP Control Plane — end-to-end demo
# No API keys or network access required.
set -euo pipefail
cd "$(dirname "$0")"

echo "────────────────────────────────────────────────────────"
echo " Discord MCP Control Plane — mock demo"
echo " (runs entirely offline with synthetic Discord data)"
echo "────────────────────────────────────────────────────────"
echo

python3 demo.py
