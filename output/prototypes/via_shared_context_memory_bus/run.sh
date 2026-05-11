#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=== Via Shared Context & Memory Bus — Demo ==="
echo ""

# Clean previous data so each run starts fresh
rm -f .via_data.json

# Install dependencies if needed
if [ ! -d node_modules ]; then
  echo "Installing dependencies..."
  npm install --no-fund --no-audit 2>&1 | tail -3
  echo ""
fi

echo "Running demo: multi-tool workflow over the Via MCP bus..."
echo ""

node demo_client.js
