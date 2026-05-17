#!/usr/bin/env bash
# Claude Code Swarm Toolkit — Demo Runner
# No API keys required. Uses Python standard library only.

set -e

cd "$(dirname "$0")"

echo "Checking Python availability..."
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "ERROR: Python 3 is required but not found."
    exit 1
fi

echo "Using: $($PYTHON --version)"
echo ""

$PYTHON swarm_demo.py
