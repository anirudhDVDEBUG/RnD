# Technical Details — AI Media Prompt Generator

## What It Does

The AI Media Generator is a Claude Code Skill — a `SKILL.md` file that injects expert-level prompt engineering instructions into Claude's context when triggered. It transforms vague creative briefs ("make me a cool product shot") into platform-specific, cinematically-structured prompts optimized for 14+ generative AI platforms across three media categories: image, video, and music.

The skill encodes the vocabulary and syntax conventions of each platform so that Claude acts as a senior creative director who knows exactly how Midjourney flags differ from Stable Diffusion tags, how Sora expects scene descriptions versus Kling's motion controls, and how Suno's lyric formatting works.

## Architecture

### How Claude Code Skills Work

```
User says trigger phrase
        |
        v
Claude Code loads SKILL.md into context
        |
        v
Claude generates platform-optimized prompt
        |
        v
(Optional) Claude opens browser to target platform and submits
```

There is **no backend, no API server, no running process**. The skill is a prompt-engineering document that Claude reads and follows. All "computation" happens inside Claude's inference.

### Key Files (Source Repo)

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill definition — trigger phrases, platform specs, cinematic vocabulary, prompt templates |

### Key Files (This Prototype)

| File | Purpose |
|------|---------|
| `media_prompt_generator.py` | Standalone Python demo of the prompt-crafting logic |
| `run.sh` | Runs the demo end-to-end |

### Data Flow

1. **Input**: User describes creative vision (subject, mood, platform preference)
2. **Platform selection**: Claude matches intent to one of 14 platforms or recommends one
3. **Prompt layering**: Claude builds the prompt in structured layers:
   - Subject/action description
   - Environment/setting
   - Lighting and color grading
   - Camera specs (lens, shot type, movement)
   - Platform-specific syntax and parameters
   - Negative prompts (where supported)
4. **Output**: Ready-to-paste prompt with parameters
5. **Execution** (optional): Browser automation to submit the prompt

### Dependencies

- Claude Code (any version that supports skills)
- A browser (for optional platform execution)
- No Python/Node/API keys required for the skill itself

## Limitations

- **No actual generation**: The skill crafts prompts but doesn't call any generation API directly. It relies on browser-based execution (opening the platform's web UI).
- **Platform syntax drift**: AI platforms frequently change their prompt syntax, parameters, and capabilities. The skill's platform knowledge may lag behind the latest updates.
- **Browser automation fragility**: The "open in browser and submit" step depends on platform UI structure, which can break with site redesigns.
- **No image/video input**: The skill generates text prompts only. It doesn't handle image-to-image, video-to-video, or reference image workflows natively.
- **Single-prompt focus**: It crafts one prompt at a time. Batch generation across multiple platforms requires separate invocations.
- **No quality feedback loop**: The skill doesn't see the generated output, so it can't auto-iterate based on results.

## Why It Matters

### For Ad Creative / Marketing Teams
Eliminates the prompt-engineering bottleneck. A marketer can describe a campaign concept in plain English and get production-ready prompts for Midjourney (hero images), Sora (video ads), and Suno (jingles) — all from one conversation. This collapses the "creative brief -> prompt engineer -> revision cycle" into seconds.

### For Agent Factories
Demonstrates a pure-skill pattern: no infrastructure, no API server, no dependencies. Just a `SKILL.md` that turns Claude into a domain expert. This is the lightest-weight way to extend Claude Code's capabilities and a template for building other domain-specific skills.

### For Lead-Gen / Content Pipelines
Enables programmatic creative asset generation at scale. Pair this with a content calendar agent and you have automated visual/audio content for social media, email campaigns, or landing pages.

### For Voice AI / Multimodal Products
The music prompt generation (Suno/Udio) is directly applicable to products that need custom audio — hold music, podcast intros, branded sound. The video prompts feed into short-form video pipelines for TikTok/Reels content.
