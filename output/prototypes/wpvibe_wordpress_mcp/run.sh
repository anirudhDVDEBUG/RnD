#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=== WPVibe WordPress MCP — Demo ==="
echo ""
echo "[1/2] Starting mock WPVibe MCP server on port 3100..."

# Start mock server in background
node server.js &
SERVER_PID=$!

# Give the server a moment to bind
sleep 1

# Verify server is up
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "ERROR: Server failed to start."
  exit 1
fi

cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

# Run the demo client
echo "[2/2] Running demo client..."
echo ""
node demo-client.js

echo ""
echo "Server stopped. Demo complete."
