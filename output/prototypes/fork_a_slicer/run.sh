#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "--- Fork-a-Slicer: Process Isolation Bridge Demo ---"
echo ""

# Verify Python is available
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found on PATH."
    exit 1
fi

# Clean up any stale socket from a previous run
[ -S /tmp/bambu_bridge.sock ] && rm -f /tmp/bambu_bridge.sock

# Run the orchestrator
python3 "$SCRIPT_DIR/demo.py"
