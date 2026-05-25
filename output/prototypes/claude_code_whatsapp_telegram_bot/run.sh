#!/usr/bin/env bash
set -e

echo "Claude Code WhatsApp & Telegram Bot - Demo Runner"
echo ""

# Check Node.js
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is required but not found. Install Node.js 18+."
  exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
echo "Node.js version: $(node -v)"

# Run the mock demo (no API keys or npm install needed - zero external deps)
echo "Running mock demo (no API keys required)..."
echo ""

node src/mock-bot.js
