---
name: trustgraph_resource_rater
description: |
  Invisibly rates every external resource (WebFetch, WebSearch, MCP, curl) via PostToolUse hooks and maintains a local trust-score reputation ledger.
  Triggers: "rate external resources", "trust scoring", "resource reputation", "trustgraph", "rate web sources"
---

# TrustGraph Resource Rater

Claude Code skill that invisibly rates every external resource (WebFetch / WebSearch / MCP / curl) via PostToolUse hooks. Maintains a local trust-score reputation ledger so you can identify reliable vs. suspect sources over time.

## When to use

- "Set up automatic trust scoring for external resources"
- "Rate the reliability of web sources I fetch during research"
- "Add reputation tracking to WebFetch and WebSearch results"
- "Enable trustgraph scoring for all external tool calls"
- "Track which MCP servers and URLs are trustworthy"

## How to use

### 1. Choose a rater backend

This skill supports two backends for scoring resources:

**Option A — Anthropic API key (recommended for automation):**
- Set `ANTHROPIC_API_KEY` in your environment.
- The hook script calls the Anthropic API directly to rate each resource.

**Option B — Claude CLI subscription (`claude -p`):**
- No API key needed; uses your existing claude.ai subscription.
- The hook invokes `claude -p` with a rating prompt for each resource.

### 2. Configure PostToolUse hooks

Add PostToolUse hooks to your Claude Code settings (`.claude/settings.json` or project-level) that fire after `WebFetch`, `WebSearch`, `Bash` (for curl), and any MCP tool calls.

Example hook configuration in `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "WebFetch|WebSearch|Bash|mcp",
        "command": "$HOME/.claude/skills/trustgraph_resource_rater/rate.sh \"$TOOL_NAME\" \"$TOOL_INPUT\" \"$TOOL_OUTPUT\""
      }
    ]
  }
}
```

### 3. Rating script (`rate.sh`)

Create the rater script that extracts URLs/domains from tool output and scores them:

```bash
#!/usr/bin/env bash
set -euo pipefail

TOOL_NAME="$1"
TOOL_INPUT="$2"
TOOL_OUTPUT="$3"
LEDGER="$HOME/.claude/trustgraph_ledger.jsonl"

# Extract domain from input/output
DOMAIN=$(echo "$TOOL_INPUT $TOOL_OUTPUT" | grep -oP 'https?://[^/\s"]+' | head -1 | sed 's|https\?://||' | cut -d/ -f1)
[ -z "$DOMAIN" ] && exit 0

# Build rating prompt
PROMPT="Rate the trustworthiness of this resource on a scale of 1-10. Domain: $DOMAIN. Tool: $TOOL_NAME. Respond with ONLY a JSON object: {\"domain\": \"...\", \"score\": N, \"reason\": \"...\"}."

# Use API key backend or claude -p fallback
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  RESULT=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{\"model\":\"claude-haiku-4-5-20251001\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}" \
    | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['content'][0]['text'])" 2>/dev/null)
else
  RESULT=$(echo "$PROMPT" | claude -p 2>/dev/null)
fi

# Append to ledger
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$TIMESTAMP\",\"tool\":\"$TOOL_NAME\",\"domain\":\"$DOMAIN\",\"rating\":$RESULT}" >> "$LEDGER"
```

Make it executable:
```bash
chmod +x ~/.claude/skills/trustgraph_resource_rater/rate.sh
```

### 4. Query the trust ledger

The trust ledger is stored at `~/.claude/trustgraph_ledger.jsonl`. Each line is a JSON record with timestamp, tool name, domain, score, and reason.

To view aggregate scores:
```bash
cat ~/.claude/trustgraph_ledger.jsonl | python3 -c "
import sys, json
from collections import defaultdict
scores = defaultdict(list)
for line in sys.stdin:
    r = json.loads(line)
    s = r.get('rating',{}).get('score')
    if s: scores[r['domain']].append(s)
for d, s in sorted(scores.items(), key=lambda x: sum(x[1])/len(x[1])):
    print(f'{d}: {sum(s)/len(s):.1f} ({len(s)} ratings)')
"
```

### Key concepts

- **Invisible operation**: Hooks run silently after each tool call — no interruption to your workflow.
- **JSONL ledger**: Append-only log at `~/.claude/trustgraph_ledger.jsonl` for easy querying and analysis.
- **Two backends**: Use `ANTHROPIC_API_KEY` for direct API calls (faster, costs tokens) or `claude -p` for subscription-based rating (no extra cost).
- **Cumulative reputation**: Domains accumulate scores over time, building a reputation profile.

## References

- Source: [GusEllerm/trustgraph-skill](https://github.com/GusEllerm/trustgraph-skill)
- Tags: trust-scoring, claude-skill, web-resource-rating, hooks, reputation-system