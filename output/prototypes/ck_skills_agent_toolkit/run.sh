#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Clean previous demo output
rm -rf demo_output

echo "Running ck-skills Agent Toolkit demo..."
echo ""

python3 ck_skills_browser.py

echo ""
echo "--- Demo output files ---"
find demo_output -type f | sort
