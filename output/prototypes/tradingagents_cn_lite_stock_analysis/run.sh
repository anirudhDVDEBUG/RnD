#!/usr/bin/env bash
# TradingAgents CN Lite — end-to-end demo (mock data, no API keys needed)
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Installing dependencies (stdlib only — nothing to install)..."
echo ""

echo ">>> Running multi-agent stock analysis on all 6 demo tickers..."
echo "    (A-Share: 600519, 000001 | HK: 00700, 09988 | US: AAPL, TSLA)"
echo ""

python3 trading_agents.py

echo ""
echo ">>> Demo complete. See README.md / HOW_TO_USE.md for real-framework setup."
