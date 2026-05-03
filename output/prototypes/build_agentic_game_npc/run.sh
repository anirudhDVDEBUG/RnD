#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
pip install -q pyyaml 2>/dev/null || pip install -q --user pyyaml

echo ""
echo "=== Running Agentic Game NPC Demo ==="
echo "(Using mock AI client — set ANTHROPIC_API_KEY to use live Claude)"
echo ""

python3 main.py
