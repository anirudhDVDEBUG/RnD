#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo ""
echo "Running Ta-Persona Digital Twin Distillation (demo mode)..."
echo ""

python3 persona_distiller.py
