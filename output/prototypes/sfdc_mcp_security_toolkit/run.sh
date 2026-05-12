#!/usr/bin/env bash
# SFDC MCP Security Toolkit — Local Demo
# Runs the adversarial payload scanner with mock Salesforce data.
# No external API keys or Salesforce access required.

set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "SFDC MCP Security Toolkit — Local Demo"
echo "======================================="
echo ""
echo "This demo generates ~70 adversarial Salesforce records across"
echo "14 attack categories and simulates an MCP security scan."
echo ""

python3 scanner.py

echo ""
echo "Done. See report.json for full machine-readable results."
