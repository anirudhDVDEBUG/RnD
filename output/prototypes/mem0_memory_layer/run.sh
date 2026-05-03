#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== mem0 Memory Layer Demo ==="
echo ""

# Create and activate a venv if not already in one
if [ -z "${VIRTUAL_ENV:-}" ]; then
    if [ ! -d ".venv" ]; then
        echo "[setup] Creating virtual environment..."
        python3 -m venv .venv
    fi
    echo "[setup] Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies
echo "[setup] Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "[run] Starting demo..."
echo ""

python3 demo_memory_layer.py
