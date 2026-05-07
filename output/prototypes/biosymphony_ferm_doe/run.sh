#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
echo "──────────────────────────────────────────────────"
echo " BioSymphony Fermentation DoE — Prototype Demo"
echo "──────────────────────────────────────────────────"
echo ""

# No external deps needed — pure Python stdlib
python3 "$DIR/doe_engine.py"
