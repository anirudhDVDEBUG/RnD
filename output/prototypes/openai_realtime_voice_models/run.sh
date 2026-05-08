#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
npm install --no-audit --no-fund 2>&1 | tail -1

echo ""
echo "=== Running OpenAI Realtime Voice API Demo ==="
echo ""
node run_demo.js
