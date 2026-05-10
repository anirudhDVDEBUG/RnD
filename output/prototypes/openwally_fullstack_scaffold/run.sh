#!/usr/bin/env bash
# OpenWally Full-Stack Scaffold — Mock Demo
# Runs the multi-agent pipeline simulation without API keys.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "────────────────────────────────────────────────────────"
echo " OpenWally Full-Stack Scaffold — Mock Demo"
echo "────────────────────────────────────────────────────────"
echo ""

# Clean previous run
rm -rf generated_project

# Run mock pipeline
python3 openwally_mock.py \
  "A task management app with user auth, project boards, and real-time notifications"

echo ""
echo "────────────────────────────────────────────────────────"
echo " Verifying generated scaffold..."
echo "────────────────────────────────────────────────────────"

# Show the generated tree
if command -v tree &>/dev/null; then
  tree generated_project
else
  find generated_project -type f | sort
fi

echo ""
echo "Generated manifest:"
cat generated_project/openwally_manifest.json
echo ""
echo "Done. See HOW_TO_USE.md for real OpenWally setup."
