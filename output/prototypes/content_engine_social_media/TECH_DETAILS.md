# Tech Details: Content Engine - Social Media

## What It Does

The Content Engine is a single-script Python pipeline that takes one topic and produces five platform-adapted social media posts plus one AI-generated image. It defines channel specs (character limits, tone, format) for Twitter/X, LinkedIn, Instagram, Facebook, and Blog/Newsletter, then generates tailored content for each. In live mode, it calls Groq's API for fast LLM inference (llama-3.1-8b-instant) and fal-ai's nano-banana-2 for image generation. In mock mode, it uses deterministic templates so the pipeline runs end-to-end with zero API keys.

As a Claude Code skill, it's designed to be triggered conversationally -- the user says "create social media content about X" and Claude orchestrates the entire pipeline in one exchange, including optional review/edit before auto-publishing through Upload-Post.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `content_engine.py` | Full pipeline: content gen, image gen, publish, manifest output |
| `SKILL.md` | Claude Code skill definition with trigger phrases |
| `run.sh` | Standalone demo runner |
| `requirements.txt` | Optional API dependencies (groq, fal-client) |

### Data Flow

```
Topic (string)
  |
  v
[Content Generation] -- Groq API or mock templates
  |  Produces 5 channel-adapted posts with platform constraints
  v
[Image Generation] -- fal-ai nano-banana-2 or SVG placeholder
  |  Single visual asset sized for social sharing
  v
[Publishing] -- Upload-Post integration (stub)
  |  Posts to configured social channels
  v
output/
  manifest.json      -- full structured output
  post_*.txt         -- individual post files
  generated_image.*  -- visual asset
```

### Dependencies

- **Python 3.10+** (stdlib only for mock mode)
- **groq** (optional) - Groq API client for LLM content generation
- **fal-client** (optional) - fal-ai client for nano-banana-2 image generation
- **Upload-Post** (external) - auto-publishing integration (not bundled)

### Model Calls

| Service | Model | Purpose |
|---|---|---|
| Groq | llama-3.1-8b-instant | Per-channel post generation (5 calls per run) |
| fal-ai | nano-banana-2 | Image generation (1 call per run) |

## Limitations

- **No Upload-Post bundled**: Publishing is stubbed out. You need to configure Upload-Post separately for actual social media posting.
- **No content approval loop in standalone mode**: The review/edit step only works when invoked as a Claude skill (Claude acts as the approval layer).
- **Single image**: Generates one image for all channels rather than platform-optimized sizes/crops.
- **No scheduling**: Content is generated and published immediately. No queue or calendar integration.
- **Template quality**: Mock mode uses fixed templates; real quality depends on Groq model output.
- **No analytics**: Doesn't track post performance or engagement after publishing.

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / Marketing**: Demonstrates a pattern for turning one content brief into multi-channel campaigns with a single agent conversation -- directly applicable to marketing automation.
- **Ad Creatives**: The image generation + platform-adapted copy pattern generalizes to ad creative pipelines where you need visuals + copy variants per placement.
- **Agent Factories**: Shows how to package a multi-step agentic workflow as a Claude Code skill that triggers on natural language -- a reusable pattern for any "topic in, artifacts out" pipeline.
- **Content at Scale**: The channel-spec architecture (max chars, style, format) is extensible -- add TikTok scripts, YouTube descriptions, or email sequences by defining new channel entries.

## Source

[iamasters-academy/content-engine](https://github.com/iamasters-academy/content-engine)
