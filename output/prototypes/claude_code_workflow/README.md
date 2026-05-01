# Claude Code Workflow — Demo Simulator

Demonstrates Claude Code CLI concepts without requiring an API key or installation. The demo walks through key workflow patterns using mock data and simulated sessions.

## What It Does

1. **CLI Commands** — Shows all core `claude` commands and their purposes
2. **Project Configuration** — Creates a sample `CLAUDE.md` with conventions
3. **Project Structure** — Scaffolds a demo project with src/tests layout
4. **Interactive Session** — Simulates a multi-turn coding session (codebase Q&A, code edit, smart commit)
5. **Permission Modes** — Explains default, auto-accept, and full-auto modes with settings.json allowlists
6. **Piping & Chaining** — Examples of combining Claude Code with Unix tools
7. **Best Practices** — Summary of effective workflow patterns

## Install

```bash
# Python 3.8+ required (no external packages needed)
pip install -r requirements.txt
```

## Run

```bash
bash run.sh
```

## Expected Output

A colorized terminal walkthrough covering 8 sections. The demo creates temporary files under `/tmp/claude-code-demo-project/` to illustrate project structure and CLAUDE.md configuration. No network calls or API keys are used.
