#!/usr/bin/env bash
set -euo pipefail

echo "Markifact MCP Ads Management — Demo"
echo ""

# Check Node.js availability
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not installed."
  echo "Install from https://nodejs.org/ (v18+)"
  exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "WARNING: Node.js 18+ recommended. Found: $(node -v)"
fi

# Run the mock server demo (no external deps needed)
node "$(dirname "$0")/mock_server.js"
