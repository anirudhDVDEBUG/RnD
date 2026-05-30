# Watch — Video Input for Claude Code

**Give Claude eyes and ears for any video on the internet.** `/watch <URL>` downloads from YouTube, Instagram, X, Vimeo, or 1000+ sites via yt-dlp, extracts key frames, and transcribes audio locally with mlx-whisper — zero API keys required.

```
> /watch https://www.youtube.com/watch?v=dQw4w9WgXcQ

Downloading video...        done (3m32s, 720p)
Extracting frames...        done (12 frames)
Transcribing audio...       done (mlx-whisper, local)

Transcript: "We're no strangers to love, you know the rules..."
Frames saved to: .watch_output/frames/
```

## Quick Links

| Doc | What you'll find |
|-----|-----------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install steps, skill setup, trigger phrases, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, dependencies, limitations |

## Demo

```bash
bash run.sh
```

Runs a self-contained demo showing the full pipeline with mock data (no network or GPU needed).

## Source

Fork of [bradautomates/claude-video](https://github.com/bradautomates/claude-video) by [mathiaschu/watch](https://github.com/mathiaschu/watch).
