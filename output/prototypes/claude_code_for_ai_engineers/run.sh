#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo ""
echo "========================================================================"
echo "  AI Engineering Skill Pack — Demo Runner"
echo "  Source: github.com/surpradhan/claude-code-for-ai-engineers"
echo "========================================================================"
echo ""

# --- 1. RAG Evaluation ---
echo ">>> Running RAG Pipeline Evaluation..."
echo ""
python3 demo_rag_eval.py
echo ""

# --- 2. Agent Debugging ---
echo ">>> Running Agent Debugging Trace..."
echo ""
python3 demo_agent_debug.py
echo ""

# --- 3. Benchmark Reporting ---
echo ">>> Running Benchmark Report..."
echo ""
python3 demo_benchmark.py
echo ""

echo "========================================================================"
echo "  All 3 demos complete. Output files:"
echo "    - rag_eval_report.json"
echo "    - agent_debug_report.json"
echo "    - benchmark_report.json"
echo ""
echo "  To install the skill in Claude Code:"
echo "    cp -r skill/ ~/.claude/skills/ai-engineering-skill-pack/"
echo "  Then say: \"evaluate my RAG pipeline\" or \"debug my agent\""
echo "========================================================================"
