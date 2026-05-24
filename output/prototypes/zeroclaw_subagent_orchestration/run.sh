#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo ">>> ZeroClaw Subagent Orchestration Demo"
echo ">>> Python: $(python3 --version)"
echo ""

python3 demo.py
