#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Public-Channel Coding Agent Workflow ==="
echo "No external API keys required -- runs with mock data."
echo ""

# Install deps (stdlib only, but keep the pattern)
if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt 2>/dev/null || true
fi

python3 demo.py
