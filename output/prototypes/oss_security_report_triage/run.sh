#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing dependencies..."
pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || true

echo ""
python3 "$SCRIPT_DIR/triage.py"
