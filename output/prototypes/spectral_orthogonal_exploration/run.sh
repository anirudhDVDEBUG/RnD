#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
python soe.py
