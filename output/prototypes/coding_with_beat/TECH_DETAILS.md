# Technical Details

## What it does

Coding-with-beat is a Python-based terminal music player (TUI) that integrates with AI coding tools via the Model Context Protocol (MCP). It wraps platform music APIs (Apple Music, QQ Music) and local file playback behind a retro pixel-art interface rendered with Rich/Textual. The MCP mode exposes play/pause/skip/search as tool calls that Claude Code can invoke autonomously.

The "reactive" feature monitors coding events (test results, build status) through the MCP event stream and changes the music mood accordingly — switching to high-energy tracks on test pass, or a dramatic "panic" visualizer on failure.

## Architecture

```
┌─────────────────────────────────────────────┐
│ Claude Code (or any MCP client)             │
│   ↕ MCP JSON-RPC (stdin/stdout)            │
├─────────────────────────────────────────────┤
│ codebeat --mcp                              │
│   ├── mcp_server.py    (tool definitions)   │
│   ├── player.py        (playback engine)    │
│   ├── sources/                              │
│   │    ├── apple_music.py (API wrapper)     │
│   │    ├── qq_music.py    (API wrapper)     │
│   │    └── local.py       (file scanner)    │
│   ├── lyrics.py        (synced LRC parser)  │
│   ├── tui.py           (Rich/Textual UI)    │
│   └── events.py        (reactive triggers)  │
└─────────────────────────────────────────────┘
```

**Key dependencies:** Python 3.10+, `rich`, `textual`, `pydub` or `pygame` for audio, `httpx` for API calls.

**Data flow:**
1. User (or Claude) triggers a tool call (e.g., `play_track`).
2. `mcp_server.py` dispatches to `player.py`.
3. Player fetches audio from the configured source.
4. TUI renders progress bar + synced lyrics via `lyrics.py`.
5. `events.py` listens for coding signals and can override current playlist/mood.

## Limitations

- Apple Music and QQ Music require valid credentials / region access.
- Audio playback depends on system audio drivers — headless CI won't produce sound.
- MCP mode is stdio-based; only one client can connect at a time.
- Lyrics sync requires LRC-format files or API support from the source.
- No Spotify support currently.

## Why it matters for Claude-driven products

- **Agent UX differentiation:** Adding ambient/reactive audio to an AI coding session is a novel UX layer that makes the tool feel more "alive" — relevant for agent factories building branded developer experiences.
- **MCP pattern reference:** Clean example of wrapping a media service as an MCP server with tool definitions, useful as a template for other non-code integrations (notifications, dashboards, IoT).
- **Event-driven agent behavior:** The "panic on test fail" pattern demonstrates how agents can react to external signals, applicable to marketing alert systems or voice AI mood adaptation.
