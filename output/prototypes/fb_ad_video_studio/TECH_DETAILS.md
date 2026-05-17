# Technical Details - FB Ad Video Studio

## What It Does

FB Ad Video Studio generates motion-graphics video ads as self-contained HTML files ("HyperFrames compositions"). Given a product brief with 5 copy lines (hook, problem, solution, proof, CTA), it produces an animated HTML page with CSS keyframe animations, timed frame transitions, and platform-specific viewport sizing. The output includes audio pipeline timing cues (voiceover timestamps, SFX triggers, background track metadata) and a reverse-template JSON that can be reused for future ads with different content.

The core insight is that most short-form video ads are essentially animated text + color + timing — which HTML/CSS can represent perfectly. This makes ad creation programmable, versionable, and composable inside Claude Code without any video editing software.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `fb_ad_composer.py` | Core library: AdBrief dataclass, frame builder, HTML generator, audio cue generator, template exporter |
| `demo.py` | CLI demo that creates a sample ad and prints structured output |
| `run.sh` | Entry point for `bash run.sh` execution |

### Data Flow

```
AdBrief (product + copy + platform)
    |
    v
build_frames() -> 5 Frame objects with timing/animation/color
    |
    +---> generate_html()       -> ad_composition.html (playable in browser)
    +---> generate_audio_cues() -> audio_cues.json (voiceover + SFX timing)
    +---> generate_template()   -> template.json (reusable structure)
```

### Dependencies

- **Runtime:** Python 3.10+ standard library only (dataclasses, json, os)
- **Optional:** Playwright (HTML-to-video rendering), pydub (audio mixing), ElevenLabs SDK (AI voiceover)
- **No API keys required** for core composition

### How the HTML Composition Works

Each "frame" is an absolutely-positioned div with:
- CSS keyframe animation (slide-up, scale-bounce, shake, fade-in, pulse)
- Transition effect when entering (fade, slide-left, zoom-in)
- Timer bar showing progress within each frame
- JavaScript sequencer that shows/hides frames based on duration timing

The composition auto-plays in-browser and includes a control panel showing current section, elapsed time, and platform specs.

## Limitations

- **No actual video file output** without Playwright or similar headless renderer — produces HTML preview only
- **No real audio mixing** — generates timing cues JSON but doesn't produce WAV/MP3 files
- **No AI copy generation** — requires you to write the 5 ad copy lines (hook, problem, solution, proof, CTA)
- **No image/video asset support** — text and color only; no product photos or B-roll
- **No direct Facebook/Meta API integration** — you still upload the rendered video manually
- **Template system is structural only** — captures timing and animation patterns, not visual design assets

## Why It Matters

For teams building Claude-driven marketing and ad-creative pipelines:

1. **Programmatic ad generation** — Compose ads as data structures, enabling A/B test variant generation at scale
2. **Claude Code skill integration** — Natural language triggers let marketers describe an ad and get a working composition without touching code
3. **Reverse-template workflow** — Analyze competitor ads, extract their timing/structure pattern, and generate new ads using that proven template with your content
4. **Version control for creatives** — Ad compositions are plain text (HTML + JSON), so they diff, branch, and review like code
5. **Agency automation** — Feed client briefs into the composer to batch-produce platform-specific ad variants across FB/IG/TikTok simultaneously
