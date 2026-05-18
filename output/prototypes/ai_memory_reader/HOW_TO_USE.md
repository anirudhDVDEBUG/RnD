# How to Use — AI Memory Reader

## Installation

### This Python CLI prototype (runs anywhere)

```bash
git clone <this-repo> && cd ai_memory_reader
pip install -r requirements.txt
python3 ai_memory_reader.py
```

### Original native macOS/iOS app

```bash
git clone https://github.com/nvwalj/ai-memory-reader.git
cd ai-memory-reader
# Open in Xcode, build for macOS or iOS
# Or download pre-built .app from GitHub Releases
```

## First 60 Seconds

```bash
# 1. Run the demo (uses mock data, no API keys needed)
bash run.sh

# 2. Scan your real agent memory directories
python3 ai_memory_reader.py

# 3. Show file content previews
python3 ai_memory_reader.py --content

# 4. Filter to a specific agent
python3 ai_memory_reader.py --agent "Claude"
```

**Input:** Your filesystem (reads from `~/.claude/`, `~/.codex/`, `~/.cursor/`, `~/.gemini/`, `~/.openclaw/`)

**Output:** A table showing all discovered memory files, organized by agent, with optional Markdown content previews rendered in the terminal.

## CLI Options

| Flag | Description |
|------|-------------|
| `--mock` | Generate and include mock data for demo |
| `--content` | Show first 200 chars of each file |
| `--agent NAME` | Filter results to one agent |
| `--mock-dir PATH` | Custom directory for mock files |

## Integration as a Claude Skill

This isn't a skill itself — it's a **diagnostic tool** for inspecting what skills and memory your agents have stored. Use it to:

1. Audit what Claude Code remembers about your projects (`~/.claude/projects/`)
2. Compare memory across agents working on the same codebase
3. Verify that CLAUDE.md preferences are propagating correctly

## What It Reads

| Agent | Directories Scanned |
|-------|-------------------|
| Claude Code | `~/.claude/`, `~/.claude/projects/` |
| Codex | `~/.codex/`, `~/.codex/memory/` |
| Cursor | `~/.cursor/`, `~/.cursor/rules/` |
| Gemini | `~/.gemini/`, `~/.gemini/memory/` |
| OpenClaw | `~/.openclaw/`, `~/.openclaw/memory/` |

All reads are **read-only** — no files are modified, created, or deleted in agent directories.
