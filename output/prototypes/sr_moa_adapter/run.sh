#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
python demo.py
