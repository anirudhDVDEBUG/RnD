#!/bin/bash
# Amazon Seller Daily Digest — Demo run (no API keys required)
set -e

cd "$(dirname "$0")"

echo "[setup] Installing dependencies..."
npm install --silent 2>/dev/null || true

echo "[run] Generating Amazon Seller Daily Digest (demo mode)..."
echo ""

node index.js
