# How to Use — YouTube Research MCP

## Install

```bash
git clone https://github.com/lee-s-dev/youtube-research-mcp.git
cd youtube-research-mcp
pip install -r requirements.txt
```

Or install directly with `uv`:

```bash
uvx --from git+https://github.com/lee-s-dev/youtube-research-mcp youtube-research-mcp
```

## Configure as an MCP Server

Add the following to your `~/.claude.json` (or project `.mcp.json`) inside the `mcpServers` block:

### Option A — local clone

```json
{
  "mcpServers": {
    "youtube-research": {
      "command": "python",
      "args": ["-m", "youtube_research_mcp"],
      "cwd": "/absolute/path/to/youtube-research-mcp"
    }
  }
}
```

### Option B — via uvx (no clone needed)

```json
{
  "mcpServers": {
    "youtube-research": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/lee-s-dev/youtube-research-mcp",
        "youtube-research-mcp"
      ]
    }
  }
}
```

### Optional: YouTube API key

Comments, search, and channel analysis use the YouTube Data API v3 when a key is available. Set it in the MCP config:

```json
{
  "mcpServers": {
    "youtube-research": {
      "command": "python",
      "args": ["-m", "youtube_research_mcp"],
      "cwd": "/absolute/path/to/youtube-research-mcp",
      "env": {
        "YOUTUBE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Transcript extraction works **without** an API key (uses `youtube-transcript-api`).

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_transcript` | Extract full transcript from a YouTube video URL or ID |
| `get_comments` | Retrieve top comments for sentiment/topic analysis |
| `analyze_channel` | Channel metadata, recent uploads, content patterns |
| `search_videos` | Search YouTube for videos matching a query |

## First 60 Seconds

After adding the MCP config above and restarting Claude Code:

**Input (in Claude):**
> Get the transcript from https://www.youtube.com/watch?v=dQw4w9WgXcQ and summarize the key points

**Output:**
Claude calls `get_transcript` with the URL, receives the full text of all transcript segments, and produces a structured summary with key points, timestamps, and topics covered.

**Input:**
> Analyze the comments on that video — what are the main themes?

**Output:**
Claude calls `get_comments`, receives structured comment data (author, text, likes, date), and identifies recurring themes, sentiment breakdown, and notable questions from the audience.

**Input:**
> What topics does this channel cover most?

**Output:**
Claude calls `analyze_channel`, gets subscriber count, recent uploads, and top topics, then reports content patterns and coverage areas.

## Running the Demo Locally

```bash
bash run.sh
```

This exercises all 4 tools with mock data and prints structured output — no API key needed.
