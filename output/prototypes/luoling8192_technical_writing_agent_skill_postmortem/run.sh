#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking Python version..."
python3 --version

echo ""
echo "Running postmortem generator demo..."
echo ""

python3 postmortem_generator.py
