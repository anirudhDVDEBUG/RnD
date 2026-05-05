# Technical Details — gigaxity-deep-research

## What it does

gigaxity-deep-research is an MCP (Model Context Protocol) server that exposes a
`deep_research` tool. When called, it:

1. Takes a natural-language query and a depth setting (quick / standard / deep).
2. Searches the web for relevant sources (the upstream repo uses a web-search
   integration, likely Tavily or SearXNG).
3. Sends the gathered context to **Tongyi Qwen-2.5 30B** via **OpenRouter**,
   instructing it to synthesise a cited markdown report.
4. Returns the report with inline citations and a source table.

The server speaks MCP over stdio (JSON-RPC), making it compatible with any MCP
client: Claude Code, Cursor, Hermes, or custom integrations.

## Architecture

```
┌──────────────┐     stdio/JSON-RPC     ┌──────────────────────┐
│  MCP Client  │ ◄────────────────────► │  server.py           │
│  (Claude Code│                        │  - tools/list        │
│   / Cursor)  │                        │  - tools/call        │
└──────────────┘                        │    └─ deep_research  │
                                        └──────────┬───────────┘
                                                   │
                                    ┌──────────────┴──────────────┐
                                    │                             │
                              ┌─────▼─────┐              ┌───────▼───────┐
                              │ Web Search │              │  OpenRouter   │
                              │ (Tavily /  │              │  Qwen-2.5    │
                              │  SearXNG)  │              │  30B/72B     │
                              └────────────┘              └───────────────┘
```

### Key files

| File | Purpose |
|------|---------|
| `server.py` | MCP server — handles JSON-RPC, routes tool calls, calls OpenRouter |
| `demo.py` | Standalone demo that exercises the tool in mock mode |
| `run.sh` | One-command demo runner |
| `requirements.txt` | Python dependencies (httpx, mcp) |

### Data flow

1. Client sends `tools/call` with `name: "deep_research"` and `arguments: {query, depth}`.
2. Server checks for `OPENROUTER_API_KEY`; if missing or `MOCK=1`, returns canned output.
3. In live mode: sends a chat completion request to OpenRouter's `qwen/qwen-2.5-72b-instruct` endpoint with a system prompt instructing cited synthesis.
4. Returns the model's response wrapped in MCP `content` format.

### Dependencies

- **Python 3.10+**
- **httpx** — HTTP client for OpenRouter API calls
- **OpenRouter account** — for live mode (free tier available)
- No database, no Docker, no build step

### Model choice

The upstream project uses **Tongyi Qwen-2.5 30B** via OpenRouter. This model is:
- Significantly cheaper than GPT-4 or Claude for research synthesis ($0.15/M input tokens)
- Strong at following structured output instructions
- Available with high rate limits on OpenRouter

Our prototype also supports the 72B variant (`qwen/qwen-2.5-72b-instruct`) for higher quality.

## Limitations

- **No persistent memory** — each call is stateless; no conversation threading.
- **Web search quality** depends on the upstream search provider configuration.
- **No source verification** — citations come from the model's synthesis; URLs may be hallucinated in mock mode (and potentially in live mode too).
- **Single model** — locked to Qwen via OpenRouter; no model selection at runtime.
- **No streaming** — returns the full report at once; long queries may take 10-30s.
- **Rate limits** — subject to OpenRouter's rate limits for your API key tier.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Lead generation** | Research prospects, industries, or market segments on demand |
| **Marketing / content** | Generate cited research sections for blog posts or reports |
| **Ad creatives** | Research competitor positioning before generating ad copy |
| **Agent factories** | Plug deep-research as a tool in multi-agent workflows |
| **Voice AI** | Back a voice agent with real-time research capability |

The key value: it turns Claude Code into a research assistant with web access
and cited synthesis — without needing Perplexity or a custom RAG pipeline.
The MCP interface means zero code changes in the client; just add the server
config and the tool appears.
