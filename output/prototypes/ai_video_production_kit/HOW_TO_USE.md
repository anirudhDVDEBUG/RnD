# How to Use — AI Video Production Kit

## Option A: Install as a Claude Code Skill

### 1. Create the skill directory

```bash
mkdir -p ~/.claude/skills/ai-video-production-kit
cp SKILL.md ~/.claude/skills/ai-video-production-kit/SKILL.md
```

### 2. Trigger phrases

Once installed, Claude Code activates this skill when you say any of:

- "Help me write a prompt for Kling / Runway / Sora / Veo"
- "Which AI video model should I use?"
- "Generate an AI video prompt for a product demo"
- "Optimize my video generation prompt"
- "ai video", "video generation prompt", "video model selection"
- Model-specific: "kling prompt", "runway prompt", "sora prompt", "veo prompt", "seedance", "wan video", "cogvideox", "hunyuan video"

### 3. What Claude does with the skill

Claude will:
1. Ask you for the scene brief (subject, action, style, platform, budget)
2. Generate a 5-layer prompt: `[Camera] + [Subject] + [Action] + [Environment] + [Style]`
3. Recommend the top 3 models for your use case with scoring rationale
4. Provide negative prompts and parameter suggestions

## Option B: Run the Standalone Demo

### Install

```bash
git clone https://github.com/cclank/lanshu-awesome-ai-video-kit.git
cd lanshu-awesome-ai-video-kit

# This prototype needs only Python 3.10+ (no pip install needed)
```

Or just run this prototype directly:

```bash
cd ai_video_production_kit/
bash run.sh
```

### Dependencies

Python 3.10+ standard library only. No external packages required.

### Interactive Mode

```bash
python3 video_prompt_engine.py --interactive
```

You'll be prompted for:
- **Subject**: what's in the scene (e.g., "a woman holding a phone")
- **Action**: what happens (e.g., "smiling and tapping the screen")
- **Style**: cinematic, commercial, social_media, documentary, artistic, noir, anime, vintage
- **Use case**: creative, commercial, social_media, enterprise
- **Budget**: free, low, mid, high

## First 60 Seconds

```
$ bash run.sh

  AI VIDEO PRODUCTION KIT — Demo Run
  411+ prompts | 15 models | 5-layer prompt engine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SCENARIO 1: COMMERCIAL — a sleek wireless headphone
  Platform: youtube | Budget: high | Style: commercial | 6s @ 16:9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  GENERATED VIDEO PROMPT
  ================================================================
  Full prompt:
    Crane shot rising, a sleek wireless headphone rotating
    slowly on a marble pedestal, softly flowing, soft golden
    hour sunlight through floor-to-ceiling windows...

  MODEL SELECTION REPORT
  ================================================================
  1st — Veo 3  (score: 63.0)
    Strengths : photorealism, cinematic quality, physics accuracy
    Best for  : cinematic, product, enterprise
    ...

  2nd — Runway Gen-3 Alpha  (score: 58.0)
  3rd — Sora  (score: 43.0)
```

The demo runs 4 scenarios (commercial, social media, cinematic, enterprise) and prints a full model coverage summary table at the end.
