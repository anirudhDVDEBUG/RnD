#!/usr/bin/env bash
# Agents Best Practices — Demo Runner
# Runs the workflow pattern simulator (no API keys needed)

set -e

cd "$(dirname "$0")"

echo "Agents Best Practices — Workflow Pattern Simulator"
echo "Source: github.com/DenisSergeevitch/agents-best-practices"
echo ""

python3 agents_demo.py
