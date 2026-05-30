---
name: watch_video_input
description: |
  Download and analyze videos from YouTube, Instagram, X, Vimeo, or any yt-dlp supported site.
  Extracts frames and transcribes audio locally using mlx-whisper — no API key required.
  TRIGGER: user says /watch, "watch this video", "transcribe this video", "analyze this video",
  "download and transcribe", "extract frames from video", "get video transcript"
---

# Watch — Video Input for Claude Code

Give Claude a video input. Downloads from YouTube, Instagram, X, Vimeo, or any yt-dlp supported site, extracts frames, and transcribes audio locally with mlx-whisper — no API key needed.

## When to use

- "Watch this YouTube video and summarize it"
- "Transcribe this video for me"
- "Analyze the content of this video URL"
- "Download and extract frames from this video"
- "Get the transcript from this video"

## How to use

### Prerequisites

Ensure the following dependencies are installed:

```bash
# Install yt-dlp for video downloading
pip install yt-dlp

# Install mlx-whisper for local transcription (macOS with Apple Silicon)
pip install mlx-whisper

# Install ffmpeg for frame extraction
brew install ffmpeg  # macOS
# or: sudo apt install ffmpeg  # Linux

# Install the watch skill
pip install -e /path/to/watch  # or clone from GitHub
```

### Steps

1. **User provides a video URL** from YouTube, Instagram, X, Vimeo, or any yt-dlp supported platform.

2. **Download the video** using the watch tool:
   ```bash
   python watch.py "<VIDEO_URL>"
   ```
   This will:
   - Download the video via yt-dlp
   - Extract key frames from the video using ffmpeg
   - Transcribe the audio locally using mlx-whisper

3. **Review the output**: The tool produces:
   - Extracted video frames (as images) for visual analysis
   - A full text transcript of the audio
   - Both are made available to Claude for analysis

4. **Analyze the content**: Once frames and transcript are extracted, analyze, summarize, or answer questions about the video content.

### Supported platforms

- YouTube
- Instagram
- X (Twitter)
- Vimeo
- Any site supported by yt-dlp (1000+ sites)

### Notes

- Transcription runs entirely locally via mlx-whisper — no external API keys required
- Best performance on macOS with Apple Silicon (M1/M2/M3/M4) due to MLX optimization
- For Linux or non-Apple Silicon systems, consider using standard whisper instead of mlx-whisper
- Large videos may take longer to process; consider specifying time ranges if only a portion is needed

## References

- **Source repository**: [mathiaschu/watch](https://github.com/mathiaschu/watch)
- **Original project**: Fork of [bradautomates/claude-video](https://github.com/bradautomates/claude-video)
- **yt-dlp**: [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **mlx-whisper**: [ml-explore/mlx-examples](https://github.com/ml-explore/mlx-examples)