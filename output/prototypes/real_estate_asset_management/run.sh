#!/usr/bin/env bash
# Real Estate Asset Management — Demo Runner
# Produces a full Quarterly Asset Review from mock portfolio data.
# No API keys or external services required.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Running Real Estate Asset Management analysis..."
echo ""

python3 asset_analyzer.py
