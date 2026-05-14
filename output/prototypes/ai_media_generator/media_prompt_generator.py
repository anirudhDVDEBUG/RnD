#!/usr/bin/env python3
"""
AI Media Prompt Generator — demonstrates the prompt-crafting engine
behind the ai_media_generator Claude Code skill.

Generates senior-director-level prompts optimized for 14+ generative AI
platforms (Midjourney, Sora, Kling, Suno, etc.) without requiring any
API keys or external services.
"""

import json
import random
import textwrap
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Platform definitions
# ---------------------------------------------------------------------------

PLATFORMS = {
    # Image platforms
    "midjourney": {
        "category": "image",
        "strengths": ["photorealism", "artistic styles", "cinematic lighting"],
        "syntax_notes": "Use --ar for aspect ratio, --v for version, --s for stylize, --q for quality",
        "default_params": {"version": "6.1", "stylize": 750, "quality": 1},
        "supports_negative": True,
        "negative_flag": "--no",
    },
    "flux": {
        "category": "image",
        "strengths": ["text rendering", "prompt adherence", "photorealism"],
        "syntax_notes": "Natural language prompts work best. Specify resolution explicitly.",
        "default_params": {"model": "flux-1.1-pro", "steps": 28},
        "supports_negative": False,
    },
    "dall-e": {
        "category": "image",
        "strengths": ["creative interpretation", "safety", "text-in-image"],
        "syntax_notes": "Natural language. Specify style (vivid/natural) and size.",
        "default_params": {"model": "dall-e-3", "style": "vivid", "size": "1792x1024"},
        "supports_negative": False,
    },
    "stable-diffusion": {
        "category": "image",
        "strengths": ["fine-tuning", "LoRA support", "controlnet"],
        "syntax_notes": "Comma-separated tags. Use (parentheses) for emphasis. Negative prompt in separate field.",
        "default_params": {"model": "SDXL", "sampler": "DPM++ 2M Karras", "steps": 30, "cfg_scale": 7},
        "supports_negative": True,
        "negative_flag": "negative_prompt",
    },
    "ideogram": {
        "category": "image",
        "strengths": ["typography", "text rendering", "graphic design"],
        "syntax_notes": "Natural language with style presets. Excellent for text-heavy images.",
        "default_params": {"model": "ideogram-v2", "style": "auto"},
        "supports_negative": True,
        "negative_flag": "negative_prompt",
    },
    # Video platforms
    "sora": {
        "category": "video",
        "strengths": ["physics simulation", "long coherent clips", "cinematic quality"],
        "syntax_notes": "Detailed scene descriptions. Specify camera movement, duration, aspect ratio.",
        "default_params": {"duration": "10s", "resolution": "1080p", "aspect_ratio": "16:9"},
        "supports_negative": False,
    },
    "kling": {
        "category": "video",
        "strengths": ["character consistency", "motion quality", "Asian aesthetics"],
        "syntax_notes": "Scene-based prompts. Specify motion type and camera movement explicitly.",
        "default_params": {"mode": "professional", "duration": "5s", "resolution": "1080p"},
        "supports_negative": True,
        "negative_flag": "negative_prompt",
    },
    "veo": {
        "category": "video",
        "strengths": ["cinematic realism", "long-form", "Google ecosystem"],
        "syntax_notes": "Cinematic descriptions with camera direction. Supports 4K output.",
        "default_params": {"duration": "8s", "resolution": "4K", "fps": 24},
        "supports_negative": False,
    },
    "seedance": {
        "category": "video",
        "strengths": ["dance/motion", "character animation", "music sync"],
        "syntax_notes": "Character-focused with motion descriptions. Can sync to audio.",
        "default_params": {"duration": "6s", "resolution": "1080p"},
        "supports_negative": False,
    },
    "runway": {
        "category": "video",
        "strengths": ["gen-3 motion", "image-to-video", "style transfer"],
        "syntax_notes": "Concise scene + motion descriptions. Works well with reference images.",
        "default_params": {"model": "gen-3-alpha", "duration": "4s"},
        "supports_negative": False,
    },
    "pika": {
        "category": "video",
        "strengths": ["quick iterations", "3D effects", "lip sync"],
        "syntax_notes": "Short, focused prompts. Use motion controls for specific movements.",
        "default_params": {"duration": "3s", "fps": 24},
        "supports_negative": True,
        "negative_flag": "negative_prompt",
    },
    # Music platforms
    "suno": {
        "category": "music",
        "strengths": ["full songs", "vocals", "genre variety"],
        "syntax_notes": "Specify genre, mood, tempo, instruments. Lyrics in [Verse]/[Chorus] format.",
        "default_params": {"model": "v4", "duration": "120s"},
        "supports_negative": False,
    },
    "udio": {
        "category": "music",
        "strengths": ["audio quality", "genre accuracy", "instrumental"],
        "syntax_notes": "Genre tags + mood descriptors. Supports instrumental-only mode.",
        "default_params": {"model": "v1.5", "duration": "90s"},
        "supports_negative": False,
    },
}

