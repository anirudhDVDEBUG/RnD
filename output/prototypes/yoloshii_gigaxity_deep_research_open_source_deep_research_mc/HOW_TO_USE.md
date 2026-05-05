# How to Use — gigaxity-deep-research MCP

## Option A: Use the upstream repo directly

```bash
git clone https://github.com/yoloshii/gigaxity-deep-research.git
cd gigaxity-deep-research
pip install -r requirements.txt   # or: npm install (if Node version)
```

## Option B: Use this prototype's server.py

```bash
pip install httpx mcp
```

No other dependencies required.

## MCP Configuration for Claude Code

Add this to your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "gigaxity-deep-research": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-YOUR_KEY_HERE"
      }
    }
  }
}
```

Replace `/absolute/path/to/server.py` with the actual path.

### Mock mode (no API key)

To test without an OpenRouter key, add `"MOCK": "1"` to the `env` block:

```json
{
  "mcpServers": {
    "gigaxity-deep-research": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "MOCK": "1"
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | For live mode | Your OpenRouter API key (get one at https://openrouter.ai) |
| `MOCK` | No | Set to `1` to use canned responses (no API calls) |

## First 60 Seconds

1. Add the MCP config above to `~/.claude.json`
2. Restart Claude Code
3. Ask Claude:

```
Use deep_research to find out about open-source alternatives to Perplexity
```

4. Claude calls the `deep_research` tool → you get a cited markdown report:

```markdown
## Deep Research Report
### Query: open-source alternatives to Perplexity

### Executive Summary
This report synthesises findings from multiple web sources...

### Key Findings
1. **Finding 1** — Several projects now offer... [[1]](https://...)
2. **Finding 2** — Performance benchmarks show... [[2]](https://...)

### Sources
| # | Title | URL |
|---|-------|-----|
| 1 | ... | https://... |
```

## Tool Reference

### `deep_research`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The research question or topic |
| `depth` | string | No | `"quick"`, `"standard"` (default), or `"deep"` |

**depth controls output length:** quick ~500 words, standard ~1000 words, deep ~2000 words.
