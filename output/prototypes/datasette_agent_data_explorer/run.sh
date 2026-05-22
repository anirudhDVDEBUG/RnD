#!/usr/bin/env bash
# Datasette Agent Data Explorer — Mock Demo
# Runs end-to-end without any API keys using a sample SQLite database.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Step 1: Creating sample power plants database..."
python3 demo_data.py

echo "Step 2: Running mock Datasette Agent conversation..."
echo
python3 mock_agent.py
