#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ">> Installing dependencies..."
npm install --no-fund --no-audit 2>&1 | tail -1

echo ""
echo ">> Running Second Brain MCP demo..."
echo ""
node src/demo.js
