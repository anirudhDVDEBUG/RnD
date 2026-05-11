#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "--- Honeydew Semantic Layer Demo (mock data, no API key needed) ---"
echo ""
python3 demo.py
