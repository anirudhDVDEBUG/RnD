# Technical Details — YouTube Research MCP

## What It Does

YouTube Research MCP is a Model Context Protocol server that exposes YouTube data as structured research tools for AI agents. It wraps two data sources — the free `youtube-transcript-api` library (no API key) for transcript extraction, and the YouTube Data API v3 (requires API key) for comments, channel metadata, and search — behind four MCP tools that any MCP-compatible client (Claude Code, Claude Desktop, etc.) can call.

The server communicates via JSON-RPC over stdin/stdout, following the MCP 2024-11-05 protocol spec. When an API key is unavailable, tools gracefully fall back to built-in mock data so the demo and tests still run.

## Architecture

```
Claude / MCP Client
       |
       | stdin/stdout (JSON-RPC)
       v
 ┌─────────────────────────┐
 │  youtube_research_mcp   │
 │  server.py              │
 │                         │
 │  ┌───────────────────┐  │
 │  │ get_transcript    │──┼──> youtube-transcript-api (no key)
 │  │ get_comments      │──┼──> YouTube Data API v3 (key) or mock
 │  │ analyze_channel   │──┼──> YouTube Data API v3 (key) or mock
 │  │ search_videos     │──┼──> YouTube Data API v3 (key) or mock
 │  └───────────────────┘  │
 └─────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `youtube_research_mcp/server.py` | Core logic — tool implementations, mock data, MCP JSON-RPC handler |
| `youtube_research_mcp/__main__.py` | Entry point for `python -m youtube_research_mcp` |
| `demo.py` | Stand-alone script that calls all 4 tools and prints output |
| `run.sh` | One-command demo runner |
| `requirements.txt` | Python dependencies |

### Dependencies

- **youtube-transcript-api** — scrapes YouTube's auto-generated transcript data (no API key needed)
- **google-api-python-client** — official Google API client for comments, channel, and search endpoints (needs `YOUTUBE_API_KEY`)

### Data Flow

1. MCP client sends a `tools/call` JSON-RPC request with tool name and arguments
2. Server extracts the video ID from URL/ID input
3. Tool function calls the appropriate data source (transcript API, YouTube Data API, or mock)
4. Result is returned as structured JSON inside a `tools/call` response
5. Client (Claude) uses the structured data to answer the user's question

## Limitations

- **Transcript extraction** depends on YouTube having captions available. Videos without auto-generated or manual captions will return an error.
- **Comments, search, and channel analysis** require a `YOUTUBE_API_KEY` for live data. Without it, the server returns realistic mock data.
- **Rate limits**: YouTube Data API has a daily quota of 10,000 units. Transcript API has no official rate limit but aggressive scraping may trigger blocks.
- **No video upload/editing** — this is read-only research tooling.
- **No audio/video content analysis** — only text-based data (transcripts, comments, metadata).
- **Channel analysis** currently returns mock data even with an API key (real implementation would need `channels.list` + `search.list` API calls).

## Why This Matters for Claude-Driven Products

**Lead generation & market research**: Analyze competitor YouTube channels to understand what topics resonate, what questions audiences ask in comments, and where content gaps exist. Feed this into lead-gen workflows.

**Marketing & content strategy**: Extract transcripts from top-performing videos in a niche, identify recurring themes, and use Claude to generate content briefs or ad copy that mirrors proven formats.

**Ad creatives**: Pull comment sentiment from product review videos to understand customer language, objections, and enthusiasm — feed directly into ad creative generation.

**Agent factories**: Compose YouTube research tools with other MCP servers (web search, CRM, email) to build autonomous research agents that monitor channels, track competitor content, and surface insights.

**Voice AI**: Extract transcripts from podcast-style YouTube content to build training datasets or knowledge bases for voice AI applications.
