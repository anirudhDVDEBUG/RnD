"""Generate Meta image ads using Luma uni-1 model."""

import argparse
import json
import os
import sys
from pathlib import Path

from brand_config import BrandConfig
from luma_client import LumaClient


def build_prompt(config: BrandConfig, template: dict = None) -> str:
    """Construct a uni-1 prompt from brand config and optional template."""
    parts = []

    if template:
        parts.append(template.get("scene", ""))
        parts.append(template.get("composition", ""))
    else:
        parts.append(f"Professional advertising photo for {config.brand_name}.")
        parts.append(f"Product: {config.product}, centered in frame.")

    parts.append(f"Aesthetic: {config.tone}.")

    if config.color_palette:
        colors = ", ".join(config.color_palette)
        parts.append(f"Color palette emphasizing {colors}.")

    parts.append("High-end commercial photography, studio lighting, "
                 "sharp focus, advertising quality.")
    parts.append("No text overlays, no watermarks.")

    return " ".join(p for p in parts if p)


def generate(config: BrandConfig, template: dict = None,
             output_dir: str = "./output", mock: bool = False) -> dict:
    """Run the full generation pipeline."""
    os.makedirs(output_dir, exist_ok=True)

    prompt = build_prompt(config, template)
    slug = config.brand_name.lower().replace(" ", "")
    ratio_tag = config.aspect_ratio.replace(":", "x")
    filename = f"ad_{slug}_hero_{ratio_tag}.png"
    output_path = os.path.join(output_dir, filename)

    result = {
        "brand": config.brand_name,
        "prompt": prompt,
        "aspect_ratio": config.aspect_ratio,
        "output_file": output_path,
        "status": "pending",
    }

    if mock:
        # Demo mode: create a placeholder image
        from PIL import Image, ImageDraw
        size_map = {"1:1": (1024, 1024), "9:16": (576, 1024),
                    "16:9": (1024, 576), "1.91:1": (1024, 536)}
        size = size_map.get(config.aspect_ratio, (1024, 1024))
        img = Image.new("RGB", size, color=(30, 30, 40))
        draw = ImageDraw.Draw(img)
        draw.rectangle([40, 40, size[0]-40, size[1]-40], outline=(200, 160, 60), width=3)
        draw.text((size[0]//2 - 80, size[1]//2 - 20),
                  f"{config.brand_name}\nAD MOCK", fill=(200, 160, 60))
        img.save(output_path)
        result["status"] = "completed_mock"
        print(f"[MOCK] Generated: {output_path}")
    else:
        client = LumaClient()
        gen = client.generate_image(prompt, config.aspect_ratio)
        gen_id = gen.get("id")
        print(f"Generation submitted: {gen_id}")
        completed = client.poll_until_complete(gen_id)
        image_url = (completed.get("assets", {}).get("image")
                     or completed.get("image_url", ""))
        if image_url:
            client.download_image(image_url, output_path)
            result["status"] = "completed"
            print(f"Generated: {output_path}")
        else:
            result["status"] = "error_no_url"
            print("Error: no image URL in response", file=sys.stderr)

    # Save prompt log
    log_path = os.path.join(output_dir, "prompt_log.json")
    logs = []
    if os.path.exists(log_path):
        with open(log_path) as f:
            logs = json.load(f)
    logs.append(result)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate Meta image ads with Luma uni-1")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--product", required=True, help="Product description")
    parser.add_argument("--tone", default="modern, premium", help="Visual tone/mood")
    parser.add_argument("--cta", default="Shop Now", help="Call-to-action text")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio (1:1, 9:16, 16:9, 1.91:1)")
    parser.add_argument("--platform", default="instagram_feed", help="Target platform")
    parser.add_argument("--template", help="Path to template YAML")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--mock", action="store_true", help="Use mock mode (no API key needed)")
    args = parser.parse_args()

    config = BrandConfig.from_args(
        brand_name=args.brand,
        product=args.product,
        tone=args.tone,
        cta_text=args.cta,
        platform=args.platform,
    )

    template = None
    if args.template:
        import yaml
        with open(args.template) as f:
            template = yaml.safe_load(f)

    generate(config, template=template, output_dir=args.output, mock=args.mock)


if __name__ == "__main__":
    main()
