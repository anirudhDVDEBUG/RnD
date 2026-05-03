# How to Use

## Install

No packages to install. Clone and run:

```bash
git clone https://github.com/readysolutionsai/opus-compatibility-scanner.git
cd opus-compatibility-scanner
python3 scanner.py /path/to/your/project
```

Requires Python 3.8+. No pip dependencies.

## As a Claude Skill

Drop the skill file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/opus_compatibility_scanner
cp SKILL.md ~/.claude/skills/opus_compatibility_scanner/SKILL.md
```

Then trigger it with natural language in Claude Code:

- "Scan my project for Opus 4.7 compatibility issues"
- "Check if my CLAUDE.md is compatible with the new Opus"
- "Run a migration check on my Claude Code configuration"
- "What do I need to change before upgrading to Opus 4.7?"

Claude will read the skill and execute the scanner logic against your project files.

## First 60 Seconds

```bash
# 1. Run the demo against the included mock project
bash run.sh

# 2. See the report — it finds ~40 issues across severity levels:
#    CRITICAL: deprecated model IDs, removed API methods
#    WARNING:  renamed settings keys, changed hook signatures
#    INFO:     new defaults, recommended updates

# 3. Scan your own project
python3 scanner.py ~/my-claude-project

# 4. Pipe to a file for review
python3 scanner.py ~/my-claude-project > migration-report.txt
```

### Example output (abbreviated)

```
========================================================================
  OPUS COMPATIBILITY SCANNER — 4.6 → 4.7 Migration Report
========================================================================
  Files scanned:    6
  Patterns checked: 70
  Issues found:     38

  Summary:  11 CRITICAL  |  18 WARNING  |  9 INFO
========================================================================

  [!!!] CRITICAL (11 issues)
  --------------------------------------------------------------------
  [MODEL-002] CLAUDE.md:4
    Deprecated model ID: claude-opus-4-6
    -> Replace with claude-opus-4-7

  [API-004] app.py:12
    Legacy .completion() method removed in 4.7 SDK
    -> Use .messages.create() instead

  [API-005] app.py:14
    HUMAN_PROMPT constant removed in 4.7 SDK
    -> Use messages API format with role-based messages

  [HOOK-003] dot_claude/settings.json:20
    PreCommit hook removed in 4.7
    -> Use PreToolUse with tool='git_commit' filter instead

  [MCP-002] dot_claude/settings.json:33
    MCP protocol v1 deprecated in 4.7
    -> Upgrade to mcp-v2 protocol
  ...
```

## Scan Your Own Project

The scanner walks the project directory and checks all `.py`, `.ts`, `.js`, `.json`, `.md`, `.yaml`, and `.yml` files. It skips `.git`, `node_modules`, `__pycache__`, and virtual environments automatically.

```bash
# Scan current directory
python3 scanner.py .

# Scan a specific project
python3 scanner.py /home/user/my-agent-project

# Only care about critical issues? Filter with grep
python3 scanner.py . | grep -A2 "CRITICAL"
```
