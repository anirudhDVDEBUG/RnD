#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo ">>> Installing dependencies (stdlib only — nothing to install)"
echo ""

echo ">>> Running GPT-5.5 Instant overview demo..."
echo ""

python3 gpt55_overview.py
