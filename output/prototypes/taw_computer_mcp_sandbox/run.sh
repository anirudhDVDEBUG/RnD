#!/usr/bin/env bash
# taw-computer MCP sandbox demo — runs without Docker or API keys
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Running taw-computer MCP capability demo..."
echo ""
node demo.mjs
