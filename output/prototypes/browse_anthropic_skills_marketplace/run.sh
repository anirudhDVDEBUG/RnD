#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Anthropic Skills Marketplace Browser ==="
echo "No external dependencies required — pure Python 3."
echo ""

python3 skills_browser.py
