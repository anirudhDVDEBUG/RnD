#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Redis Development Patterns Demo ==="
echo ""

# Create virtualenv if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
python3 redis_demo.py
