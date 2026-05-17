#!/usr/bin/env bash
# Multi-Agent Orchestration Engine Demo
# Runs all three orchestration patterns (sequential, parallel, hierarchical)
# No API keys required - uses simulated agent handlers.

set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || true

echo "Running Multi-Agent Orchestration Demo..."
echo ""
python orchestrator.py
