#!/usr/bin/env bash
# Ringback Voice Call MCP — Demo Runner
# Runs the full demo in mock mode (no SIP infrastructure required).
set -euo pipefail
cd "$(dirname "$0")"

echo "Setting up Ringback Voice Call MCP demo..."
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found."
    exit 1
fi

# No external deps needed for the demo — stdlib only
echo "No external dependencies required (stdlib only)."
echo ""

# Run the demo
python3 demo.py
