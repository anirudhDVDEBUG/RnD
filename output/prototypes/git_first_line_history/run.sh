#!/bin/bash
# Demo: creates a temporary git repo with simulated project renames,
# then runs first_line_history.sh to show the rename timeline.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR=$(mktemp -d)
trap "rm -rf $DEMO_DIR" EXIT

echo "=== Git First Line History Demo ==="
echo ""
echo "Creating a sample repo with project rename history..."
echo ""

cd "$DEMO_DIR"
git init -q
git config user.email "demo@example.com"
git config user.name "Demo User"

# Simulate a project that gets renamed multiple times
echo "# Warelay — WhatsApp Relay CLI (Twilio)" > README.md
echo "" >> README.md
echo "A CLI tool for WhatsApp messaging." >> README.md
git add README.md
GIT_AUTHOR_DATE="2025-11-24T11:23:15+01:00" GIT_COMMITTER_DATE="2025-11-24T11:23:15+01:00" \
  git commit -q -m "Initial commit"

echo "# warelay — Send, receive, and auto-reply on WhatsApp" > README.md
echo "" >> README.md
echo "Full-featured WhatsApp automation." >> README.md
git add README.md
GIT_AUTHOR_DATE="2025-11-25T13:51:13+01:00" GIT_COMMITTER_DATE="2025-11-25T13:51:13+01:00" \
  git commit -q -m "Rebrand: lowercase + new tagline"

# A commit that doesn't change line 1 (should be filtered out)
echo "# warelay — Send, receive, and auto-reply on WhatsApp" > README.md
echo "" >> README.md
echo "Full-featured WhatsApp automation platform." >> README.md
git add README.md
GIT_AUTHOR_DATE="2025-11-28T10:00:00+01:00" GIT_COMMITTER_DATE="2025-11-28T10:00:00+01:00" \
  git commit -q -m "Update body text only"

echo "# CLAWDIS" > README.md
echo "" >> README.md
echo "Messaging platform, renamed." >> README.md
git add README.md
GIT_AUTHOR_DATE="2025-12-01T09:15:00+01:00" GIT_COMMITTER_DATE="2025-12-01T09:15:00+01:00" \
  git commit -q -m "Major rename to CLAWDIS"

echo "# OpenClaw" > README.md
echo "" >> README.md
echo "Open-source claw messaging platform." >> README.md
git add README.md
GIT_AUTHOR_DATE="2025-12-15T14:30:00+01:00" GIT_COMMITTER_DATE="2025-12-15T14:30:00+01:00" \
  git commit -q -m "Final rename: OpenClaw"

echo "--- Running first_line_history.sh on demo repo ---"
echo ""

# Run the tool (handle systems without tac by falling back to tail -r)
if command -v tac >/dev/null 2>&1; then
  bash "$SCRIPT_DIR/first_line_history.sh" README.md
else
  # macOS fallback: replace tac with tail -r
  FILE="README.md"
  prev=""
  git log --follow --diff-filter=AM --format='%H %aI' -- "$FILE" | while read hash date; do
    line=$(git show "$hash:$FILE" 2>/dev/null | head -n 1)
    if [ -n "$line" ] && [ "$line" != "$prev" ]; then
      short=$(echo "$hash" | cut -c1-7)
      echo "$date $short $line"
      prev="$line"
    fi
  done | tail -r
fi

echo ""
echo "--- Done ---"
echo ""
echo "The project was renamed $(bash "$SCRIPT_DIR/first_line_history.sh" README.md 2>/dev/null | wc -l | tr -d ' ') times total."
echo "Source: https://simonwillison.net/2026/May/16/openclaw-names/#atom-everything"
