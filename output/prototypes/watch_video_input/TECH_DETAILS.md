# Technical Details — Watch Video Input

## What it does

Watch is a local video-processing pipeline that turns any video URL into structured input for Claude. It chains three open-source tools — yt-dlp for downloading, ffmpeg for frame extraction, and mlx-whisper for transcription — into a single command. The output (a set of key-frame images plus a timestamped transcript) is fed directly to Claude's multimodal context, letting it reason about video content without any cloud transcription API.

The key insight is that Claude can already process images and text but has no native video input. Watch bridges that gap by decomposing video into the modalities Claude already handles well, running entirely on local hardware.

## Architecture

```
User provides URL
       |
       v
  yt-dlp download
  (any of 1000+ sites)
       |
       v
  .watch_output/video.mp4
       |
       +-------> ffmpeg frame extraction
       |           - adaptive interval (shorter video = more frames per minute)
       |           - outputs .watch_output/frames/frame_001.jpg ...
       |
       +-------> ffmpeg audio extraction
                   - extracts audio track to .watch_output/audio.wav
                   |
                   v
                mlx-whisper (local, Apple Silicon optimized)
                   - outputs .watch_output/transcript.txt
                   - timestamped segments
```

### Key files

| File | Role |
|------|------|
| `watch.py` | Main entry point — orchestrates download, frame extraction, transcription |
| `downloader.py` | Wraps yt-dlp with sensible defaults (format selection, output naming) |
| `frame_extractor.py` | Drives ffmpeg to pull key frames at adaptive intervals |
| `transcriber.py` | Runs mlx-whisper (or fallback whisper) for local speech-to-text |

### Dependencies

| Dependency | Purpose | Install |
|-----------|---------|---------|
| **yt-dlp** | Video downloading from 1000+ sites | `pip install yt-dlp` |
| **ffmpeg** | Frame extraction + audio isolation | `brew install ffmpeg` / `apt install ffmpeg` |
| **mlx-whisper** | Local transcription on Apple Silicon | `pip install mlx-whisper` |
| **Pillow** | Image handling for extracted frames | `pip install Pillow` |

### Model calls

- **No external API calls.** Transcription runs entirely via mlx-whisper using the `mlx-community/whisper-large-v3-turbo` model, downloaded once and cached locally (~1.5 GB).
- On first run, the whisper model downloads automatically. Subsequent runs use the cached model.

## Limitations

- **Apple Silicon only (for mlx-whisper):** mlx-whisper requires an M-series Mac. On Linux or Intel Macs, you must swap to `openai-whisper` (slower, CPU-based) or `faster-whisper` (needs CUDA GPU).
- **No streaming:** The entire video must download before processing begins. Long videos (1hr+) can take significant time and disk space.
- **Frame sampling is lossy:** Extracting one frame every few seconds misses fast visual changes. Not suitable for frame-by-frame analysis of action sequences.
- **No speaker diarization:** The transcript is a single stream of text — it does not identify who is speaking.
- **Platform restrictions:** Some sites block yt-dlp or require authentication cookies. DRM-protected content cannot be downloaded.
- **Token limits:** Very long videos produce large transcripts that may exceed Claude's context window. Consider trimming to relevant sections.

## Why this matters

For teams building Claude-driven products:

- **Content analysis at scale:** Marketing teams can ingest competitor videos, webinar recordings, or social media clips and have Claude summarize, extract quotes, or generate derivative content.
- **Ad creative pipelines:** Analyze existing video ads to extract messaging patterns, then feed insights into Claude-powered ad copy generators.
- **Agent factories:** A video-input skill turns Claude Code into a multimedia research agent — point it at a YouTube playlist and get structured analysis.
- **Voice AI training data:** Extract transcripts from domain-specific videos to build prompt libraries or fine-tuning datasets.
- **Lead-gen intelligence:** Monitor competitor YouTube channels, conference talks, or product demos and auto-generate competitive intelligence briefs.
