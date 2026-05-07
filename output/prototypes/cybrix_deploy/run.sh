#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q pyyaml

echo ""
python3 cybrix_sim.py
