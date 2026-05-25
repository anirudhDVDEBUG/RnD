---
name: coding_with_beat
description: |
  Play background music in the terminal while coding with Claude Code. Uses coding-with-beat to run a retro pixel DJ with Apple Music, QQ Music, or local files — synced lyrics, smart playlists, and reactive audio that responds to coding events like test failures.
  Triggers: play music, background music, coding DJ, terminal music player, code beat
---

# Coding with Beat — Terminal Music Player for Claude Code

A retro pixel DJ for your AI coding terminal. Play music, display synced lyrics, and react to coding events (e.g., panic mode when tests fail).

## When to use

- "Play some music while I code"
- "Set up background music in the terminal"
- "I want a coding DJ / lofi beats while working"
- "Add music player to my Claude Code session"
- "Play Apple Music / QQ Music in the terminal"

## How to use

### 1. Install coding-with-beat

```bash
# Install via pip
pip install coding-with-beat

# Or clone and install from source
git clone https://github.com/jaychempan/coding-with-beat.git
cd coding-with-beat
pip install -e .
```

### 2. Run as a standalone terminal music player

```bash
# Launch the TUI music player
codebeat

# Or with specific music source
codebeat --source apple-music
codebeat --source qq-music
codebeat --source local --path ~/Music
```

### 3. Configure as an MCP server for Claude Code

Add to your Claude Code MCP configuration (`.mcp.json` or via `claude mcp add`):

```json
{
  "mcpServers": {
    "codebeat": {
      "command": "codebeat",
      "args": ["--mcp"]
    }
  }
}
```

Or via CLI:
```bash
claude mcp add codebeat -- codebeat --mcp
```

### 4. Use within Claude Code

Once configured, ask Claude to:
- Play/pause/skip music tracks
- Search and queue songs
- Show current lyrics
- Switch music sources (Apple Music, QQ Music, local files)
- React to coding events (tests passing/failing)

### Key Features

- **Retro pixel DJ TUI** — beautiful terminal-based music player interface
- **Synced lyrics display** — see lyrics in real-time as music plays
- **Multiple music sources** — Apple Music, QQ Music, or local files
- **Smart playlists** — AI-powered song selection for coding sessions
- **Coding event reactions** — music reacts when tests fail or pass
- **MCP integration** — control music directly from Claude Code

## References

- GitHub: https://github.com/jaychempan/coding-with-beat
- Website: https://codebeat.top/
