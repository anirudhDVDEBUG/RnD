#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== McClaude Minecraft Dev Bridge — Demo ==="
echo ""

# Install dependencies
if [ ! -d "node_modules" ]; then
  echo "[setup] Installing dependencies..."
  npm install --no-audit --no-fund 2>&1 | tail -1
  echo ""
fi

# Run the demo
node demo.js
