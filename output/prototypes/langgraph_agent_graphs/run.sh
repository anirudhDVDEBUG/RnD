#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installing dependencies ==="
pip install -q -r requirements.txt 2>&1 | tail -1

echo ""
echo "=== Running LangGraph Agent Graph Demo ==="
echo ""
python agent_graph.py
