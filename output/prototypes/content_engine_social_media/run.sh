#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Content Engine - Social Media Pipeline"
echo "======================================="
echo ""

# Install deps if needed (only stdlib is required for mock mode)
if [ -f requirements.txt ]; then
    pip install -q -r requirements.txt 2>/dev/null || true
fi

# Run with a demo topic
python3 content_engine.py "AI-Powered Analytics Dashboard"

# Show generated files
echo "Generated files:"
ls -la output/ 2>/dev/null || true
echo ""

# Display one post as example
if [ -f output/post_twitter.txt ]; then
    echo "--- Sample: Twitter Post ---"
    cat output/post_twitter.txt
    echo ""
    echo "----------------------------"
fi
