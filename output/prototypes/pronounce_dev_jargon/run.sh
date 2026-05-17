#!/usr/bin/env bash
# Pronounce Dev Jargon — end-to-end demo
# Runs without external API keys or network access.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing dependencies (none required — stdlib only)..."
echo ""

# Run the demo in non-interactive mode (pipe empty input to skip interactive prompt)
echo "" | python3 "$SCRIPT_DIR/pronounce_db.py"
