# AI Video Pipeline

**Fully automated text-to-video generation: give it a topic, get back a narrated MP4.** Uses Groq (LLM script writing), Pexels (stock images), Edge-TTS (voiceover), and MoviePy (video assembly) — all free-tier APIs.

## Headline Result

```
$ bash run.sh
=== AI Video Pipeline — Demo ===
--- Step 1: Script Generation ---
  Scene 1: Welcome to our exploration of The Future of AI...
--- Step 2: Image Sourcing ---
--- Step 3: Voiceover Generation ---
--- Step 4: Video Assembly ---
Video saved to: output/final_video.mp4
```

One command, zero API keys needed (mock mode), produces a playable `.mp4` in `output/`.

## Quick Start

```bash
bash run.sh          # mock mode, no keys needed
```

For live mode with real AI-generated content:

```bash
cp .env.example .env  # add your GROQ_API_KEY and PEXELS_API_KEY
python3 pipeline.py "Solar Energy" 5
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, configure, run in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, data flow, limitations
