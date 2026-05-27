# Technical Details — Director SKILL

## What It Does

Director SKILL is a Claude Code skill that transforms natural-language scene descriptions into structured cinematic outputs: shot lists, keyframe image-generation prompts, and platform-specific AI video prompts. It encodes the visual grammar of 10 iconic film directors — lens choices, lighting setups, color grades, composition rules, and camera movements — and applies them as "style overlays" to any scene.

The skill itself (SKILL.md) is a prompt-engineering artifact: it instructs Claude to produce filmmaker-quality output structured for downstream AI tools. The companion Python module (`director_skill.py`) is a standalone implementation of the same logic that runs without Claude, using rule-based heuristics and a director style database.

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Scene text   │────▶│ Scene Analyzer   │────▶│ Shot List Generator │
│ + director   │     │ (element extract) │     │ (5-shot structure)  │
└──────────────┘     └──────────────────┘     └────────┬────────────┘
                                                       │
                                          ┌────────────┼────────────┐
                                          ▼            ▼            ▼
                                   ┌────────────┐ ┌────────┐ ┌──────────┐
                                   │ Keyframe   │ │ Video  │ │ JSON     │
                                   │ Prompts    │ │ Prompts│ │ Export   │
                                   └────────────┘ └────────┘ └──────────┘
```

### Key Files

| File | Purpose |
|---|---|
| `SKILL.md` | The Claude Code skill definition — drop into `~/.claude/skills/` |
| `director_skill.py` | Standalone Python implementation (stdlib only) |
| `run.sh` | End-to-end demo runner |

### Data Flow

1. **Scene Analyzer** — Rule-based extraction of setting (interior/exterior), time of day, mood, presence of characters/nature/architecture, scale (epic/intimate).
2. **Director Style DB** — 10 director entries, each with: lens, lighting, color grade, composition rules, camera movement vocabulary, and signature motifs.
3. **Shot List Generator** — Maps scene elements to a 5-shot structure (establishing → approach → detail → reveal → contemplation), adapting shot types and movements per director style.
4. **Keyframe Prompt Generator** — Combines shot descriptions with director visual language into detailed image-generation prompts (aspect ratio, film grain, lens specs).
5. **Video Prompt Generator** — Platform-aware templates (Runway, Kling, Veo) wrapping motion descriptions, camera behavior, and style notes.

### Dependencies

- **Python 3.7+** (stdlib only: `json`, `textwrap`, `sys`, `dataclasses`)
- No external packages, no API keys, no network calls

### Model Calls

- The standalone Python demo makes **zero LLM calls** — it's pure rule-based.
- When used as a Claude Code skill, the SKILL.md prompt shapes Claude's responses — Claude itself generates the creative output, guided by the director style specifications in the skill.

## Limitations

- **Rule-based scene analysis** — The standalone Python module uses keyword matching, not NLP. Complex or ambiguous scenes may get generic treatment. The Claude Code skill (via Claude) handles nuance much better.
- **Fixed 5-shot structure** — Every scene gets exactly 5 shots. Real filmmaking varies shot count by scene complexity. The Claude skill is more flexible.
- **No actual video generation** — This produces prompts for Runway/Kling/Veo, not the videos themselves. Users still need accounts and credits on those platforms.
- **Director styles are approximations** — The 10 styles are distilled signatures, not comprehensive filmography analysis. They capture the most recognizable visual traits.
- **No audio/sound design** — Purely visual — no dialogue, music, or sound effect prompts.
- **English only** — Scene descriptions and outputs are in English.

## Why It Matters for Claude-Driven Products

**Ad Creatives / Marketing**: Marketers can describe a product scene and instantly get production-quality shot lists and video prompts. Instead of hiring a storyboard artist for initial concepting, they get Kubrick-precision or Spielberg-warmth applied to their brand story in seconds. Feed the video prompts directly into Runway or Kling for rapid ad creative generation.

**Agent Factories**: This skill demonstrates a pattern — encoding domain expertise (cinematography) as a reusable Claude Code skill. The same architecture works for any structured creative output: music production, game design, architecture visualization. It's a template for building specialized creative agents.

**Lead-Gen Content**: Video-first content pipelines (TikTok, YouTube Shorts, Instagram Reels) need cinematic frameworks. This skill lets a single operator produce director-grade shot plans that feed AI video tools, enabling solo creators to compete with production teams.

**Voice AI Integration**: The structured shot list format (numbered shots with durations) maps cleanly to voice-narrated storyboard presentations — useful for pitching concepts to clients or stakeholders via voice-AI interfaces.
