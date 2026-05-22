#!/usr/bin/env bash
# Run the datasette-agent-sprites mock demo
# No API keys or external services required

set -e

cd "$(dirname "$0")"

echo "Running datasette-agent-sprites sandbox demo..."
echo ""

python3 mock_sprites_plugin.py
