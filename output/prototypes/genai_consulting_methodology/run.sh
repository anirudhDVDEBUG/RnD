#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  GenAI Consulting Methodology Toolkit — Demo Run                   ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Running L1-L5 maturity assessment on mock company: Acme Manufacturing Co."
echo ""

python3 assess.py mock_company.json

echo ""
echo "── Done. See assessment_output.json for machine-readable summary. ──"
