#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
python3 demo.py
