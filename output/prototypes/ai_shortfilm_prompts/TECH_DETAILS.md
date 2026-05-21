# Technical Details

## What it does

This is a structured prompt engineering methodology (packaged as a Claude Code skill and a standalone Python CLI) for producing AI short films with video generation models. It encodes the production workflow behind *Zombie Scavenger* by Mx-Shell into a repeatable 4-phase process: story development, visual direction, model-specific prompt engineering, and production assembly. The output is a set of concrete, copy-paste-ready prompts optimized for a target video model (Sora, Kling, Veo, Seedance, or Jimeng).

The CLI demo (`generate_prompts.py`) generates a complete prompt package for a 90-second post-apocalyptic short film ("Last Light") with 4 scenes, 10 shots, character consistency references, and per-model style tuning — entirely offline with no API calls.

## Architecture

```
generate_prompts.py          # Single-file CLI, zero dependencies
  |
  +-- Domain models           dataclasses: ShortFilm, Scene, Shot, Character
  +-- build_prompt()          Assembles shot_type + camera + subject + env + action + lighting + style
  +-- MODEL_STYLE_HINTS       Per-model suffix tuning (photorealism for Sora, motion for Kling, etc.)
  +-- create_demo_film()      Hardcoded "Last Light" demo with 4 scenes / 10 shots
  +-- retarget_film()         Swaps style hints when switching target model
  +-- format_markdown()       Full structured doc output
  +-- format_json()           Machine-readable export
  +-- format_prompts_only()   Raw prompts for direct model input

SKILL.md                     # Claude Code skill definition (methodology + prompt template)
```

**Data flow:** Concept (hardcoded demo or user-provided via skill) -> beat sheet -> scene list -> shot design -> model-specific prompt assembly -> formatted output.

**Dependencies:** Python 3.8+ stdlib only (`json`, `textwrap`, `argparse`, `dataclasses`). No pip packages, no API keys, no network calls.

## Limitations

- **No actual video generation.** This produces prompts, not videos. You still need access to Sora/Kling/Veo/Seedance/Jimeng to generate clips.
- **Demo is hardcoded.** The CLI generates prompts for a single demo film. Custom stories require using the Claude Code skill interactively or extending the Python code.
- **No character consistency enforcement.** The tool encourages verbatim character descriptions across shots, but video models may still produce inconsistent results — that's a model limitation, not a prompt limitation.
- **No audio/music generation.** The methodology covers audio planning but the tool doesn't produce audio prompts or integrate with audio AI models.
- **Model-specific tuning is heuristic.** The style hints per model are based on community best practices as of mid-2025, not formal benchmarks.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Ad creatives / marketing** | Generate storyboarded video ad prompts at scale — hand them to a video model for rapid creative testing. |
| **Agent factories** | The 4-phase methodology is a reusable agentic workflow pattern: decompose creative tasks into structured steps with consistent outputs. |
| **Lead-gen content** | AI short films are attention magnets on social platforms. This skill lets teams produce film-quality prompt packages without a cinematography background. |
| **Voice AI integration** | The production assembly phase includes audio/voiceover planning — pairs naturally with ElevenLabs or other voice AI for complete short film pipelines. |

## Source

- Repository: [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts)
- Methodology: Based on *Zombie Scavenger* by Mx-Shell
