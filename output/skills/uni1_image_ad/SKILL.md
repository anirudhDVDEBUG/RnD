---
name: uni1_image_ad
description: |
  Generate Meta (Facebook/Instagram) image ads using Luma's uni-1 image generation model.
  Reverse-engineer existing ads into reusable prompt templates, then generate new ad creatives for any brand.
  TRIGGER: user wants to create image ads, generate ad creatives, reverse-engineer ad designs,
  make Meta/Facebook/Instagram ads, or use Luma uni-1 for marketing visuals.
---

# uni1-image-ad

Generate professional Meta image ads with Luma's uni-1 model. Reverse-engineer any existing ad into a reusable template, then plug it into any brand to produce scroll-stopping creatives.

## When to use

- "Generate a Meta image ad for my product"
- "Reverse-engineer this ad and create a template from it"
- "Create Facebook/Instagram ad creatives using AI"
- "Make an image ad in the style of [brand/reference]"
- "Generate ad variations for A/B testing"

## How to use

### Prerequisites

Set the following environment variable:

- `LUMALABS_API_KEY` — Your Luma Labs API key for uni-1 image generation

### Step 1: Reverse-Engineer an Existing Ad (Optional)

If you have a reference ad to replicate:

1. Provide the reference ad image (URL or local path)
2. Analyze the ad's composition: layout, color palette, typography style, focal elements, CTA placement
3. Extract a structured prompt template capturing the visual DNA:
   - Scene/background description
   - Product placement and scale
   - Text overlay style and positioning
   - Color grading and mood
   - Aspect ratio (1:1 for feed, 9:16 for stories, 1.91:1 for link ads)

### Step 2: Configure Brand Parameters

Define the brand context for generation:

```yaml
brand_name: "Your Brand"
product: "Product description"
color_palette: ["#hex1", "#hex2", "#hex3"]
tone: "modern/luxury/playful/minimal/bold"
cta_text: "Shop Now / Learn More / Get Started"
target_platform: "facebook_feed | instagram_feed | instagram_stories"
```

### Step 3: Generate the Ad Image

1. Construct the uni-1 prompt by combining the template with brand parameters
2. Call the Luma uni-1 API to generate the image:

```python
import requests

response = requests.post(
    "https://api.lumalabs.ai/dream-machine/v1/generations/image",
    headers={
        "Authorization": f"Bearer {LUMALABS_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "prompt": constructed_prompt,
        "aspect_ratio": "1:1",  # or "9:16", "16:9"
        "model": "uni1"
    }
)
```

3. Poll for completion and download the generated image
4. Save output to `./output/` directory with descriptive filename

### Step 4: Iterate and Create Variations

- Adjust prompt parameters for A/B test variants (different backgrounds, CTAs, product angles)
- Generate multiple aspect ratios for cross-platform deployment
- Create a batch of 3-5 variations per concept

### Output Structure

```
output/
  ad_[brand]_[variant]_[ratio].png
  prompt_log.json          # All prompts used for reproducibility
  template.yaml            # Reusable template extracted from reference
```

## Tips

- For best results, be specific about lighting, camera angle, and composition in prompts
- Use 1:1 for Facebook/Instagram feed, 9:16 for Stories/Reels, 1.91:1 for link ads
- Include negative constraints (e.g., "no text overlays" if adding text in post-production)
- Keep prompt templates modular so brand elements are easily swappable

## References

- Source: [krusemediallc/uni1-image-ad](https://github.com/krusemediallc/uni1-image-ad)
- [Luma Labs API Documentation](https://docs.lumalabs.ai/)
- [Meta Ad Specs](https://www.facebook.com/business/ads-guide)
