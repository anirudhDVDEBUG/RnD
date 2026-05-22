# Technical Details: TrustGraph Resource Rater

## What It Does

TrustGraph hooks into Claude Code's PostToolUse event system to intercept every external resource access — `WebFetch`, `WebSearch`, `Bash` (for curl/wget), and MCP server calls. After each tool completes, a background shell script extracts the domain from the tool's input/output, sends a one-shot rating prompt to a fast LLM (Haiku or `claude -p`), and appends the scored result to a local JSONL ledger.

Over time, the ledger accumulates a per-domain reputation profile: domains that consistently score high (official docs, authoritative APIs) surface as trusted; domains that score low (SEO farms, sketchy downloads) get flagged. The scoring is invisible — it never interrupts the user's workflow.

## Architecture

### Data Flow

```
Claude Code tool call (WebFetch, WebSearch, Bash, MCP)
        |
        v
PostToolUse hook fires
        |
        v
rate.sh receives $TOOL_NAME, $TOOL_INPUT, $TOOL_OUTPUT
        |
        v
Extract domain via regex (grep -oP 'https?://[^/\s"]+')
        |
        v
Send rating prompt to backend:
  - ANTHROPIC_API_KEY set? --> Anthropic Messages API (claude-haiku-4-5-20251001)
  - Otherwise             --> claude -p (CLI subscription)
        |
        v
Append JSON record to ~/.claude/trustgraph_ledger.jsonl
```

### Key Files

| File | Purpose |
|------|---------|
| `rate.sh` | PostToolUse hook script. Extracts domains, calls rater, writes ledger. ~40 lines of bash. |
| `query_ledger.py` | Reads JSONL ledger and prints per-domain aggregate scores (avg/min/max/count). |
| `demo_mock.py` | Generates synthetic ledger data for demos. No API calls. |
| `~/.claude/trustgraph_ledger.jsonl` | Append-only JSONL log. Each line: `{ts, tool, domain, rating: {domain, score, reason}}` |

### Dependencies

- **Runtime:** Bash, Python 3.8+, `curl` (for API backend only)
- **Python packages:** None (stdlib only: `json`, `collections`, `pathlib`)
- **Optional:** `ANTHROPIC_API_KEY` env var, or `claude` CLI installed

### Model Calls

Each PostToolUse event triggers one LLM call:
- **API backend:** `claude-haiku-4-5-20251001`, max 256 tokens. Cost: ~$0.00001 per rating.
- **CLI backend:** `claude -p` pipes a prompt to whatever model your subscription uses.

The rating prompt asks for a 1-10 score with a one-sentence reason. Response is pure JSON.

### Ledger Format

```jsonl
{"ts":"2026-05-22T08:15:30Z","tool":"WebFetch","domain":"docs.python.org","rating":{"domain":"docs.python.org","score":9,"reason":"Official Python documentation"}}
{"ts":"2026-05-22T08:16:02Z","tool":"WebSearch","domain":"medium.com","rating":{"domain":"medium.com","score":5,"reason":"Mixed quality blog platform"}}
```

## Limitations

- **Domain-level only:** Scores entire domains, not individual pages. `github.com/torvalds/linux` and `github.com/abandoned-repo` get the same domain score.
- **LLM knowledge bias:** Ratings reflect the model's training data, not real-time reputation checks. The model knows `docs.python.org` is good but can't detect a newly compromised site.
- **No content analysis:** The rater sees the domain and tool name, not the actual page content. A more sophisticated version could hash or summarize content.
- **Latency on CLI backend:** `claude -p` adds 2-5 seconds per hook call. The API backend is faster (~500ms) but costs tokens.
- **No deduplication:** The same domain gets re-rated on every access. This is by design (scores can change), but means high-traffic domains dominate the ledger.
- **Shell injection surface:** The current `rate.sh` passes tool output through shell variables. In production, sanitize or base64-encode inputs.

## What It Does NOT Do

- Does not block or filter resources — it only scores them.
- Does not share scores across users or machines.
- Does not do real-time threat detection (no WHOIS, DNS, or certificate checks).
- Does not persist scores in a database — it's an append-only flat file.

## Why This Matters

For teams building Claude-driven products:

- **Lead-gen / research agents:** When an agent crawls dozens of sources, TrustGraph lets you post-filter results by source reliability. Low-scored domains get deprioritized in reports.
- **Marketing / content pipelines:** Agents that pull competitor data or industry news can flag when sources are unreliable, reducing hallucination-from-bad-source risk.
- **Agent factories:** If you're orchestrating multiple Claude Code agents, a shared ledger (pointed at a common path) gives you fleet-wide source reputation.
- **Compliance / audit:** The JSONL ledger is an audit trail of every external resource accessed and its assessed trustworthiness. Useful for regulated industries.
- **MCP server vetting:** As MCP ecosystems grow, knowing which third-party servers consistently return trustworthy data is valuable for selecting and ranking MCP providers.
