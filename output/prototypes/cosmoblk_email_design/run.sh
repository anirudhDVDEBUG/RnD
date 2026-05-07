#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════╗"
echo "║  CosmoBlk Email Design — Demo Runner     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Install dependencies if needed
if [ ! -d node_modules ]; then
  echo "→ Installing dependencies (mjml)..."
  npm install --no-audit --no-fund --loglevel=error
  echo ""
fi

echo "─── 1. Single archetype: Welcome email ───"
node index.js welcome generic
echo ""

echo "─── 2. All six archetypes at once ───"
node generate_all.js

echo "─── 3. ESP-specific merge tags (Klaviyo) ───"
node index.js promotional klaviyo
echo ""

echo "✓ All done. Check the output/ directory for .mjml and .html files."
echo "  Open any .html file in a browser to see the rendered email."
