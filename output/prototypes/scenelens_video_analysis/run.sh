#!/usr/bin/env bash
# SceneLens Demo — runs end-to-end mock pipeline
# No external API keys or system deps required

set -e

cd "$(dirname "$0")"

echo "SceneLens Video Analysis — Demo"
echo ""

# Clean previous output
rm -rf demo_output

# Run the mock pipeline
python3 demo_scenelens.py
