#!/usr/bin/env bash
# run.sh — Demo the Claude Code Session Picker
# No API keys or external services required.
set -euo pipefail
cd "$(dirname "$0")"

echo "=============================================="
echo "  Claude Code Session Picker — Demo"
echo "=============================================="
echo ""

# ── 1. Show all mock sessions as a table ──
echo ">>> Listing mock sessions (--demo --list):"
echo ""
python3 ccsession.py --demo --list

# ── 2. Pick session #3 and show resume info (dry-run) ──
echo ">>> Auto-picking session #3 (--demo --pick 3 --dry-run):"
python3 ccsession.py --demo --pick 3 --dry-run
echo ""

# ── 3. JSON output for piping / scripting ──
echo ">>> JSON output of first 3 sessions (--demo --json | head):"
echo ""
python3 ccsession.py --demo --json | python3 -c "
import json, sys
data = json.load(sys.stdin)[:3]
for s in data:
    print(f'  {s[\"id\"][:12]}…  {s[\"project\"]:35}  {s[\"summary\"][:45]}')
"
echo ""

# ── 4. Scan real sessions if they exist ──
CLAUDE_DIR="$HOME/.claude/projects"
if [ -d "$CLAUDE_DIR" ]; then
    REAL_COUNT=$(find "$CLAUDE_DIR" -name '*.jsonl' 2>/dev/null | wc -l)
    echo ">>> Found $REAL_COUNT real session file(s) in $CLAUDE_DIR"
    if [ "$REAL_COUNT" -gt 0 ]; then
        echo ""
        echo ">>> Your real sessions (--list):"
        python3 ccsession.py --list
    fi
else
    echo ">>> No real sessions found (${CLAUDE_DIR} does not exist)."
    echo "   Install Claude Code and run a few sessions to populate it."
fi

echo ""
echo "=============================================="
echo "  Done. See HOW_TO_USE.md for full usage."
echo "=============================================="
