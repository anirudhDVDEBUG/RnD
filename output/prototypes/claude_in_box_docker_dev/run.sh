#!/usr/bin/env bash
# run.sh — Claude-in-Box simulator: runs end-to-end with no API keys.
# Produces CLI output showing multi-session management, hook engine,
# and resource monitoring.  Pass --serve to also start the web UI.

set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-$(command -v python3 || command -v python)}"

echo "Installing dependencies..."
"$PYTHON" -m pip install -q -r requirements.txt 2>/dev/null || true

echo ""
"$PYTHON" simulator.py
