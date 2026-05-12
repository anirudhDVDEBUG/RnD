#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "========================================"
echo " Zombie Internet Content Audit - Demo"
echo "========================================"
echo ""
echo "Scanning 3 sample texts for AI slop signals..."
echo ""

python3 audit_content.py samples/ai_slop.txt
python3 audit_content.py samples/human_authentic.txt
python3 audit_content.py samples/zombie_hybrid.txt

echo ""
echo "========================================"
echo " JSON output example (first sample):"
echo "========================================"
echo ""
python3 audit_content.py --format json samples/ai_slop.txt
