#!/usr/bin/env bash
# Rare Disease Diagnostic Assistant — end-to-end demo
# No API keys required. Uses mock patient data + built-in disease KB.
set -e

cd "$(dirname "$0")"

echo "--- Installing dependencies (if needed) ---"
pip install -q -r requirements.txt 2>/dev/null || true

echo "--- Running diagnostic demo ---"
python3 demo.py
