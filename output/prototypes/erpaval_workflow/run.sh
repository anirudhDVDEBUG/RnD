#!/usr/bin/env bash
# ERPAVal Workflow Demo — runs end-to-end with mock data, no API keys needed.
set -euo pipefail
cd "$(dirname "$0")"

echo "Installing dependencies (stdlib only — no external packages required)..."
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

echo ""
python3 demo.py
