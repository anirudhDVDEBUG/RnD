---
name: youtube_research_mcp
description: |
  Set up and use the YouTube Research MCP server for extracting transcripts, comments, and channel analysis from YouTube videos as AI research sources.
  TRIGGER when: user wants to extract YouTube transcripts, analyze YouTube channels, get video comments for research, set up YouTube MCP server, or use YouTube as a research source.
  DO NOT TRIGGER when: user wants to upload videos, edit videos, or interact with YouTube in ways unrelated to research/analysis.
---

# YouTube Research MCP

MCP server that provides YouTube transcripts, comments, and channel analysis as structured AI research sources.

## When to use

- "Get the transcript from this YouTube video"
- "Analyze this YouTube channel's content"
- "Extract comments from a YouTube video for research"
- "Set up YouTube as a research source for my AI workflow"
- "Summarize what this YouTube video is about using its transcript"

## How to use

### 1. Install the MCP server

```bash
# Clone the repository
git clone https://github.com/lee-s-dev/youtube-research-mcp.git
cd youtube-research-mcp

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure as an MCP server

Add to your Claude MCP settings (e.g., `~/.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "youtube-research": {
      "command": "python",
      "args": ["-m", "youtube_research_mcp"],
      "cwd": "/path/to/youtube-research-mcp"
    }
  }
}
```

Alternatively, using `uv`:

```json
{
  "mcpServers": {
    "youtube-research": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/lee-s-dev/youtube-research-mcp", "youtube-research-mcp"]
    }
  }
}
```

### 3. Available tools

Once configured, the following MCP tools become available:

- **get_transcript** — Extract full transcript from a YouTube video URL or ID
- **get_comments** — Retrieve comments from a YouTube video for sentiment/topic analysis
- **analyze_channel** — Get channel metadata, recent uploads, and content patterns
- **search_videos** — Search YouTube for videos matching a query

### 4. Example usage patterns

**Research a topic from video content:**
> "Get the transcript from https://youtube.com/watch?v=XXXXX and summarize the key points"

**Analyze audience sentiment:**
> "Extract comments from this video and identify the main themes"

**Channel analysis:**
> "Analyze this YouTube channel and tell me what topics they cover most frequently"

### 5. API Key (if needed)

Some features (comments, search) may require a YouTube Data API key:

```bash
export YOUTUBE_API_KEY="your-api-key-here"
```

Transcript extraction typically works without an API key.

## References

- Source: https://github.com/lee-s-dev/youtube-research-mcp
- Topics: ai, claude, mcp, mcp-server, transcript, youtube
- Language: Python
