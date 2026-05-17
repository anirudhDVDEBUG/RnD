#!/usr/bin/env python3
"""
Demo: Generate a sample video ad composition using FB Ad Video Studio.
Produces an interactive HTML HyperFrames file + audio cues + reusable template.
"""

from fb_ad_composer import AdBrief, compose_ad, PLATFORM_SPECS
import json
import sys


def main():
    print("=" * 60)
    print("  FB Ad Video Studio - HyperFrames Composition Demo")
    print("=" * 60)
    print()

    # Sample ad brief for a SaaS product
    brief = AdBrief(
        product_name="FlowMetrics AI",
        tagline="Analytics that think for you",
        target_audience="SaaS founders & growth marketers, 25-45",
        platform="ig_reels",
        duration=30,
        hook_text="Your dashboard is lying to you.",
        problem_text="Vanity metrics hide real problems. You're flying blind.",
        solution_text="FlowMetrics AI surfaces the signals that actually predict churn & growth.",
        proof_text='"Cut churn 34% in 6 weeks" - Series A founder',
        cta_text="Start free. See your real metrics in 60 seconds.",
        brand_color="#6C5CE7",
        accent_color="#00B894",
    )

    print(f"  Product:    {brief.product_name}")
    print(f"  Platform:   {brief.platform.replace('_', ' ').title()}")
    print(f"  Duration:   {brief.duration}s")
    print(f"  Audience:   {brief.target_audience}")
    print()

    # Generate the composition
    summary = compose_ad(brief, output_dir="output")

    print("  Ad Structure:")
    print("  +" + "-" * 50 + "+")
    print(f"  | {'Section':<10} | {'Time':<8} | {'Content':<26} |")
    print("  +" + "-" * 50 + "+")

    time_offset = 0
    sections = [
        ("HOOK", brief.hook_text),
        ("PROBLEM", brief.problem_text),
        ("SOLUTION", brief.solution_text),
        ("PROOF", brief.proof_text),
        ("CTA", brief.cta_text),
    ]
    allocations = [0.10, 0.17, 0.33, 0.20, 0.20]
    for (section, text), alloc in zip(sections, allocations):
        dur = brief.duration * alloc
        time_str = f"{time_offset:.1f}-{time_offset+dur:.1f}s"
        display_text = text[:26] + ".." if len(text) > 26 else text
        print(f"  | {section:<10} | {time_str:<8} | {display_text:<26} |")
        time_offset += dur
    print("  +" + "-" * 50 + "+")
    print()

    # Show output files
    print("  Generated Files:")
    for f in summary["output_files"]:
        print(f"    {f}")
    print(f"    output/summary.json")
    print()

    # Load and display audio cues summary
    with open("output/audio_cues.json") as f:
        audio = json.load(f)
    print(f"  Audio Pipeline:")
    print(f"    Background: {audio['background_track']['style']} @ {audio['background_track']['bpm']} BPM")
    print(f"    Voiceover cues: {len(audio['voiceover'])}")
    print(f"    SFX triggers: {len(audio['sfx'])}")
    print()

    # Load template
    with open("output/template.json") as f:
        template = json.load(f)
    print(f"  Reverse-Template: {template['template_name']}")
    print(f"    Reusable structure with {len(template['structure'])} sections")
    print()

    # Platform specs
    spec = PLATFORM_SPECS[brief.platform]
    print(f"  Platform Specs ({brief.platform.replace('_',' ').title()}):")
    print(f"    Resolution: {spec['width']}x{spec['height']}")
    print(f"    Aspect:     {spec['aspect']}")
    print(f"    Max:        {spec['max_duration']}s")
    print()
    print("  Open output/ad_composition.html in a browser to preview the ad.")
    print("=" * 60)

    # Also generate a second variant for FB Feed to show multi-platform
    brief_fb = AdBrief(
        product_name="FlowMetrics AI",
        tagline="Analytics that think for you",
        target_audience="SaaS founders & growth marketers, 25-45",
        platform="fb_feed",
        duration=15,
        hook_text="Stop guessing. Start knowing.",
        problem_text="Most dashboards show you WHAT happened. Not WHY.",
        solution_text="FlowMetrics AI predicts churn before it happens.",
        proof_text="Trusted by 200+ SaaS teams",
        cta_text="Free trial - no card needed",
        brand_color="#6C5CE7",
        accent_color="#00B894",
    )
    compose_ad(brief_fb, output_dir="output/variant_fb_feed")
    print()
    print("  Bonus: FB Feed variant (15s, 4:5) -> output/variant_fb_feed/")
    print()


if __name__ == "__main__":
    main()
