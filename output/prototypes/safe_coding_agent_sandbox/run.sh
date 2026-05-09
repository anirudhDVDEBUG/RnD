#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Safe Coding Agent Sandbox ==="
echo "Running end-to-end security demo..."
echo ""

python3 demo.py
