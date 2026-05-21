#!/usr/bin/env bash
# run.sh — end-to-end demo of YouTube Research MCP tools
# Works without API keys (uses built-in mock data)
set -e

cd "$(dirname "$0")"

echo "── Installing dependencies (quiet) ──"
pip install -q youtube-transcript-api 2>/dev/null || true

echo "── Running demo ──"
python -m demo
