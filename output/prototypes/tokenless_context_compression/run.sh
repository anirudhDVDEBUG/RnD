#!/usr/bin/env bash
# Tokenless Context Compression — end-to-end demo
# No external API keys required. Runs entirely locally.
set -euo pipefail
cd "$(dirname "$0")"

echo "Tokenless Context Compression Demo"
echo "==================================="
echo ""
echo "Running compression on sample_project/ ..."
echo ""

node demo.js
