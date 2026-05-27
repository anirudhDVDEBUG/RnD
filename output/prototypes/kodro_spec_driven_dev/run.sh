#!/usr/bin/env bash
# Kodro Spec-Driven Development — end-to-end demo
# Runs the 6-phase pipeline on a sample JWT auth spec.
# No API keys or external deps needed.
set -e

cd "$(dirname "$0")"

echo "Checking Python..."
python3 --version

echo ""
echo "Running Kodro SDD pipeline demo..."
echo ""

python3 demo.py
