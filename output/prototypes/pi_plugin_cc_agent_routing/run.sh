#!/usr/bin/env bash
set -euo pipefail

echo "=== Pi Plugin for Claude Code — Demo ==="
echo ""

# Check Node.js is available
if ! command -v node &> /dev/null; then
  echo "ERROR: Node.js is required but not found. Install Node >= 16."
  exit 1
fi

cd "$(dirname "$0")"

# No external deps to install — zero dependencies
echo "Running tests..."
node test.js
echo ""
echo "Running demo..."
echo ""
node demo.js
