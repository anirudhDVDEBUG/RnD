#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== CSP Allow-list Sandbox ==="
echo ""

# Check for Node.js
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not found."
  echo "Install it from https://nodejs.org or via your package manager."
  exit 1
fi

echo "Starting static file server on http://localhost:8090 ..."
echo "Open the URL in your browser to use the sandbox."
echo "Press Ctrl+C to stop."
echo ""

# No npm install needed — zero dependencies, uses Node built-in http module.
node server.js