# ---------------------------------------------------------------------------
# Cinematic vocabulary banks
# ---------------------------------------------------------------------------

SHOT_TYPES = [
    "extreme wide shot", "wide shot", "medium shot", "medium close-up",
    "close-up", "extreme close-up", "over-the-shoulder", "bird's eye view",
    "low angle", "Dutch angle", "tracking shot", "dolly zoom",
]

LENSES = [
    "24mm wide-angle", "35mm", "50mm", "85mm portrait", "135mm telephoto",
    "anamorphic", "tilt-shift", "macro 100mm",
]

LIGHTING = [
    "golden hour sunlight", "blue hour ambient", "Rembrandt lighting",
    "butterfly lighting", "split lighting", "rim lighting",
    "neon-lit", "overcast diffused", "chiaroscuro", "volumetric fog",
    "practical lighting", "high-key studio",
]

COLOR_GRADES = [
    "teal and orange", "desaturated noir", "warm vintage film",
    "cool cyberpunk", "pastel soft", "high contrast editorial",
    "Kodak Portra 400", "Fujifilm Velvia", "bleach bypass",
]

CAMERA_MOVES = [
    "slow dolly forward", "orbiting 360", "crane up reveal",
    "handheld intimate", "steadicam follow", "whip pan",
    "pull-back reveal", "push-in dramatic", "aerial descent",
]

MUSIC_GENRES = [
    "cinematic orchestral", "lo-fi hip hop", "synthwave",
    "acoustic folk", "dark ambient", "future bass",
    "jazz fusion", "indie rock", "classical piano",
]

MUSIC_MOODS = [
    "euphoric", "melancholic", "intense", "dreamy",
    "nostalgic", "triumphant", "mysterious", "serene",
]


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

@dataclass
class MediaPrompt:
    platform: str
    category: str
    prompt: str
    negative_prompt: Optional[str] = None
    parameters: dict = field(default_factory=dict)
    craft_notes: list = field(default_factory=list)


def build_image_prompt(platform: str, scene: dict) -> MediaPrompt:
    """Build a platform-optimized image prompt from a scene description."""
    plat = PLATFORMS[platform]
    shot = random.choice(SHOT_TYPES)
    lens = random.choice(LENSES)
    light = random.choice(LIGHTING)
    grade = random.choice(COLOR_GRADES)

    subject = scene.get("subject", "a lone figure standing at the edge of a cliff")
    environment = scene.get("environment", "overlooking a vast misty valley at dawn")
    mood = scene.get("mood", "contemplative and awe-inspiring")
    style = scene.get("style", "cinematic photorealism")

    # Layer the prompt cinematically
    layers = [
        f"{shot} of {subject}",
        environment,
        f"{light}, {grade} color grading",
        f"shot on {lens} lens",
        f"{mood} atmosphere",
        f"style: {style}",
    ]

    if platform == "midjourney":
        prompt_text = ", ".join(layers)
        params = plat["default_params"].copy()
        params["aspect_ratio"] = scene.get("aspect_ratio", "16:9")
        suffix = f" --ar {params['aspect_ratio']} --v {params['version']} --s {params['stylize']} --q {params['quality']}"
        prompt_text += suffix
    elif platform == "stable-diffusion":
        prompt_text = ", ".join(layers) + f", masterpiece, best quality, {style}"
    else:
        prompt_text = ". ".join(layers) + "."

    negative = None
    if plat["supports_negative"]:
        negative = "blurry, deformed, low quality, watermark, text, logo, oversaturated, cropped, bad anatomy, ugly, duplicate"

    notes = [
        f"Selected {shot} for dramatic composition",
        f"Paired {light} with {grade} for visual depth",
        f"Tailored syntax for {platform} ({plat['syntax_notes'][:60]}...)",
    ]

    return MediaPrompt(
        platform=platform,
        category="image",
        prompt=prompt_text,
        negative_prompt=negative,
        parameters=plat["default_params"].copy(),
        craft_notes=notes,
    )


