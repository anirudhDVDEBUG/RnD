#!/usr/bin/env python3
"""
demo.py — end-to-end demonstration of the Claude Design Agents Toolkit.

Runs all four agents and writes output to the `output/` directory.
No API keys required — everything is template-driven.
"""

import json
import os
import sys
from pathlib import Path

from design_agents import (
    ColorAgent,
    ComponentAgent,
    DesignToCodeAgent,
    LayoutAgent,
)

OUTPUT_DIR = Path(__file__).parent / "output"
SEPARATOR = "=" * 60


def section(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    app_name = "TrendForge"
    theme = "ocean"

    # ── 1. Layout Agent ─────────────────────────────────────────────────
    section("1. Layout Agent — available layouts")
    layout = LayoutAgent(app_name)
    for name in layout.available_layouts():
        print(f"  - {name}: {layout.describe(name)}")

    print(f"\nGenerating 'dashboard' layout for '{app_name}'...")
    dashboard_html = layout.generate("dashboard")
    print(f"  -> {len(dashboard_html)} chars of HTML + Tailwind generated")

    # ── 2. Color Agent ──────────────────────────────────────────────────
    section("2. Color Agent — theme palettes")
    colors = ColorAgent()
    print(f"Available themes: {', '.join(colors.available_themes())}")

    tokens = colors.generate_tokens(theme)
    print(f"\nGenerated '{theme}' design tokens:")
    for palette_name, shades in tokens.colors.items():
        sample = {k: v for k, v in list(shades.items())[:4]}
        print(f"  {palette_name}: {json.dumps(sample)} ... ({len(shades)} shades)")

    # Write CSS variables
    css_path = OUTPUT_DIR / "design-tokens.css"
    css_path.write_text(tokens.to_css_vars())
    print(f"\n  -> CSS variables written to {css_path}")

    # Write Tailwind config
    tw_path = OUTPUT_DIR / "tailwind.extend.json"
    tw_path.write_text(tokens.to_json())
    print(f"  -> Tailwind config written to {tw_path}")

    # ── 3. Component Agent ──────────────────────────────────────────────
    section("3. Component Agent — component library")
    components = ComponentAgent()
    print(f"Available components: {', '.join(components.available_components())}")

    specs = components.generate_all_specs()
    for spec in specs:
        print(f"\n  [{spec['name']}]")
        print(f"    {spec['description']}")
        print(f"    Props: {json.dumps(spec['props'])}")
        print(f"    Classes: {', '.join(spec['key_classes'])}")

    specs_path = OUTPUT_DIR / "component-specs.json"
    specs_path.write_text(json.dumps(specs, indent=2))
    print(f"\n  -> Full specs written to {specs_path}")

    # ── 4. Design-to-Code Agent ─────────────────────────────────────────
    section("4. Design-to-Code Agent — full page generation")
    d2c = DesignToCodeAgent(app_name, theme)

    for layout_type in ["dashboard", "landing", "form"]:
        result = d2c.generate_page(layout_type)
        html_path = OUTPUT_DIR / f"{layout_type}.html"
        html_path.write_text(result["html"])
        print(f"  {layout_type}.html — {len(result['html'])} chars (open in browser to preview)")

    # ── Summary ─────────────────────────────────────────────────────────
    section("Summary")
    output_files = sorted(OUTPUT_DIR.iterdir())
    print(f"Generated {len(output_files)} files in {OUTPUT_DIR}/:")
    for f in output_files:
        size = f.stat().st_size
        print(f"  {f.name:30s} {size:>6,} bytes")

    print(f"\nOpen output/dashboard.html in a browser to see the result.")
    print("All agents ran successfully — no API keys needed.\n")


if __name__ == "__main__":
    main()
