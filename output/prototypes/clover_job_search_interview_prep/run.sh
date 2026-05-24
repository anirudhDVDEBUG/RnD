#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Clover Job Search & Interview Prep — Demo ==="
echo "No API keys required (uses mock data)."
echo ""

python3 clover_demo.py
