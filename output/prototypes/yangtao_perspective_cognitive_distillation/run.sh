#!/usr/bin/env bash
# Yang Tao Perspective — Cognitive Distillation Demo
# Runs 3 sample business scenarios through the framework engine
# No API keys or external dependencies required

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Yang Tao Perspective — Cognitive Distillation Engine    ║"
echo "║  杨涛视角 · 认知操作系统蒸馏                              ║"
echo "║                                                          ║"
echo "║  Running 3 sample business scenarios...                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

python3 yangtao_engine.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Demo complete. To analyze your own scenario:"
echo "  python3 yangtao_engine.py \"your business idea here\""
echo ""
echo "  To install as a Claude Code skill:"
echo "  mkdir -p ~/.claude/skills/yangtao-perspective"
echo "  cp SKILL.md ~/.claude/skills/yangtao-perspective/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
