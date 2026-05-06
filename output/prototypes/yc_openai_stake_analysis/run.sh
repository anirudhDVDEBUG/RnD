#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== YC OpenAI Stake Analysis ==="
echo ""
python3 yc_openai_analysis.py
