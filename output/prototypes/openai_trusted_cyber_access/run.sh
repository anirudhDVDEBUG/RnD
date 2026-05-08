#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[*] Installing dependencies ..."
pip install -q -r requirements.txt 2>/dev/null || pip install -q openai 2>/dev/null || true

echo "[*] Running GPT-5.5-Cyber vulnerability analysis demo ..."
echo
python cyber_analyzer.py
