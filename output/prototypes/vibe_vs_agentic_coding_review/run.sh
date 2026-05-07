#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Running Vibe Coding vs Agentic Engineering Review Tool"
echo ""

python3 review_diff.py
