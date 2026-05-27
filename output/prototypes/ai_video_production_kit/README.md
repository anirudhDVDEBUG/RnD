# AI Video Production Kit

**TL;DR:** A Claude Code skill + standalone prompt engine that generates optimized prompts for 15 AI video models (Kling, Runway, Sora, Veo, Seedance, Wan, CogVideoX, etc.) using a 5-layer structure — camera, subject, action, environment, style. It also scores and ranks models for your specific use case, budget, and platform.

## Headline Result

```
INPUT:  "Product shot of wireless headphones, commercial style, YouTube, high budget"

OUTPUT: Smooth dolly-in shot, a sleek wireless headphone rotating slowly
        on a marble pedestal, softly flowing, soft golden hour sunlight
        through floor-to-ceiling windows...

        Model recommendation: Veo 3 (score: 63) > Runway Gen-3 Alpha (58) > Sora (43)
```

Covers 4 demo scenarios out of the box — commercial, social media, cinematic, and enterprise — with zero API keys needed.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the Claude Skill, trigger phrases, interactive mode
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, why it matters

## Source

[cclank/lanshu-awesome-ai-video-kit](https://github.com/cclank/lanshu-awesome-ai-video-kit) — 411 prompts, 15 models, 7 Claude Skills, 14 methodology articles
