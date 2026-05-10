#!/usr/bin/env bash
# run.sh — End-to-end demo of the DeepSeek Loop Agent (no API key needed)
set -e

cd "$(dirname "$0")"

echo "=============================================="
echo "  DeepSeek Loop Agent — Demo Run"
echo "=============================================="
echo ""

# ---------- Part 1: Agent Loop Demo ----------
echo "--- Part 1: Agent Loop (mock DeepSeek backend) ---"
echo ""
echo "Running agent with prompt: 'Analyze this codebase and summarize its structure.'"
echo ""
python3 cli.py --allow-all "Analyze this codebase and summarize its structure."
echo ""

# ---------- Part 2: Tools Demo ----------
echo "--- Part 2: Built-in Tools (standalone) ---"
echo ""
python3 demo_tools.py
echo ""

# ---------- Part 3: Cron Scheduler Demo ----------
echo "--- Part 3: Cron Scheduler ---"
echo ""
python3 cron_scheduler.py
echo ""

# ---------- Part 4: SdkMessage Event Stream ----------
echo "--- Part 4: SdkMessage Event Stream ---"
echo ""
python3 demo_events.py

echo ""
echo "=============================================="
echo "  Demo complete. All components working."
echo "=============================================="
