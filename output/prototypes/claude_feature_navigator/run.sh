#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Claude Feature Navigator — Skill Discovery Demo ==="
echo ""
python3 navigator.py
