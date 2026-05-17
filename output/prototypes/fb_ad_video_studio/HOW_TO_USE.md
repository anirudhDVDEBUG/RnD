# How to Use - FB Ad Video Studio

## Installation

```bash
# Clone or copy into your workspace
git clone https://github.com/ai-agents-for-agencies-coaches/fb-ad-video-studio.git
cd fb-ad-video-studio

# No external dependencies required for core functionality
pip install -r requirements.txt  # (empty - pure Python)
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/fb-ad-video-studio
cp SKILL.md ~/.claude/skills/fb-ad-video-studio/SKILL.md
```

### Trigger Phrases

Say any of these to Claude Code to activate the skill:

- "Create a Facebook video ad for my product"
- "Build a high-converting Instagram Reels ad"
- "Generate a TikTok video ad creative using HyperFrames"
- "Make a video ad with hook, problem, solution, CTA structure"
- "Reverse-engineer this ad style into a reusable template"

Claude will then ask for your product details and generate the full HyperFrames composition.

## First 60 Seconds

```bash
# 1. Run the demo
bash run.sh

# 2. Output appears immediately:
#    output/ad_composition.html   <- open in browser, see animated ad
#    output/audio_cues.json       <- voiceover + SFX timing
#    output/template.json         <- reusable structure for future ads
#    output/summary.json          <- metadata

# 3. Open the HTML file in any browser to see the animated ad preview
open output/ad_composition.html  # macOS
# or: xdg-open output/ad_composition.html  # Linux
```

### Sample Input (in code)

```python
from fb_ad_composer import AdBrief, compose_ad

brief = AdBrief(
    product_name="MyApp",
    tagline="Ship faster",
    target_audience="Developers, 25-40",
    platform="ig_reels",       # fb_feed | ig_reels | tiktok
    duration=30,               # seconds
    hook_text="Still deploying on Fridays?",
    problem_text="Broken deploys cost you weekends.",
    solution_text="MyApp catches failures before they ship.",
    proof_text='"Zero rollbacks in 3 months" - CTO, Acme',
    cta_text="Try free for 14 days. No card needed.",
    brand_color="#FF6B35",
    accent_color="#004E89",
)

summary = compose_ad(brief, output_dir="output")
```

### Sample Output

```
  FB Ad Video Studio - HyperFrames Composition Demo
============================================================

  Product:    FlowMetrics AI
  Platform:   Ig Reels
  Duration:   30s

  Ad Structure:
  +--------------------------------------------------+
  | Section    | Time     | Content                    |
  +--------------------------------------------------+
  | HOOK       | 0.0-3.0s | Your dashboard is lying .. |
  | PROBLEM    | 3.0-8.1s | Vanity metrics hide real.. |
  | SOLUTION   | 8.1-18.0s| FlowMetrics AI surfaces .. |
  | PROOF      | 18.0-24.0s| "Cut churn 34% in 6 wee.. |
  | CTA        | 24.0-30.0s| Start free. See your rea.. |
  +--------------------------------------------------+

  Generated Files:
    output/ad_composition.html
    output/audio_cues.json
    output/template.json
```

## Rendering to Video

The HTML composition can be rendered to MP4 using headless browser capture:

```bash
# Using Playwright (optional dependency)
pip install playwright && playwright install chromium

python3 -c "
# Screen-record the HTML animation to video
# (requires playwright - not included in base requirements)
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 1920})
    page.goto('file://$(pwd)/output/ad_composition.html')
    # Use page.video or screenshot sequence for MP4 export
"
```

## Multi-Platform Variants

Generate the same ad optimized for different platforms by changing `platform`:

| Platform | Aspect | Use case |
|----------|--------|----------|
| `fb_feed` | 4:5 (1080x1350) | Facebook Feed ads |
| `ig_reels` | 9:16 (1080x1920) | Instagram Reels |
| `tiktok` | 9:16 (1080x1920) | TikTok In-Feed |
