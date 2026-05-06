#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo " Claude Pets — Desktop Pet Demo"
echo "=========================================="
echo ""

# Check for Node.js (>= 18 for ES modules + top-level await)
if ! command -v node &> /dev/null; then
  echo "ERROR: Node.js is required but not found."
  echo "Install it: https://nodejs.org/ (v18+)"
  exit 1
fi

NODE_VERSION=$(node -e "console.log(process.versions.node.split('.')[0])")
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "ERROR: Node.js 18+ required (found v${NODE_VERSION})"
  exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "--- Part 1: Hook Simulation ---"
echo ""
echo "[on_session_start]"
node "$DIR/hooks/on_session_start.js"
echo ""

echo "[on_tool_call] (Read)"
echo '{"tool_name":"Read"}' | node "$DIR/hooks/on_tool_call.js"
echo ""

echo "[on_tool_call] (Edit)"
echo '{"tool_name":"Edit"}' | node "$DIR/hooks/on_tool_call.js"
echo ""

echo "[on_tool_call] (Bash)"
echo '{"tool_name":"Bash"}' | node "$DIR/hooks/on_tool_call.js"
echo ""

echo "[on_session_end]"
node "$DIR/hooks/on_session_end.js"
echo ""

echo "--- Part 2: MCP Server Tools ---"
echo ""
node "$DIR/src/mcp-server.js"
echo ""

echo "--- Part 3: Full Session Simulation ---"
echo ""
node "$DIR/src/demo.js"

echo ""
echo "Done. See HOW_TO_USE.md for real setup instructions."
