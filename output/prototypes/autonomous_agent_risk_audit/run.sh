#!/usr/bin/env bash
# Autonomous Agent Risk Audit — end-to-end demo
# Runs two scenarios: a dangerous AI cafe agent vs. a well-guarded one
set -e
cd "$(dirname "$0")"
python3 audit_agent.py
