#!/usr/bin/env bash
# run.sh -- Execute the web-researcher-mcp mock demo
# No API keys or external services required.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/demo_web_researcher.py"
