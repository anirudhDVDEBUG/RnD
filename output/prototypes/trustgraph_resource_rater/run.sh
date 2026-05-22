#!/usr/bin/env bash
# TrustGraph Resource Rater — end-to-end demo
# Generates mock trust data and prints the aggregate report.
# No API keys required.
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking Python 3..."
python3 --version

echo ""
echo "Running TrustGraph demo with mock data..."
echo ""

python3 demo_mock.py
