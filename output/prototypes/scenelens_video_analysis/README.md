# SceneLens Video Analysis

**TL;DR:** Scene-aware frame extraction + per-frame OCR + auto-chunked Whisper transcripts — gives Claude (or any LLM) structured video understanding without dumping every frame.

## Headline Result

```
$ bash run.sh
[SceneLens] Extracted 8 keyframes from 2m30s video (vs 150 at 1fps)
[SceneLens] OCR detected text in 5/8 frames
[SceneLens] Whisper transcript: 3 chunks, 847 words

Frame 3 (00:01:12): "Deploy with docker-compose up -d"
Frame 5 (00:01:48): "SELECT * FROM users WHERE active = true"
Transcript chunk 1: "In this tutorial we'll set up a production deployment..."
```

## Quick Links

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Install, configure as Claude skill, first 60 seconds
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture, data flow, limitations
- [run.sh](./run.sh) — End-to-end demo (no API keys needed, uses mock data)
