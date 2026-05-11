# How to Use: Content Engine - Social Media

## Installation

```bash
# Clone this prototype
cd content_engine_social_media/

# (Optional) Install API dependencies for live mode
pip install -r requirements.txt
```

Mock mode requires only Python 3.10+ with no extra packages.

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install:

1. Copy the skill directory into your Claude skills folder:

```bash
mkdir -p ~/.claude/skills/content_engine_social_media
cp SKILL.md ~/.claude/skills/content_engine_social_media/SKILL.md
```

2. Set API keys (optional, for live generation):

```bash
export FAL_KEY="your-fal-ai-key"        # AI image generation
export GROQ_API_KEY="your-groq-key"     # Fast LLM content generation
```

3. **Trigger phrases** that activate the skill:
   - "Create social media content about [topic]"
   - "Generate posts for all channels"
   - "Content engine"
   - "Social media campaign"
   - "Auto-publish content"

## Running Standalone (without Claude)

```bash
# Default demo topic
python3 content_engine.py

# Custom topic
python3 content_engine.py "Your Product Launch Announcement"

# Full demo with file output
bash run.sh
```

## First 60 Seconds

**Input:**

```bash
python3 content_engine.py "AI-Powered Analytics Dashboard"
```

**Output:**

```
============================================================
  Content Engine - Social Media Pipeline
============================================================

  Topic: AI-Powered Analytics Dashboard
  Date:  2026-05-11 08:30:00

[1/3] Generating content for 5 channels (mock mode)...

  --- Twitter / X (167/280 chars) ---
  🚀 AI-Powered Analytics Dashboard is changing the game...

  --- LinkedIn (598/1300 chars) ---
  I've been diving deep into AI-Powered Analytics Dashboard...

  --- Instagram (412/2200 chars) ---
  🚀 AI-Powered Analytics Dashboard just hit different...

  --- Facebook (318/500 chars) ---
  Have you tried AI-Powered Analytics Dashboard yet?...

  --- Blog / Newsletter (742/3000 chars) ---
  # AI-Powered Analytics Dashboard: A Practical Guide...

[2/3] Generating image (mock SVG)...
  Image saved: output/generated_image.svg

[3/3] Publishing to channels (mock mode)...
  Twitter / X: published (mock)
  LinkedIn: published (mock)
  Instagram: published (mock)
  Facebook: published (mock)
  Blog / Newsletter: published (mock)

============================================================
  Pipeline complete!
  Output directory: output
  Manifest: output/manifest.json
  Posts: 5 files
  Image: output/generated_image.svg
============================================================
```

**What gets created in `output/`:**

| File | Description |
|---|---|
| `manifest.json` | Full pipeline output with metadata |
| `post_twitter.txt` | Twitter/X post copy |
| `post_linkedin.txt` | LinkedIn post copy |
| `post_instagram.txt` | Instagram caption |
| `post_facebook.txt` | Facebook post copy |
| `post_newsletter.txt` | Blog/newsletter snippet |
| `generated_image.svg` | Placeholder image (or `.png` with FAL_KEY) |

## Live Mode

Set both API keys and re-run to get real LLM-generated content and AI images:

```bash
export GROQ_API_KEY="gsk_..."
export FAL_KEY="fal_..."
python3 content_engine.py "Your topic here"
```

Content will be generated via Groq (llama-3.1-8b-instant) and images via fal-ai (nano-banana-2).
