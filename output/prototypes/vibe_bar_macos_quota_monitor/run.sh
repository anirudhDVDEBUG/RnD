#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo ">>> Vibe Bar — Quota Monitor (Terminal Demo)"
echo ">>> No API keys needed — uses mock billing data."
echo ""

# No external deps required — stdlib only
python3 quota_monitor.py

echo ""
echo ">>> JSON output mode:"
echo ""
python3 quota_monitor.py --json