def build_video_prompt(platform: str, scene: dict) -> MediaPrompt:
    """Build a platform-optimized video prompt from a scene description."""
    plat = PLATFORMS[platform]
    shot = random.choice(SHOT_TYPES)
    lens = random.choice(LENSES)
    light = random.choice(LIGHTING)
    grade = random.choice(COLOR_GRADES)
    move = random.choice(CAMERA_MOVES)

    subject = scene.get("subject", "a dancer performing in an abandoned warehouse")
    action = scene.get("action", "spinning gracefully through shafts of dusty light")
    environment = scene.get("environment", "industrial space with broken windows")
    mood = scene.get("mood", "ethereal and haunting")

    layers = [
        f"{shot}, {move}.",
        f"{subject} {action}.",
        f"Environment: {environment}.",
        f"Lighting: {light}, {grade} color grading.",
        f"Camera: {lens} lens.",
        f"Mood: {mood}.",
    ]

    prompt_text = " ".join(layers)

    negative = None
    if plat["supports_negative"]:
        negative = "jittery, flickering, morphing faces, static, watermark, blurry, low resolution"

    notes = [
        f"Camera: {move} creates cinematic motion",
        f"Specified {lens} for depth-of-field control",
        f"Duration set to {plat['default_params'].get('duration', 'default')} for {platform}",
    ]

    return MediaPrompt(
        platform=platform,
        category="video",
        prompt=prompt_text,
        negative_prompt=negative,
        parameters=plat["default_params"].copy(),
        craft_notes=notes,
    )


def build_music_prompt(platform: str, scene: dict) -> MediaPrompt:
    """Build a platform-optimized music prompt from a scene description."""
    plat = PLATFORMS[platform]
    genre = scene.get("genre", random.choice(MUSIC_GENRES))
    mood = scene.get("mood", random.choice(MUSIC_MOODS))
    tempo = scene.get("tempo", "moderate")
    instruments = scene.get("instruments", "piano, strings, subtle percussion")

    prompt_text = (
        f"{genre}, {mood} mood, {tempo} tempo. "
        f"Instruments: {instruments}. "
        f"Build from a soft intro to an emotional crescendo, "
        f"then resolve to a gentle outro."
    )

    if platform == "suno" and scene.get("lyrics"):
        prompt_text += f"\n\n[Verse 1]\n{scene['lyrics']}"

    notes = [
        f"Genre '{genre}' selected for tonal match",
        f"Mood '{mood}' drives arrangement choices",
        f"Structure: intro -> build -> crescendo -> outro",
    ]

    return MediaPrompt(
        platform=platform,
        category="music",
        prompt=prompt_text,
        parameters=plat["default_params"].copy(),
        craft_notes=notes,
    )


def generate_prompt(platform: str, scene: dict) -> MediaPrompt:
    """Route to the correct builder based on platform category."""
    if platform not in PLATFORMS:
        raise ValueError(f"Unknown platform: {platform}. Supported: {', '.join(PLATFORMS.keys())}")

    category = PLATFORMS[platform]["category"]
    builders = {"image": build_image_prompt, "video": build_video_prompt, "music": build_music_prompt}
    return builders[category](platform, scene)


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def format_prompt(mp: MediaPrompt) -> str:
    """Pretty-print a MediaPrompt."""
    lines = []
    divider = "=" * 70
    lines.append(divider)
    lines.append(f"  PLATFORM: {mp.platform.upper()}  |  CATEGORY: {mp.category.upper()}")
    lines.append(divider)
    lines.append("")
    lines.append("  PROMPT:")
    for wrapped in textwrap.wrap(mp.prompt, width=66):
        lines.append(f"    {wrapped}")
    if mp.negative_prompt:
        lines.append("")
        lines.append("  NEGATIVE PROMPT:")
        for wrapped in textwrap.wrap(mp.negative_prompt, width=66):
            lines.append(f"    {wrapped}")
    lines.append("")
    lines.append(f"  PARAMETERS: {json.dumps(mp.parameters, indent=2)}")
    lines.append("")
    lines.append("  CRAFT NOTES:")
    for note in mp.craft_notes:
        lines.append(f"    - {note}")
    lines.append(divider)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo scenarios
