#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== DemandBird Social Media Management — Demo ==="
echo ""

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --no-fund --no-audit 2>&1
  echo ""
fi

# Run the demo
node demo.js
