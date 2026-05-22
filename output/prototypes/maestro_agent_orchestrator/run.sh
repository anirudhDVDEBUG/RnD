#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Maestro Agent Orchestrator Demo ==="
echo ""

# Install dependencies
if command -v pip3 &>/dev/null; then
    pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt 2>/dev/null
elif command -v pip &>/dev/null; then
    pip install -q -r requirements.txt 2>/dev/null
else
    echo "Warning: pip not found, assuming pyyaml is already installed"
fi

# Run demo
python3 demo.py
