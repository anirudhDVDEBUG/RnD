#!/usr/bin/env bash
# Hermes Notion GBrain Task Manager — Demo
# Runs the full pipeline with mock data (no API keys needed)
set -e

cd "$(dirname "$0")"

echo "Checking Python..."
python3 --version

echo "Running Hermes Notion GBrain demo..."
echo ""
python3 demo.py
