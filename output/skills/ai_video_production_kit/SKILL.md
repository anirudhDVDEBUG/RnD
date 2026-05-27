---
name: AI Video Production Kit
description: |
  Enterprise AI video production toolkit with 411+ prompts across 15 models.
  Helps craft optimized prompts, select models, and manage end-to-end AI video workflows.
  Triggers: "ai video", "video generation prompt", "video model selection",
  "kling prompt", "runway prompt", "sora prompt", "veo prompt",
  "seedance", "wan video", "cogvideox", "hunyuan video"
---

# AI Video Production Kit

Enterprise-grade AI video production skill based on the lanshu-awesome-ai-video-kit. Provides prompt engineering, model selection guidance, and production workflows across 15+ AI video models.

## When to use

- "Help me write a prompt for Kling / Runway / Sora / Veo / Seedance"
- "Which AI video model should I use for this scene?"
- "Generate an AI video prompt for a product demo / cinematic shot / social media ad"
- "Optimize my video generation prompt for better results"
- "Set up an AI video production pipeline for my project"

## Supported Models

| Model | Strengths |
|---|---|
| **Kling** | Chinese market, fast iteration, good motion |
| **Runway Gen** | Creative control, style transfer, compositing |
| **Sora** | Long-form coherence, complex scenes |
| **Veo** | Photorealism, cinematic quality |
| **Seedance** | Dance/motion generation |
| **Wan** | Open-source, customizable |
| **CogVideoX** | Open-source, research-friendly |
| **Hunyuan Video** | Tencent ecosystem, Chinese text |
| **LTX Video** | Lightweight, fast generation |
| **Mochi** | Open-source, high quality |
| **Jimeng** | ByteDance ecosystem |
| **Higgsfield** | Character animation |

## How to use

### 1. Define your video brief

Specify the core parameters:
- **Subject**: What is in the scene (person, product, landscape)
- **Motion**: What movement or action occurs
- **Style**: Cinematic, documentary, commercial, artistic
- **Duration**: Target length (most models: 4-16 seconds)
- **Aspect ratio**: 16:9, 9:16, 1:1

### 2. Select the right model

Consider these factors:
- **Use case**: Commercial vs. creative vs. social media
- **Quality needs**: Draft/preview vs. final render
- **Motion complexity**: Static scene vs. complex choreography
- **Budget**: API cost per generation
- **Platform**: Target distribution (TikTok, YouTube, enterprise)

### 3. Craft the prompt using the 5-layer structure

```
[Camera] + [Subject] + [Action/Motion] + [Environment] + [Style/Mood]
```

**Example prompt (cinematic product shot):**
```
Smooth dolly-in shot, a sleek wireless headphone rotating slowly on a marble pedestal,
soft golden hour sunlight streaming through floor-to-ceiling windows,
minimal modern interior with blurred city skyline in background,
cinematic 4K, shallow depth of field, warm color grading
```

**Example prompt (social media ad):**
```
Dynamic tracking shot, a young woman jogging through a sunlit park,
she stops and takes a sip from a branded water bottle smiling at camera,
vibrant green trees and morning fog, energetic and fresh mood,
vertical 9:16 format, bright natural lighting
```

### 4. Iterate and refine

- Start with a simple prompt, then add detail layer by layer
- Use negative prompts where supported (e.g., "no distortion, no extra fingers")
- Adjust motion intensity keywords: "slowly", "gradually", "dynamically", "explosively"
- Specify camera movements explicitly: dolly, pan, tilt, crane, handheld, steadicam

### 5. Production pipeline

For enterprise video projects:
1. **Script breakdown** → Identify scenes needing AI generation
2. **Prompt batch** → Write prompts for all shots in sequence
3. **Model assignment** → Match each shot to the best model
4. **Generate & review** → Run generations, select best takes
5. **Post-production** → Composite, color grade, add audio

## Prompt Engineering Tips

- **Be specific about camera**: "Medium close-up" beats "shot of person"
- **Describe motion arc**: "Hand rises from waist to above head" beats "hand moves up"
- **Anchor style references**: "Like a Wes Anderson film" or "documentary style"
- **Control pacing**: "In slow motion" or "at 2x speed" where supported
- **Layer atmosphere**: Lighting + weather + time of day = mood
- **Use model-specific syntax**: Some models support structured parameters (seed, CFG, frames)

## References

- Source repository: [cclank/lanshu-awesome-ai-video-kit](https://github.com/cclank/lanshu-awesome-ai-video-kit) — 411 prompts, 15 models, 7 Claude Skills, 14 methodology articles
- Topics: ai-video, prompt-engineering, video-generation, claude-skills
