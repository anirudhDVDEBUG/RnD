#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "=================================================="
echo "  llm-echo Mock Model Testing — run.sh"
echo "=================================================="
echo

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/3] Virtual environment exists."
fi

# Activate and install
source "$VENV_DIR/bin/activate"

echo "[2/3] Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r "$SCRIPT_DIR/requirements.txt"

echo "[3/3] Running demo test suite..."
echo
python3 "$SCRIPT_DIR/demo_echo.py"
