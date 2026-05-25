---
name: youtube_video_summarizer
description: |
  Summarize YouTube videos into structured notes with TL;DR, key takeaways, chapter breakdowns, and optional slide extraction. Uses yt-dlp to fetch transcripts and generates clean markdown summaries.
  Trigger: user asks to summarize a YouTube video, extract notes from a video, get key takeaways from a YouTube link, create video notes, or transcribe and summarize a video.
---

# YouTube Video Summarizer

Summarize any YouTube video into structured, readable notes with a TL;DR, key takeaways, chapter-by-chapter breakdown, and optional slide extraction.

## When to use

- "Summarize this YouTube video: [URL]"
- "Give me the key takeaways from this video"
- "Create notes from this YouTube video"
- "Extract chapters and highlights from [YouTube URL]"
- "Transcribe and summarize this video for me"

## How to use

### Prerequisites

Ensure `yt-dlp` is installed:

```bash
# macOS
brew install yt-dlp

# pip
pip install yt-dlp
```

### Steps

1. **Fetch the transcript** using `yt-dlp`:
   ```bash
   yt-dlp --write-subs --write-auto-subs --sub-lang en --skip-download --sub-format json3 -o "transcript" "<YOUTUBE_URL>"
   ```
   If JSON3 subtitles are unavailable, fall back to VTT format:
   ```bash
   yt-dlp --write-subs --write-auto-subs --sub-lang en --skip-download --sub-format vtt -o "transcript" "<YOUTUBE_URL>"
   ```

2. **Get video metadata** (title, channel, duration, chapters):
   ```bash
   yt-dlp --dump-json --skip-download "<YOUTUBE_URL>"
   ```

3. **Parse the transcript** file and clean it:
   - Remove duplicate/overlapping subtitle segments
   - Strip formatting tags and timestamps for a clean text transcript
   - If chapters exist in metadata, segment the transcript by chapter timestamps

4. **Optional: Extract key slides/frames**:
   ```bash
   yt-dlp --write-thumbnail --skip-download -o "thumbnail" "<YOUTUBE_URL>"
   ```

5. **Generate the structured summary** in markdown format with TL;DR, Key Takeaways, Chapter Breakdown, Notable Quotes, and Action Items.

6. **Save the output** to `./notes/<slugified-video-title>.md`
