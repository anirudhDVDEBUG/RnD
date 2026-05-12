#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Enterprise AI Scaling Playbook — Demo"
echo ""

python3 assess.py --demo --json report.json

echo ""
echo "==> Done. JSON report also saved to report.json"
