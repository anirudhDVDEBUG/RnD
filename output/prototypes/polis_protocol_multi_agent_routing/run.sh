#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Polis Protocol — Multi-Agent Routing Demo"
echo ""

# Clean previous ledger so each run is fresh
rm -f .polis/lessons/ledger.json .polis/lessons/ledger.md

# No external dependencies needed (stdlib only)
python3 demo.py
