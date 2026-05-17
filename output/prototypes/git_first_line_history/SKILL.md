---
name: git_first_line_history
description: |
  Track how the first line of a file has changed across Git history. Useful for tracing project name changes, title evolution, or header mutations over time.
  Triggers: git history of file header, track name changes in repo, first line evolution, readme title history, project rename tracking
---

# Git First Line History

Trace how the first line (or any specific line) of a file has evolved across all Git commits. This is especially useful for tracking project renames, README title changes, or version bumps over time.

## When to use

- "How many times has this project been renamed?"
- "Show me the history of the first line of README.md"
- "Track how the title of this file changed over time in git"
- "What was this repo originally called?"
- "Show the evolution of the project name from git history"

## How to use

1. **Run the following shell script** in the target repository to extract the first line of a file at every commit where it changed:

```bash
#!/bin/sh
# Usage: ./first_line_history.sh <filepath>
# Example: ./first_line_history.sh README.md

FILE="${1:-README.md}"

git log --follow --diff-filter=AM --format='%H %aI' -- "$FILE" | while read hash date; do
  line=$(git show "$hash:$FILE" 2>/dev/null | head -n 1)
  if [ -n "$line" ]; then
    short=$(echo "$hash" | cut -c1-7)
    echo "$date $short $line"
  fi
done | tac
```

2. **Deduplicate consecutive identical lines** to see only actual changes:

```bash
#!/bin/sh
FILE="${1:-README.md}"
prev=""

git log --follow --diff-filter=AM --format='%H %aI' -- "$FILE" | while read hash date; do
  line=$(git show "$hash:$FILE" 2>/dev/null | head -n 1)
  if [ -n "$line" ] && [ "$line" != "$prev" ]; then
    short=$(echo "$hash" | cut -c1-7)
    echo "$date $short $line"
    prev="$line"
  fi
done | tac
```

3. **Interpret the output**: Each line shows the date, short commit hash, and the first line of the file at that point. This reveals the full naming/title history of the project.

## Example output

```
2025-11-24T11:23:15+01:00 16dfc1a # Warelay — WhatsApp Relay CLI (Twilio)
2025-11-25T13:51:13+01:00 4d2a8a8 # warelay — Send, receive, and auto-reply on WhatsApp
2025-12-01T09:15:00+01:00 a3b2c1d # CLAWDIS
2025-12-15T14:30:00+01:00 e4f5a6b # OpenClaw
```

## Tips

- Use `--follow` to track renames of the file itself
- Pipe through `wc -l` to count total name changes
- For tracking a different line number, replace `head -n 1` with `sed -n 'Np'` where N is the line number
- Works with any text file, not just READMEs

## References

- Source: [Simon Willison – Warelay -> OpenClaw](https://simonwillison.net/2026/May/16/openclaw-names/#atom-everything)
- Tool: [first_line_history.py](https://github.com/simonw/tools/blob/main/python/first_line_history.py)
