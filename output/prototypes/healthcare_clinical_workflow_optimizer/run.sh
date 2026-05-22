#!/usr/bin/env bash
# Healthcare Clinical Workflow Optimizer — end-to-end demo
# No API keys required; runs entirely on mock data.
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking Python version..."
python3 --version

echo "Running Healthcare Clinical Workflow Optimizer demo..."
echo ""
python3 demo.py
