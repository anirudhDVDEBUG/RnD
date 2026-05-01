#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo "==> Running Claude Code Workflow demo..."
python3 claude_code_sim.py
