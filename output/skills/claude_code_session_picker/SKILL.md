---
name: claude_code_session_picker
description: |
  Pick and resume any past Claude Code session via fzf interactive fuzzy finder, automatically restoring the correct working directory.
  Triggers: session picker, resume session, switch session, list sessions, fzf session
---

# Claude Code Session Picker

Interactively browse, search, and resume past Claude Code sessions using fzf. Each session is resumed from its original working directory.

## When to use

- "How do I pick a past Claude Code session to resume?"
- "I want to switch to a previous Claude Code session"
- "List my recent Claude Code sessions and let me choose one"
- "Resume a Claude Code session from the right directory"
- "Use fzf to find and resume a Claude Code session"

## How to use

### Prerequisites

1. **Go** (1.21+) must be installed
2. **fzf** must be installed (`brew install fzf` on macOS, `apt install fzf` on Debian/Ubuntu)
3. **Claude Code CLI** (`claude`) must be available on your PATH

### Installation

```bash
go install github.com/sorafujitani/ccsession@latest
```

Or build from source:

```bash
git clone https://github.com/sorafujitani/ccsession.git
cd ccsession
go build -o ccsession .
```

### Usage

Run the session picker:

```bash
ccsession
```

This will:

1. Scan your Claude Code session history
2. Present an interactive fzf list of past sessions
3. Let you fuzzy-search and select a session
4. Resume the selected session from its original working directory (`cwd`)

### Tips

- Use fzf search to quickly filter sessions by project name, directory, or conversation topic
- The tool automatically detects and restores the correct working directory for each session
- Sessions are listed with metadata to help you identify the right one

## References

- **Source**: [sorafujitani/ccsession](https://github.com/sorafujitani/ccsession)
- **Language**: Go
- **License**: See repository for license details
