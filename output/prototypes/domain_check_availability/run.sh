#!/usr/bin/env bash
set -euo pipefail

echo "=== Domain Availability Checker Demo ==="
echo ""

# No external dependencies needed — stdlib only
cd "$(dirname "$0")"

echo "--- Example 1: Check 'launchpad' across default TLDs ---"
python3 domain_check.py launchpad
echo ""

echo "--- Example 2: Check 'cloudforge' across specific TLDs ---"
python3 domain_check.py cloudforge com,io,dev,ai,xyz
echo ""

echo "--- Example 3: Check full domain input (strips TLD, checks all) ---"
python3 domain_check.py myapp.com com,net,io,dev
echo ""

echo "=== Demo complete ==="
