# Technical Details

## What SceneLens Does

SceneLens is a Python library that converts video into structured, LLM-friendly data. Instead of naively extracting frames at fixed intervals (which produces hundreds of redundant frames), it uses scene-change detection to pick only visually distinct keyframes. Each keyframe is then passed through Tesseract OCR to extract on-screen text. Audio is transcribed via OpenAI Whisper with automatic chunking to handle long videos without OOM errors.

The result is a compact representation of video content — a handful of keyframes with OCR text plus a full transcript — that fits comfortably in an LLM context window.

## Architecture

```
Video File / YouTube URL
        |
        v
  [ffmpeg scene detect]  -->  Keyframe PNGs (threshold-based)
        |                           |
        v                           v
  [Whisper transcribe]      [Tesseract OCR per frame]
   (auto-chunked)                   |
        |                           v
        v                     ocr_results.json
  transcript.txt
        |
        v
  summary.json (combined output)
```

### Key Files (in the `scenelens` package)

| File | Role |
|------|------|
| `scenelens/extract.py` | Scene detection via ffmpeg `select='gt(scene,0.3)'`, writes keyframes |
| `scenelens/ocr.py` | Tesseract wrapper, batch OCR on extracted frames |
| `scenelens/transcribe.py` | Whisper integration with chunking (splits audio into segments) |
| `scenelens/cli.py` | Click-based CLI (`extract`, `transcribe`, `analyze` commands) |
| `scenelens/core.py` | `SceneLens` class — unified Python API |

### Dependencies

- **ffmpeg** — frame extraction + scene detection + audio splitting
- **tesseract-ocr** — per-frame OCR
- **openai-whisper** (optional) — audio transcription
- **yt-dlp** (optional) — YouTube download
- **Pillow** — image handling
- **numpy** — frame comparison for scene detection fallback

### Data Flow

1. ffmpeg extracts frames where scene-change score > threshold (default 0.3)
2. Frames saved as numbered PNGs with timestamp in filename
3. Each frame passed to Tesseract; results stored as JSON map (filename -> text)
4. Audio extracted via ffmpeg, split into chunks (default 10min), each chunk transcribed by Whisper
5. Chunks merged into single transcript with timestamps

## Limitations

- **No GPU required** but Whisper is slow on CPU (~10x realtime for base model)
- **OCR quality** depends heavily on video resolution and text clarity (works great for slides/terminals, poor for handwritten or stylized text)
- **Scene detection threshold** is a heuristic — fast-cut videos may produce too many frames, static videos too few
- **No speaker diarization** — transcript is a single stream without speaker labels
- **YouTube downloads** may break when yt-dlp falls behind YouTube changes
- **Large videos** (>1hr) can consume significant disk space for frames

## Why This Matters for Claude-Driven Products

| Use Case | Application |
|----------|-------------|
| **Content marketing** | Auto-summarize competitor YouTube videos, extract key claims and stats |
| **Ad creative analysis** | Extract text overlays + scene transitions from ad videos at scale |
| **Agent factories** | Give autonomous agents video understanding without vision API costs per frame |
| **Lead-gen** | Monitor webinar recordings for buying signals, extract CTA text |
| **Voice AI** | Pre-process video meetings into structured data for voice agent context |
| **Knowledge bases** | Convert video libraries into searchable text (OCR + transcript) |

The key insight: scene-aware extraction reduces a 10-minute video from ~600 frames (at 1fps) to ~8-15 keyframes, making it practical to feed video content into LLM context windows without massive token costs.
