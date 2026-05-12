#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "============================================"
echo "  GCC Market Intelligence — Demo Run"
echo "============================================"
echo ""

# 1. Single-country briefing (Saudi + cybersecurity)
echo ">>> Briefing: Saudi Arabia / Cybersecurity"
echo ""
python3 gcc_intel.py --country saudi --vertical cybersecurity

echo ""
echo ""

# 2. Country comparison (Saudi vs UAE vs Qatar for fintech)
echo ">>> Comparison: Saudi vs UAE vs Qatar (fintech)"
echo ""
python3 gcc_intel.py --compare saudi uae qatar --vertical fintech

echo ""
echo ""

# 3. JSON output for a single country
echo ">>> JSON output: Bahrain / fintech (first 30 lines)"
echo ""
python3 gcc_intel.py --country bahrain --vertical fintech --json | head -30
echo "  ... (truncated)"

echo ""
echo "============================================"
echo "  Demo complete. No API keys required."
echo "============================================"
