#!/usr/bin/env bash
# run.sh — Execute the OpenSquilla token-efficient agent demo
# No API keys required. Uses mock LLM backend.
set -euo pipefail

cd "$(dirname "$0")"

echo ">> Checking Python..."
python3 --version

echo ">> Running OpenSquilla agent demo..."
python3 demo.py

echo ">> Done."
