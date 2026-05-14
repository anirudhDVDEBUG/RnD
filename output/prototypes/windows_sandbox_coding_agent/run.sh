#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Windows Sandbox Coding Agent Demo ==="
echo ""

# Install deps if needed (none beyond stdlib, but keep the pattern)
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

python3 demo.py
