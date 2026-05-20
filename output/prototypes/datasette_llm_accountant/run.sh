#!/usr/bin/env bash
# datasette-llm demo — shows llm_prompt_context() hook and the v0.1a8 fix.
# No API keys or Datasette installation needed.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== datasette-llm: llm_prompt_context() Hook Demo ==="
echo ""
python3 demo_plugin.py
