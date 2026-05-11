#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Verdandi Unix Socket Agent Awareness Demo"
echo "============================================"
echo ""

# Clean up any stale socket from a previous run
rm -f /tmp/verdandi_demo.sock

# Run the demo
python3 "$SCRIPT_DIR/demo.py"
