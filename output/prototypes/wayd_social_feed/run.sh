#!/usr/bin/env bash
# WAYD Social Feed - Demo runner
# Runs the mock feed demo (no API keys or network access needed).
set -euo pipefail

cd "$(dirname "$0")"

echo "=== WAYD Social Feed Demo ==="
echo ""

# Install deps (stdlib only, but honour the requirements.txt convention)
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

python3 wayd_demo.py
