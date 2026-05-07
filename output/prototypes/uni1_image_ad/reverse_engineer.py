"""Reverse-engineer an existing ad into a reusable prompt template."""

import argparse
import json
import os
import yaml


def analyze_ad_to_template(reference_path: str, mock: bool = False) -> dict:
    """Analyze a reference ad and extract a structured template.

    In production, this would use a vision model (Claude, GPT-4V) to
    analyze the image. In mock mode, returns a realistic sample template.
    """
    if mock:
        return {
            "name": "dark_hero_product",
            "description": "Dark moody product hero shot with warm accent lighting",
            "scene": "Dark studio background with dramatic side lighting, "
                     "warm golden rim light on product, subtle smoke/mist in background",
            "composition": "Product centered at 60% frame height, slight low angle, "
                           "shallow depth of field with bokeh background",
            "color_grading": "Dark shadows, desaturated midtones, warm highlights",
            "mood": "premium, mysterious, luxurious",
            "aspect_ratios": ["1:1", "4:5"],
            "notes": "Best for single-product hero shots. Add text overlays in post.",
        }

    # Production path would call a vision API here
    raise NotImplementedError(
        "Vision analysis requires a multimodal model. "
        "Use --mock for demo or integrate Claude vision API."
    )


def main():
    parser = argparse.ArgumentParser(description="Reverse-engineer ad into template")
    parser.add_argument("--reference", required=True, help="Reference ad image path/URL")
    parser.add_argument("--output-template", default="./output/template.yaml",
                        help="Output template path")
    parser.add_argument("--mock", action="store_true", help="Use mock analysis")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_template), exist_ok=True)

    print(f"Analyzing reference: {args.reference}")
    template = analyze_ad_to_template(args.reference, mock=args.mock)

    with open(args.output_template, "w") as f:
        yaml.dump(template, f, default_flow_style=False, sort_keys=False)

    print(f"Template saved: {args.output_template}")
    print(f"Template name: {template['name']}")
    print(f"Scene: {template['scene'][:80]}...")


if __name__ == "__main__":
    main()
