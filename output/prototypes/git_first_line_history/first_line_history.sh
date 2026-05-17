#!/bin/sh
# Usage: ./first_line_history.sh [filepath]
# Shows how the first line of a file changed across git history.
# Only prints when the first line actually changed (deduplicates consecutive identical lines).

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
