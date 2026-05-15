#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "  Qobrix CRM MCP Server — Evaluation Demo"
echo "=============================================="
echo ""

# Install deps if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --silent 2>&1 | tail -1
  echo ""
fi

echo "Running demo queries against mock CRM data..."
echo "(No API keys required — uses built-in mock data)"
echo ""

node demo.js
