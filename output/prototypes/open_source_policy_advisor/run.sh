#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Open Source Policy Advisor — running all 3 scenarios"
echo ""
python3 advisor.py
echo ""
echo ">>> JSON output for scenario 2 (HMRC — actively exploited vuln):"
echo ""
python3 advisor.py 2 --json
