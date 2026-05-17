#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Multi-Agent Market Lab — Setting up..."

# Create venv if needed
if [ ! -d ".venv" ]; then
    python3 -m venv .venv 2>/dev/null || true
fi

# No external deps required — stdlib only
echo "No external dependencies needed (pure Python stdlib)."
echo ""

python3 demo.py
