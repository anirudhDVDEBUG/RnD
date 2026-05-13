---
name: social_media_scraper
description: |
  Scrapes any social media post for metadata, comments, transcription, and AI video analysis.
  Supports Instagram, TikTok, Twitter/X, and YouTube.
  TRIGGER: user shares a social media URL or asks to scrape/extract/analyze a social media post.
---

# Social Media Scraper Skill

Scrape any social media post — extract metadata, comments, transcriptions, and AI-powered video analysis. Drop a link, get everything.

## When to use

- "Scrape this Instagram post and get all the comments"
- "Extract metadata from this TikTok video"
- "Transcribe and analyze this YouTube video"
- "What does this Twitter/X post say? Here's the link"
- "Download and analyze the content of this social media post"

## Supported Platforms

- **Instagram** — posts, reels, stories
- **TikTok** — videos
- **Twitter/X** — tweets, video tweets
- **YouTube** — videos, shorts

## Prerequisites

Ensure the following tools are installed and available on PATH:

- **yt-dlp** — media downloading (`pip install yt-dlp` or `brew install yt-dlp`)
- **whisper** — audio transcription (`pip install openai-whisper`)
- **ffmpeg** — media processing (`apt install ffmpeg` or `brew install ffmpeg`)
- **jq** — JSON processing (`apt install jq` or `brew install jq`)
- **Gemini API key** — for AI video analysis (set `GEMINI_API_KEY` environment variable)

## How to use

1. **User provides a social media URL** from any supported platform.

2. **Extract metadata** using yt-dlp:
   ```bash
   yt-dlp --dump-json --no-download "<URL>"
   ```
   This returns JSON with title, description, uploader, view count, like count, comments, upload date, duration, thumbnail URL, and more.

3. **Download the media** (if video/audio analysis is needed):
   ```bash
   yt-dlp -o "/tmp/scrape_%(id)s.%(ext)s" "<URL>"
   ```

4. **Transcribe audio** using Whisper:
   ```bash
   whisper "/tmp/scrape_<id>.<ext>" --model base --output_format txt --output_dir /tmp/
   ```

5. **AI video analysis** using Gemini (if visual analysis is requested):
   - Extract key frames from the video using ffmpeg:
     ```bash
     ffmpeg -i "/tmp/scrape_<id>.<ext>" -vf "fps=1" "/tmp/frames_%04d.jpg"
     ```
   - Send frames to Gemini API for multimodal analysis with a descriptive prompt.

6. **Extract comments** (if available):
   ```bash
   yt-dlp --write-comments --dump-json --no-download "<URL>" | jq '.comments'
   ```

7. **Compile and present results** to the user in a structured format:
   - Post metadata (author, date, engagement metrics)
   - Full text content / caption
   - Audio transcription (if media contained audio)
   - AI visual analysis summary (if video)
   - Top comments (if available)

8. **Clean up** temporary files:
   ```bash
   rm -f /tmp/scrape_* /tmp/frames_*
   ```

## Output Format

Present results in a structured markdown format:

```
### Post Metadata
- **Author:** @username
- **Platform:** Instagram/TikTok/X/YouTube
- **Date:** YYYY-MM-DD
- **Views:** N | **Likes:** N | **Comments:** N

### Content
<caption or description text>

### Transcription
<whisper transcription output>

### Video Analysis
<Gemini multimodal analysis summary>

### Top Comments
1. @user1: comment text (N likes)
2. @user2: comment text (N likes)
```

## Notes

- Always respect rate limits and platform terms of service.
- Some platforms may require cookies for authentication. Use `yt-dlp --cookies` if needed.
- Whisper model sizes: `tiny`, `base`, `small`, `medium`, `large` — use `base` for speed, `medium`+ for accuracy.
- If `GEMINI_API_KEY` is not set, skip the AI video analysis step and inform the user.
- Clean up all temporary files after processing.
