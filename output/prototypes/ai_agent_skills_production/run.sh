#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies (stdlib only - nothing to install)..."
pip install -r requirements.txt --quiet 2>/dev/null || true

echo ""
python3 demo.py
