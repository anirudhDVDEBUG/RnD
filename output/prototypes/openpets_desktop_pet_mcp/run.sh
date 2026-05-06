#!/usr/bin/env bash
# OpenPets Desktop Pet MCP Demo
# Simulates the MCP server + pet animation loop without needing Electron or Bun.
set -euo pipefail
cd "$(dirname "$0")"

echo "=== OpenPets Desktop Pet MCP Demo ==="
echo ""

# Check for Node.js
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not found. Install it from https://nodejs.org"
  exit 1
fi

node demo.mjs
