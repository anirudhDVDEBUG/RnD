#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo ">>> Cleaning up previous demo artifacts..."
rm -f demo_journal.sqlite

echo ">>> Running demo workflow (fake adapter — no API keys needed)..."
echo
python3 demo_workflow.py
echo
echo ">>> Verifying SQLite journal exists..."
if [ -f demo_journal.sqlite ]; then
    echo "    demo_journal.sqlite created ($(wc -c < demo_journal.sqlite) bytes)"
else
    echo "    ERROR: journal not created"
    exit 1
fi
echo
echo ">>> Demo complete."
