# How to Use — AI Video Skill

## Install

```bash
git clone https://github.com/0xadvait/ai-video-skill.git
cd ai-video-skill
pip install -r requirements.txt
```

No heavy dependencies for the demo — it runs on stdlib alone. Real API calls need `requests` and provider-specific SDKs (see `requirements.txt` comments).

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install it:

1. Copy the skill folder into your skills directory:

```bash
mkdir -p ~/.claude/skills/ai-video-skill
cp SKILL.md ~/.claude/skills/ai-video-skill/SKILL.md
```

2. Set API keys for the model providers you want to use:

```bash
export SEEDANCE_API_KEY="sk-..."
export KLING_API_KEY="sk-..."
export WAN_API_KEY="sk-..."
export VEO_API_KEY="sk-..."
export OMNIHUMAN_API_KEY="sk-..."
```

You only need keys for the models you plan to use — the skill auto-selects based on your prompt.

3. **Trigger phrases** that activate the skill in Claude Code:

- "generate a video"
- "text to video"
- "image to video"
- "create video from prompt"
- "video generation with AI"

## First 60 Seconds

### Mock demo (no keys needed)

```bash
bash run.sh
```

**What you'll see:**

```
=== Single Prompt Demo ===
Prompt:    A dancer spinning under neon lights in slow motion
Mode:      text-to-video
Model:     Seedance 2.0 (auto-selected)
Threshold: 0.7
Max iters: 3

--- Quality Loop Results ---
  Iteration 1: motion=0.72  adherence=0.81  fidelity=0.65  overall=0.738  [PASS]

Final video: output/seedance_1716200000.mp4
Resolution:  1280x720
Duration:    7.2s
Accepted:    Yes
Iterations:  1
```

### Custom prompt

```bash
python3 video_skill.py --prompt "A cat playing piano" --model kling
```

### Multi-model sweep

```bash
python3 video_skill.py --all-models
```

Runs 4 prompts across Seedance, Veo, Wan, and Kling to compare model selection and quality scores.

### Inside Claude Code

Once the skill is installed, just type naturally:

> "Generate a video of a golden retriever running through autumn leaves"

Claude will auto-select Kling (general-purpose), generate the video, run the quality loop, and return the file path.

> "Create an image-to-video clip of this portrait using OmniHuman"

Claude will use OmniHuman to animate a still photo into a talking-head video.
