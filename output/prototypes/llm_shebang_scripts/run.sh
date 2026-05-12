#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "============================================================"
echo "  LLM Shebang Scripts — Demo Run"
echo "  Uses mock responses (no API keys or llm CLI needed)"
echo "============================================================"
echo ""

# Make example scripts executable
chmod +x examples/*.sh examples/*.yaml 2>/dev/null || true

# ── 1. Validate all example scripts ──────────────────────────────
echo "┌──────────────────────────────────────────────────────────┐"
echo "│  Step 1: Validate example shebang scripts               │"
echo "└──────────────────────────────────────────────────────────┘"
echo ""
python3 shebang_builder.py validate examples/*
echo ""

# ── 2. Simulate running fragment scripts ─────────────────────────
echo "┌──────────────────────────────────────────────────────────┐"
echo "│  Step 2: Simulate fragment-mode scripts                  │"
echo "└──────────────────────────────────────────────────────────┘"
echo ""

python3 shebang_simulator.py examples/hello_pelican.sh
python3 shebang_simulator.py examples/time_haiku.sh
python3 shebang_simulator.py examples/commit_message.sh
python3 shebang_simulator.py examples/code_review.sh

# ── 3. Simulate running a YAML template script ──────────────────
echo "┌──────────────────────────────────────────────────────────┐"
echo "│  Step 3: Simulate template-mode script (calculator)      │"
echo "└──────────────────────────────────────────────────────────┘"
echo ""

python3 shebang_simulator.py examples/calculator.yaml "what is 2344 * 5252 + 134"

# ── 4. Create a new script with the builder ──────────────────────
echo "┌──────────────────────────────────────────────────────────┐"
echo "│  Step 4: Build a new shebang script via CLI              │"
echo "└──────────────────────────────────────────────────────────┘"
echo ""

python3 shebang_builder.py create /tmp/llm_demo_joke.sh \
    "Tell me a short programming joke" \
    --mode fragment

echo ""
echo "Generated script contents:"
echo "---"
cat /tmp/llm_demo_joke.sh
echo "---"
echo ""

# Validate the generated script
python3 shebang_builder.py validate /tmp/llm_demo_joke.sh

# Simulate running it
python3 shebang_simulator.py /tmp/llm_demo_joke.sh

# Cleanup
rm -f /tmp/llm_demo_joke.sh

echo "============================================================"
echo "  Demo complete!"
echo ""
echo "  With the real llm CLI installed, you can run any of these"
echo "  scripts directly:  ./examples/hello_pelican.sh"
echo "============================================================"
