#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== PRTS Agent Terminal Service — Demo ==="
echo ""

# Create venv if missing
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install -q -r requirements.txt

echo ""
python3 main.py --demo
