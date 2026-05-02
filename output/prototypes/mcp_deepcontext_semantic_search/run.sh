#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== mcp-deepcontext Semantic Search Demo ==="
echo ""
echo "No external API keys required — this demo uses a local mock"
echo "that mirrors the real MCP server's symbol extraction + search."
echo ""

node demo.js
