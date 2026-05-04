#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "-------------------------------------------"
echo " Kagi Session MCP Server — Demo"
echo "-------------------------------------------"
echo ""

# Check Python version
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found."
    exit 1
fi

PYVER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PYVER"
echo ""

# Run demo mode (produces visible output without needing a session token)
python3 "$SCRIPT_DIR/server.py" --demo
