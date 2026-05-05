#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q httpx 2>/dev/null || true

echo ">>> Running demo (mock mode — no API key required)..."
echo
MOCK=1 python3 demo.py
