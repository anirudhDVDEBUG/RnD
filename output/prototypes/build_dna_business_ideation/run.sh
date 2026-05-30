#!/usr/bin/env bash
# Build DNA — Business Ideation Demo
# Runs the full 3-phase workflow with a mock founder profile.
# No API keys required.

set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Installing dependencies (stdlib only — nothing to install)..."
echo ">>> Running Build DNA demo..."
echo

python3 demo.py

echo ">>> Done. See output.json for structured results."
