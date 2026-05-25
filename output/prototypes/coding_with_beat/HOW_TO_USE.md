# How to Use Coding with Beat

## Install

```bash
# Option A: pip (recommended)
pip install coding-with-beat

# Option B: from source
git clone https://github.com/jaychempan/coding-with-beat.git
cd coding-with-beat
pip install -e .
```

## Run as standalone TUI player

```bash
codebeat                              # launch with default settings
codebeat --source apple-music         # Apple Music source
codebeat --source qq-music            # QQ Music source
codebeat --source local --path ~/Music  # local files
```

## Configure as MCP server for Claude Code

Add to `~/.claude.json` under the `mcpServers` block:

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

Once active, ask Claude: "play some lofi while I code", "skip track", "show lyrics", "panic mode".

## Install as a Claude Code Skill

```bash
mkdir -p ~/.claude/skills/coding_with_beat
cp SKILL.md ~/.claude/skills/coding_with_beat/SKILL.md
```

Trigger phrases: "play music", "background music", "coding DJ", "terminal music player", "code beat"

## First 60 seconds

```
$ pip install coding-with-beat
$ codebeat --source local --path ~/Music

  ╔══════════════════════════════════════╗
  ║  CODEBEAT DJ v1.0                   ║
  ║  Now Playing: lofi_chill_01.mp3     ║
  ║  ▶ ━━━━━━━━━━━━━━━━━━━━━ 2:14/3:45 ║
  ║                                     ║
  ║  ♪ "writing code at 3am..."         ║
  ║  ♪ "the bugs don't stand a chance"  ║
  ╚══════════════════════════════════════╝

  [n]ext  [p]ause  [s]kip  [q]uit
```

When a test fails (via MCP event hook), the player switches to "panic mode" — red visuals, faster BPM track.

## Demo (no install needed)

```bash
bash run.sh
```

This runs a mock version showing the TUI layout, playlist management, and event-reactive mode changes.
