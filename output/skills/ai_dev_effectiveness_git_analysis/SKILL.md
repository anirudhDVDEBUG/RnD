---
name: ai_dev_effectiveness_git_analysis
description: |
  Measure AI co-programming effectiveness on any git repo. Detects Claude/Copilot/Cursor/Codex commit signatures and calculates productivity multipliers.
  TRIGGER when: user asks to measure AI coding productivity, analyze AI-assisted commits, detect AI co-programming patterns in git history, calculate developer productivity multipliers, or audit how much code was AI-generated.
  DO NOT TRIGGER when: general git log viewing, non-productivity code metrics, or unrelated repository analysis.
---

# AI Dev Effectiveness Analysis

Measure AI co-programming effectiveness on any git repository. Detects Claude/Copilot/Cursor/Codex signatures and triangulates productivity multipliers via top-down roles, bottom-up formula, and optional Claude Code subagent diff reading.

## When to use

- "How much of this repo was written with AI assistance?"
- "Measure AI coding productivity on this project"
- "Detect Claude or Copilot commits in git history"
- "Calculate developer productivity multiplier from AI tools"
- "Audit AI-generated code percentage in this repository"

## How to use

1. **Clone the tool** (if not already available):
   ```bash
   git clone https://github.com/denn-gubsky/ai-dev-effectiveness.git /tmp/ai-dev-effectiveness
   cd /tmp/ai-dev-effectiveness
   pip install -r requirements.txt
   ```

2. **Run analysis on target repo**:
   ```bash
   python analyze.py --repo /path/to/target/repo
   ```

3. **Interpret results**:
   - The tool detects AI signatures in commits (Co-authored-by trailers, tool-specific patterns)
   - It calculates three productivity estimates:
     - **Top-down**: Based on role allocation (% time with AI vs without)
     - **Bottom-up**: Formula-based LOC analysis comparing AI-assisted vs manual commits
     - **Subagent** (optional): Claude Code reads diffs to classify AI involvement
   - Output includes: AI-assisted commit %, LOC breakdown, estimated productivity multiplier

4. **Optional flags**:
   - `--since YYYY-MM-DD` — limit analysis window
   - `--author "name"` — filter to specific developer
   - `--use-subagent` — enable Claude-powered diff classification for higher accuracy
   - `--output json` — machine-readable output

5. **Review the report** for:
   - Which AI tools are being used (Claude, Copilot, Cursor, Codex)
   - Productivity multiplier estimate (typically 1.5x–4x range)
   - Breakdown by author, time period, or file type

## References

- Source: https://github.com/denn-gubsky/ai-dev-effectiveness
- Language: Python / Jupyter Notebook
- Detects: Claude Code, GitHub Copilot, Cursor, OpenAI Codex signatures
