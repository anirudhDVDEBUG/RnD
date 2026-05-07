# How to Use uni1-image-ad

## Installation

```bash
git clone https://github.com/krusemediallc/uni1-image-ad.git
cd uni1-image-ad
pip install -r requirements.txt
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/uni1_image_ad
cp SKILL.md ~/.claude/skills/uni1_image_ad/SKILL.md
```

### Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Generate a Meta image ad for my product"
- "Reverse-engineer this ad and create a template"
- "Create Facebook/Instagram ad creatives using AI"
- "Make an image ad in the style of [brand]"
- "Generate ad variations for A/B testing"
- "Use Luma uni-1 for marketing visuals"

## Environment Variables

```bash
export LUMALABS_API_KEY="your-luma-labs-api-key"
```

Get a key at https://lumalabs.ai/dream-machine/api

## First 60 Seconds

```bash
# 1. Set your API key
export LUMALABS_API_KEY="luma-xxxxxxxxxxxx"

# 2. Generate an ad
python generate_ad.py \
  --brand "AcmeCoffee" \
  --product "Single-origin dark roast" \
  --tone "dark, moody, premium" \
  --cta "Shop Now" \
  --ratio "1:1" \
  --output ./output/

# 3. Check output
ls output/
# => ad_acmecoffee_hero_1x1.png
# => prompt_log.json
```

### Reverse-Engineer Mode

```bash
python reverse_engineer.py \
  --reference "https://example.com/competitor-ad.png" \
  --output-template ./output/template.yaml
```

This analyzes the reference image and produces a reusable YAML template you can plug into `generate_ad.py --template ./output/template.yaml`.

## Demo Mode (No API Key Required)

```bash
bash run.sh
```

Runs end-to-end with mock data, producing a sample prompt log and placeholder image to show the full pipeline.
