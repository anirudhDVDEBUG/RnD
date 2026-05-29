#!/usr/bin/env bash
# run.sh — execute the hermes-code-bridge demo end-to-end
# No API keys or external services required.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ">>> Hermes Code Bridge — local orchestration demo"
echo ""

python3 "${SCRIPT_DIR}/hermes_bridge.py"

echo ""
echo ">>> Done. See HOW_TO_USE.md for real-repo setup instructions."
