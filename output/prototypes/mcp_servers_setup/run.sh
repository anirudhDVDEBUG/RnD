#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "############################################################"
echo "#  MCP Servers Setup — Demo                                #"
echo "############################################################"
echo ""

cd "$(dirname "$0")"

# Part 1: Config generator — catalog + sample configs
echo ">>> Part 1: MCP Config Generator"
echo ""
python3 mcp_config_generator.py

# Part 2: Demo MCP server — protocol walkthrough
echo ""
echo ">>> Part 2: Demo MCP Server (JSON-RPC protocol walkthrough)"
echo ""
python3 demo_mcp_server.py

echo ""
echo "Done. See HOW_TO_USE.md for real setup instructions."