# ---------------------------------------------------------------------------

DEMO_SCENES = [
    {
        "name": "Product Hero Shot",
        "platform": "midjourney",
        "scene": {
            "subject": "a sleek titanium smartwatch floating above a reflective surface",
            "environment": "minimalist studio with gradient backdrop, soft caustic reflections",
            "mood": "premium, aspirational, clean",
            "style": "commercial product photography",
            "aspect_ratio": "1:1",
        },
    },
    {
        "name": "Brand Story Video",
        "platform": "sora",
        "scene": {
            "subject": "a young entrepreneur",
            "action": "walks through a bustling co-working space, pausing to sketch an idea on a whiteboard",
            "environment": "modern open-plan office with floor-to-ceiling windows, golden afternoon light",
            "mood": "ambitious and inspiring",
        },
    },
    {
        "name": "Social Media Ad",
        "platform": "kling",
        "scene": {
            "subject": "a hand reaching for a coffee cup",
            "action": "lifts the cup as steam curls upward in slow motion",
            "environment": "cozy cafe corner with bokeh background lights",
            "mood": "warm and inviting",
        },
    },
    {
        "name": "Brand Jingle",
        "platform": "suno",
        "scene": {
            "genre": "upbeat indie pop",
            "mood": "cheerful",
            "tempo": "120 BPM",
            "instruments": "ukulele, claps, tambourine, bass synth",
            "lyrics": "Rise and shine, the world is yours today\nEvery step you take lights up the way",
        },
    },
    {
        "name": "Cinematic Landscape",
        "platform": "flux",
        "scene": {
            "subject": "ancient ruins of a forgotten temple",
            "environment": "overgrown with bioluminescent vines, starlit sky with visible nebula",
            "mood": "mysterious and otherworldly",
            "style": "sci-fi concept art, matte painting quality",
        },
    },
    {
        "name": "Music Video Clip",
        "platform": "veo",
        "scene": {
            "subject": "a silhouette of a singer",
            "action": "standing on a rooftop, city lights reflecting on wet pavement, rain falling",
            "environment": "neon-lit urban rooftop at night",
            "mood": "melancholic and cinematic",
        },
    },
]


def run_demo(scenes=None):
    """Run the full demo, generating prompts for each scenario."""
    if scenes is None:
        scenes = DEMO_SCENES

    print()
    print("  AI MEDIA PROMPT GENERATOR")
    print("  Senior-director-level prompts for 14+ generative AI platforms")
    print("  " + "-" * 56)
    print()
    print(f"  Platforms loaded: {len(PLATFORMS)}")
    print(f"  Categories: image ({sum(1 for p in PLATFORMS.values() if p['category']=='image')}), "
          f"video ({sum(1 for p in PLATFORMS.values() if p['category']=='video')}), "
          f"music ({sum(1 for p in PLATFORMS.values() if p['category']=='music')})")
    print(f"  Demo scenarios: {len(scenes)}")
    print()

    for i, demo in enumerate(scenes, 1):
        print(f"  --- Scenario {i}/{len(scenes)}: {demo['name']} ---")
        print()
        mp = generate_prompt(demo["platform"], demo["scene"])
        print(format_prompt(mp))
        print()

    # Summary table
    print("=" * 70)
    print("  SUPPORTED PLATFORMS SUMMARY")
    print("=" * 70)
    print(f"  {'Platform':<20} {'Category':<10} {'Neg. Prompt':<12} {'Key Strengths'}")
    print(f"  {'-'*18:<20} {'-'*8:<10} {'-'*10:<12} {'-'*30}")
    for name, info in PLATFORMS.items():
        neg = "Yes" if info["supports_negative"] else "No"
        strengths = ", ".join(info["strengths"][:2])
        print(f"  {name:<20} {info['category']:<10} {neg:<12} {strengths}")
    print()
    print("  Done. All prompts generated without any API keys or external calls.")
    print()


if __name__ == "__main__":
    run_demo()
