#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "OncoAgent — Clinical Decision Support Demo"
echo "No external dependencies required (pure Python 3.8+)"
echo ""

python3 main.py
