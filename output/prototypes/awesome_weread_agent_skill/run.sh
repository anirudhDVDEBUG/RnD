#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Clean previous output
rm -rf output/

echo "Running Awesome WeRead Agent Skill Demo..."
echo ""

python3 weread_demo.py

echo ""
echo "Generated files:"
find output/ -type f | sort
