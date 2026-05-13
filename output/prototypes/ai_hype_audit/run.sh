#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "======================================"
echo " AI Hype Audit — Demo Run"
echo "======================================"
echo ""
echo "Auditing two sample proposals:"
echo "  1) A hype-heavy AI transformation memo"
echo "  2) A well-grounded pilot proposal"
echo ""

# Install deps (none beyond stdlib, but be explicit)
if [ -f requirements.txt ]; then
    pip install -r requirements.txt -q 2>/dev/null || true
fi

echo "--------------------------------------"
echo " SAMPLE 1: Hype-Heavy Proposal"
echo "--------------------------------------"
python3 -c "
from sample_proposals import HYPE_PROPOSAL
from audit import audit, format_report
result = audit(HYPE_PROPOSAL)
print(format_report(result))
"

echo ""
echo ""
echo "--------------------------------------"
echo " SAMPLE 2: Grounded Pilot Proposal"
echo "--------------------------------------"
python3 -c "
from sample_proposals import GROUNDED_PROPOSAL
from audit import audit, format_report
result = audit(GROUNDED_PROPOSAL)
print(format_report(result))
"

echo ""
echo "======================================"
echo " Done. Try: echo 'your text' | python3 audit.py"
echo "======================================"
