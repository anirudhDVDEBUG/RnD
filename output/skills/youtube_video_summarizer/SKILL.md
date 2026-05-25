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
   Extract: `title`, `channel`, `duration_string`, `chapters` (if available), and `description`.

3. **Parse the transcript** file and clean it:
   - Remove duplicate/overlapping subtitle segments
   - Strip formatting tags and timestamps for a clean text transcript
   - If chapters exist in metadata, segment the transcript by chapter timestamps

4. **Optional: Extract key slides/frames**:
   ```bash
   yt-dlp --write-thumbnail --skip-download -o "thumbnail" "<YOUTUBE_URL>"
   ```
   For frame extraction at specific timestamps (e.g., chapter markers):
   ```bash
   ffmpeg -ss <TIMESTAMP> -i "$(yt-dlp -g '<YOUTUBE_URL>')" -frames:v 1 -q:v 2 "slide_<N>.jpg"
   ```
   Note: `ffmpeg` must be installed for slide extraction.

5. **Generate the structured summary** in this markdown format:

   ```markdown
   # <Video Title>

   **Channel:** <Channel Name>
   **Duration:** <Duration>
   **URL:** <YouTube URL>
   **Date Summarized:** <Today's Date>

   ## TL;DR
   <2-3 sentence summary of the entire video>

   ## Key Takeaways
   - <Takeaway 1>
   - <Takeaway 2>
   - <Takeaway 3>
   - ...

   ## Chapter Breakdown
   ### <Chapter 1 Title> (MM:SS)
   <Summary of chapter content>

   ### <Chapter 2 Title> (MM:SS)
   <Summary of chapter content>

   ...

   ## Notable Quotes
   > "<Interesting or impactful quote>" — <Speaker/Context>

   ## Action Items
   - [ ] <Any actionable advice from the video>
   ```

6. **Save the output** to a markdown file:
   - Default location: `./notes/<slugified-video-title>.md`
   - If the user specifies a vault or directory (e.g., Obsidian), save there instead

### Tips

- For videos without auto-generated subtitles, inform the user that no transcript is available
- If the video has no chapters, create logical section breaks based on topic shifts in the transcript
- Keep the TL;DR under 3 sentences
- Limit key takeaways to 5-7 items for readability
- For long videos (>1 hour), consider offering a brief vs. detailed summary option

## References

- Source: [ParthGanatra/agent-skills](https://github.com/ParthGanatra/agent-skills)
- [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp)
