# How to Use: TrustGraph Resource Rater

## What This Is

A Claude Code **skill** (PostToolUse hook) that silently rates every external resource fetched during a session and logs scores to a local JSONL ledger.

## Install Steps

### 1. Clone and place the skill

```bash
# Clone the source repo
git clone https://github.com/GusEllerm/trustgraph-skill.git /tmp/trustgraph-skill

# Copy into Claude Code skills directory
mkdir -p ~/.claude/skills/trustgraph_resource_rater
cp /tmp/trustgraph-skill/rate.sh ~/.claude/skills/trustgraph_resource_rater/
cp /tmp/trustgraph-skill/SKILL.md ~/.claude/skills/trustgraph_resource_rater/
chmod +x ~/.claude/skills/trustgraph_resource_rater/rate.sh
```

Or manually create `~/.claude/skills/trustgraph_resource_rater/` and copy `rate.sh` from this repo.

### 2. Choose a rater backend

**Option A — Anthropic API key (recommended):**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```
Uses `claude-haiku-4-5-20251001` for fast, cheap scoring (~0.001 cents per rating).

**Option B — Claude CLI subscription (no extra cost):**
No setup needed — the script falls back to `claude -p` if no API key is set. Requires the `claude` CLI to be installed and authenticated.

### 3. Configure PostToolUse hooks

Add this to your Claude Code settings file. Choose one:

- **Project-level:** `.claude/settings.json` in your repo
- **User-level:** `~/.claude/settings.json`

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

The `matcher` regex fires on:
- `WebFetch` — any URL fetched
- `WebSearch` — search engine results
- `Bash` — catches `curl`/`wget` commands
- `mcp` — any MCP server tool call

### 4. Trigger phrases

Once installed, these phrases activate the skill in Claude Code:
- "Set up automatic trust scoring for external resources"
- "Rate the reliability of web sources"
- "Enable trustgraph scoring for all external tool calls"
- "Track which MCP servers and URLs are trustworthy"

## First 60 Seconds

**Input:** Just use Claude Code normally. Fetch a webpage:

```
> Fetch the docs at https://docs.python.org/3/library/json.html and summarize them
```

**What happens invisibly:** After `WebFetch` completes, the hook fires `rate.sh`, which:
1. Extracts the domain `docs.python.org` from the tool output
2. Sends a rating prompt to Haiku (or `claude -p`)
3. Appends a scored record to `~/.claude/trustgraph_ledger.jsonl`

**Output in the ledger** (`~/.claude/trustgraph_ledger.jsonl`):
```json
{"ts":"2026-05-22T08:15:30Z","tool":"WebFetch","domain":"docs.python.org","rating":{"domain":"docs.python.org","score":9,"reason":"Official Python documentation, highly authoritative and well-maintained"}}
```

**Query accumulated scores:**
```bash
python3 query_ledger.py
# or specify a custom ledger path:
python3 query_ledger.py ~/.claude/trustgraph_ledger.jsonl
```

Output:
```
Loaded 12 records from /home/user/.claude/trustgraph_ledger.jsonl

Domain                              Avg   Min  Max   #  Tools
--------------------------------------------------------------------------------
sketchy-blog.xyz                     2.0    1    3   2  WebSearch
stackoverflow.com                    7.3    5    9   4  WebFetch, WebSearch
docs.python.org                      9.2    8   10   6  WebFetch, WebSearch
```

## Demo (no API key needed)

```bash
bash run.sh
```

This generates 50 mock ledger entries and prints the full trust report so you can see the output format without configuring anything.

## Ledger Location

Default: `~/.claude/trustgraph_ledger.jsonl`

Override with: `export TRUSTGRAPH_LEDGER=/path/to/custom_ledger.jsonl`

## Uninstall

```bash
rm -rf ~/.claude/skills/trustgraph_resource_rater
# Remove the PostToolUse hook from your settings.json
# Optionally delete the ledger:
rm ~/.claude/trustgraph_ledger.jsonl
```
