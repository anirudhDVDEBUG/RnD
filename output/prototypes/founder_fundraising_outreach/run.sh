#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Running Founder Fundraising Outreach demo..."
echo ""

python3 outreach.py
