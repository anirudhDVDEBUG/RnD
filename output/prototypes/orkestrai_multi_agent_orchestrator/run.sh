#!/usr/bin/env bash
# Orkestrai Multi-Agent Orchestrator — end-to-end demo
# Runs in mock mode (no API keys required)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q fastapi uvicorn httpx pydantic python-dotenv 2>/dev/null

echo ""
python3 demo.py
