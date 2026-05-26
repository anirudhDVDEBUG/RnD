#!/usr/bin/env bash
set -euo pipefail

# ── plumb-mcp demo ──────────────────────────────────────────────────
# Runs the full design-to-code pipeline using mock Figma data.
# No Figma account, API key, or network access required.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  plumb-mcp  —  Figma Design-to-Code Demo"
echo "============================================"
echo ""

# Check Node.js is available
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not found."
  echo "Install it: https://nodejs.org/ or 'nvm install 20'"
  exit 1
fi

NODE_VERSION=$(node -v)
echo "Using Node.js ${NODE_VERSION}"
echo ""

# No npm install needed — zero external dependencies
echo "Running demo (mock Figma data, no API keys needed)..."
echo ""

node demo.js
