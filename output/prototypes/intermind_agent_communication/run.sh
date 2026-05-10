#!/usr/bin/env bash
set -euo pipefail

echo "──────────────────────────────────────────────────────────"
echo "  Intermind Agent Communication — Demo Runner"
echo "──────────────────────────────────────────────────────────"
echo ""

# Check for Node.js (>=18 for ESM + crypto)
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not found."
  echo "Install it: https://nodejs.org/"
  exit 1
fi

NODE_VERSION=$(node -e "console.log(process.versions.node.split('.')[0])")
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "ERROR: Node.js >= 18 required (found v${NODE_VERSION})."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running multi-agent conversation demo..."
echo ""

node "$SCRIPT_DIR/demo_conversation.js"

echo "Done. See HOW_TO_USE.md for setup instructions with the real Intermind MCP server."
