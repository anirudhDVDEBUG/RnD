#!/usr/bin/env bash
# Overkill Demo — runs the enterprise-grade addition service
set -euo pipefail

cd "$(dirname "$0")"
echo "Running Enterprise Addition Service demo..."
echo ""
python3 overkill_demo.py
