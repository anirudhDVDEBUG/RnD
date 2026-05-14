# Technical Details — AI Video Pipeline

## What It Does

This pipeline takes a text topic and produces a complete narrated video (MP4) through four automated stages: (1) an LLM generates a structured script with per-scene narration and visual descriptions, (2) stock images matching each visual description are fetched from Pexels, (3) Edge-TTS converts narration text to speech audio, and (4) MoviePy composites images with their corresponding audio tracks into a single video file with transitions.

The entire stack runs on free-tier APIs. No GPU is required. A mock mode replaces all external calls with locally generated placeholders (colored images, silent WAV audio) so the pipeline can be evaluated without any API keys.

## Architecture

```
topic (string)
    |
    v
[Groq LLM] ── script (JSON: scenes[{narration, visual}])
    |
    +──> [Pexels API] ── image_0.jpg, image_1.jpg, ...
    |
    +──> [Edge-TTS]   ── audio_0.wav, audio_1.wav, ...
    |
    v
[MoviePy]  ── final_video.mp4
```

### Key Files

| File | Purpose |
|------|---------|
| `pipeline.py` | Single-file pipeline: script gen, image fetch, TTS, assembly |
| `run.sh` | One-command demo runner (creates venv, installs deps, runs mock) |
| `requirements.txt` | Python dependencies |
| `.env` | API keys (user-created, not committed) |

### Data Flow

1. **Script generation** — `generate_script()` sends a structured prompt to Groq's `llama-3.3-70b-versatile` requesting JSON output with `narration` + `visual` per scene. Uses `response_format={"type": "json_object"}` for reliable parsing.
2. **Image sourcing** — `fetch_image()` queries Pexels search API with each scene's `visual` field, downloads the first `large2x` result. Falls back to a Pillow-generated placeholder if no results.
3. **Voiceover** — `generate_voiceover()` uses `edge_tts.Communicate` (async) to synthesize each scene's narration. Default voice: `en-US-AriaNeural`.
4. **Assembly** — `assemble_video()` creates MoviePy `ImageClip`s sized to audio duration, resized to 720p, concatenated with `compose` method, rendered at 24fps with libx264/AAC.

### Dependencies

| Package | Role | Why this one |
|---------|------|--------------|
| `groq` | LLM API client | Fastest free inference for Llama models |
| `requests` | HTTP for Pexels | Lightweight, no extra deps |
| `edge-tts` | Text-to-speech | Free, no API key, many voices/languages |
| `moviepy` | Video compositing | Python-native, wraps ffmpeg |
| `Pillow` | Placeholder images | Used only in mock mode |
| `python-dotenv` | Env config | Standard .env loading |

External: `ffmpeg` (system package, required by MoviePy).

## Limitations

- **No real video clips** — sources still images from Pexels, not video. Each scene is a static image with audio overlay. Adding Pexels video search would be a straightforward extension.
- **No subtitles/captions** — MoviePy's `TextClip` could add burned-in captions but requires ImageMagick, adding install complexity.
- **No transitions** — scenes cut directly. Crossfade/fade-to-black could be added via MoviePy transitions.
- **Single-threaded** — image downloads and TTS run sequentially. Could be parallelized with `asyncio.gather` or `concurrent.futures`.
- **Pexels rate limit** — 200 req/hr on free tier. Fine for 3-10 scene videos, not for batch production.
- **Script quality depends on prompt** — the Groq prompt is minimal. Production use would benefit from few-shot examples and guardrails.
- **No caching** — re-runs re-download everything. A content-addressed cache would avoid redundant API calls.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Marketing / Ad Creatives** | Auto-generate explainer or promo videos from a product description. Feed a landing page brief → get a 60-second video. |
| **Lead-gen Content** | Produce SEO video content at scale: blog post → video → YouTube/TikTok upload pipeline. |
| **Agent Factories** | Embed as a tool in a larger agent: "research topic → write script → produce video → post to social". Each stage is a composable function. |
| **Voice AI** | Edge-TTS integration demonstrates how to add voice output to any agent workflow without cost. Swap in ElevenLabs or OpenAI TTS for higher quality. |
| **Rapid Prototyping** | The mock mode lets you test the full flow instantly, then flip to live APIs when ready — a pattern useful for any multi-API agent pipeline. |

## References

- Source: [MYounus-Codes/ai-video-pipeline](https://github.com/MYounus-Codes/ai-video-pipeline)
- [Groq Console](https://console.groq.com) | [Pexels API](https://www.pexels.com/api/) | [Edge-TTS](https://pypi.org/project/edge-tts/) | [MoviePy](https://zulko.github.io/moviepy/)
