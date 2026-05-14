#!/usr/bin/env bash
# WhatsApp Agent for Hermes - End-to-end demo
# Runs entirely with mock data; no API keys or WhatsApp session needed.

set -euo pipefail
cd "$(dirname "$0")"

echo ">>> WhatsApp Agent for Hermes - Demo"
echo ">>> Python: $(python3 --version)"
echo ""

python3 demo.py
