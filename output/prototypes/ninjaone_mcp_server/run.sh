#!/usr/bin/env bash
# run.sh — Execute the NinjaOne MCP Server mock demo
# No API keys or external services required.

set -euo pipefail
cd "$(dirname "$0")"

echo "Running NinjaOne MCP Server demo (mock data)..."
echo ""

python3 ninjaone_mcp_server.py
