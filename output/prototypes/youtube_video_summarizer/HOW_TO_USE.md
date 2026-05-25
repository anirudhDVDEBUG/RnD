# How to Use

## Install

The summarizer is pure Python (stdlib only). The only external tool is `yt-dlp` for fetching transcripts from YouTube.

```bash
# Install yt-dlp (pick one)
pip install yt-dlp        # pip
brew install yt-dlp       # macOS Homebrew
sudo apt install yt-dlp   # Debian/Ubuntu

# Optional: ffmpeg for slide/frame extraction
sudo apt install ffmpeg   # or: brew install ffmpeg
```

No Python pip dependencies are required -- the summarizer uses only the standard library.

## As a Claude Code Skill

This is a **Claude Code skill**. To install:

1. Copy the `SKILL.md` file into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/youtube_video_summarizer
   cp SKILL.md ~/.claude/skills/youtube_video_summarizer/SKILL.md
   ```

2. Also copy `summarizer.py` alongside it (or anywhere on your PATH):
   ```bash
   cp summarizer.py ~/.claude/skills/youtube_video_summarizer/
   ```

3. Claude Code will automatically pick up the skill. Use these **trigger phrases**:
   - "Summarize this YouTube video: [URL]"
   - "Give me the key takeaways from this video"
   - "Create notes from this YouTube video"
   - "Extract chapters and highlights from [URL]"
   - "Transcribe and summarize this video for me"

When triggered, Claude will run `yt-dlp` commands to fetch the transcript and metadata, then generate a structured markdown summary following the template in `SKILL.md`.

## As a Standalone CLI

```bash
# Summarize a real video
python3 summarizer.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Specify output directory
python3 summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --output my_notes/

# Run with mock data (no network needed)
python3 summarizer.py --mock
```

## First 60 Seconds

```
$ bash run.sh

=== YouTube Video Summarizer ===

[mock mode] Using built-in demo data (no network required)
Generating structured summary...
Summary saved to: notes/how-transformers-work---a-detailed-explanation.md

--- Generated Summary Preview ---

# How Transformers Work - A Detailed Explanation

**Channel:** AI Academy
**Duration:** 18:42
**URL:** https://www.youtube.com/watch?v=EXAMPLE123
**Date Summarized:** 2026-05-25

## TL;DR
Today we'll explore how the architecture behind ChatGPT and Claude actually works.
Transformers were introduced in the landmark paper Attention Is All You Need in 2017.
Before transformers, recurrent neural networks were the go-to for sequence modeling.

## Key Takeaways
- Transformers solved this by replacing recurrence with a mechanism called self-attention.
- The core idea is to compute three vectors for each token: a query, a key, and a value.
- This is the fundamental building block.
- The key takeaway is that transformers achieve parallelism and expressiveness simultaneously.
- Positional encoding is crucial.

## Chapter Breakdown
### Introduction (0:00)
...
### Self-Attention Mechanism (2:00)
...

=== Done. See notes/ directory for output. ===
```

Output is a clean markdown file ready for Obsidian, Notion import, or any markdown reader.
