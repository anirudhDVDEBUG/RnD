# How to Use

## This is a Claude Code Skill

### Installation

1. Create the skill directory:

```bash
mkdir -p ~/.claude/skills/git_first_line_history
```

2. Copy the skill file:

```bash
cp SKILL.md ~/.claude/skills/git_first_line_history/SKILL.md
```

That's it. No pip install, no dependencies beyond `git` and a POSIX shell.

### Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Show me the history of the first line of README.md"
- "How many times has this project been renamed?"
- "Track the title changes in this file over git history"
- "What was this repo originally called?"
- "Show the evolution of the project name from git history"

### What Claude Does

Claude will run a shell one-liner in your repo that extracts the first line of the target file at every commit where it changed, deduplicates consecutive identical values, and displays the timeline.

## First 60 Seconds

1. Open Claude Code in any git repository
2. Say: **"Show me the history of the first line of README.md"**
3. Claude runs the extraction script and returns output like:

```
2024-01-10T09:00:00+00:00 abc1234 # My Cool Project
2024-03-15T14:22:00+00:00 def5678 # My Cool Project v2
2024-06-01T08:00:00+00:00 ghi9012 # Acme SDK
```

4. You instantly see every rename/title change with dates and commit hashes.

## Standalone CLI Usage (no Claude needed)

```bash
# Make the script executable
chmod +x first_line_history.sh

# Run against any file in a git repo
./first_line_history.sh README.md

# Track a different line (e.g., line 3)
# Edit the script: change `head -n 1` to `sed -n '3p'`

# Count total name changes
./first_line_history.sh README.md | wc -l
```

## Requirements

- `git` (any modern version)
- POSIX shell (`sh`, `bash`, `zsh`, `dash` all work)
- A git repository with history
