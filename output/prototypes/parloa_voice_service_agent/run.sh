#!/usr/bin/env bash
# Parloa Voice Service Agent — end-to-end demo
# Runs the simulation harness against 5 test scenarios (no API keys needed).

set -euo pipefail
cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null

echo ""
python3 simulator.py
