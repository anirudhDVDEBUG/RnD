#!/usr/bin/env bash
# Run the Ansys AEDT MCP simulation demo (no Ansys installation required)
set -euo pipefail
cd "$(dirname "$0")"
python3 demo_workflow.py
