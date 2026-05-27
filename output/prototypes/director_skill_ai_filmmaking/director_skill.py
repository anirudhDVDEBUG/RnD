#!/usr/bin/env python3
"""
Director SKILL — AI Filmmaking Demo

Generates shot lists, keyframe prompts, and AI video generation prompts
styled through 10 iconic director lenses. Works standalone (no API keys).
"""

import json
import textwrap
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Director Style Database ──────────────────────────────────────────────────

DIRECTORS = {
    "spielberg": {
        "name": "Steven Spielberg",
        "lens": "28mm wide + 85mm close-up",
        "lighting": "golden-hour key light, warm fill, lens flares",
        "color_grade": "warm amber tones, rich skin tones, soft highlights",
        "composition": "emotional close-ups, low-angle awe shots, face-lit reveals",
        "movement": "smooth dolly-ins on reaction shots, sweeping crane reveals",
        "signature": "character-first framing, eyes reflecting wonder",
    },
    "kubrick": {
        "name": "Stanley Kubrick",
        "lens": "18mm ultra-wide",
        "lighting": "cold practical lighting, overhead fluorescents, single-source",
        "color_grade": "desaturated cool tones, clinical whites, deep shadows",
        "composition": "one-point perspective, symmetrical framing, centered subjects",
        "movement": "slow steadicam tracking, deliberate reverse zooms",
        "signature": "geometric perfection, unsettling symmetry, the Kubrick stare",
    },
    "wong_kar_wai": {
        "name": "Wong Kar-wai",
        "lens": "50mm prime, handheld",
        "lighting": "neon-soaked practicals, red/green/blue color wash",
        "color_grade": "saturated neons, crushed blacks, warm skin against cool bg",
        "composition": "tight frames, reflections in glass, obscured faces",
        "movement": "step-printed slow motion, handheld sway, whip pans",
        "signature": "yearning in motion blur, clocks and rain, stolen glances",
    },
    "nolan": {
        "name": "Christopher Nolan",
        "lens": "IMAX 65mm + 50mm anamorphic",
        "lighting": "natural light, overcast diffusion, practical sources",
        "color_grade": "cool steel blues, muted earth tones, high contrast",
        "composition": "IMAX-scale wide shots, cross-cut parallel action, POV inserts",
        "movement": "handheld urgency in action, locked-off for dialogue, rotating rigs",
        "signature": "time as visual motif, practical scale, layered sound design",
    },
    "villeneuve": {
        "name": "Denis Villeneuve",
        "lens": "40mm + 65mm large format",
        "lighting": "diffused overcast, silhouette backlight, fog diffusion",
        "color_grade": "desaturated ochre/teal, muted palette, crushed blacks",
        "composition": "vast negative space, slow-reveal wide shots, human dwarfed by scale",
        "movement": "imperceptible dolly creep, slow tilt reveals, static long takes",
        "signature": "silence as tension, scale vs. intimacy, environmental dread",
    },
    "wes_anderson": {
        "name": "Wes Anderson",
        "lens": "27mm + 40mm on tripod",
        "lighting": "flat even lighting, soft pastels, no harsh shadows",
        "color_grade": "pastel palette, candy tones, vintage Kodachrome feel",
        "composition": "dead-center framing, planimetric dollhouse compositions, 90° pans",
        "movement": "lateral tracking shots, whip pans between tableaux, snap zooms",
        "signature": "miniature precision, bilateral symmetry, storybook framing",
    },
    "tarkovsky": {
        "name": "Andrei Tarkovsky",
        "lens": "35mm prime, natural glass",
        "lighting": "natural window light, candles, overcast diffusion",
        "color_grade": "muted earth tones with vivid greens, sepia undertones",
        "composition": "long unbroken takes, natural elements in frame (water, fire, wind)",
        "movement": "imperceptible gliding dolly, meditative pacing, slow pan",
        "signature": "spiritual contemplation, nature reclaiming space, time made visible",
    },
    "lynch": {
        "name": "David Lynch",
        "lens": "50mm + macro inserts",
        "lighting": "uncanny practicals, red curtain glow, strobing flicker",
        "color_grade": "deep blacks, vivid reds, sickly greens, blown-out whites",
        "composition": "surreal juxtaposition, extreme close-ups of texture, off-center framing",
        "movement": "slow creeping dolly, static lingering shots, abrupt cuts",
        "signature": "dreamlike discontinuity, industrial hum, the familiar made strange",
    },
    "park_chan_wook": {
        "name": "Park Chan-wook",
        "lens": "35mm + 85mm, precise blocking",
        "lighting": "bold chiaroscuro, colored gels, theatrical spots",
        "color_grade": "rich saturated palette, deep reds and golds, jade greens",
        "composition": "baroque layered framing, split diopter, overhead tableaux",
        "movement": "fluid tracking through architecture, rotating reveals, match cuts",
        "signature": "visceral choreography, visual irony, beauty in violence",
    },
    "ridley_scott": {
        "name": "Ridley Scott",
        "lens": "anamorphic 50mm, multiple cameras",
        "lighting": "backlit silhouettes, volumetric smoke/haze, shaft lighting",
        "color_grade": "desaturated with warm practicals, industrial amber, blue shadows",
        "composition": "layered depth with atmosphere, silhouettes in doorways, industrial detail",
        "movement": "slow push-ins through haze, handheld combat, crane establishing shots",
        "signature": "smoke and atmosphere, world-building through texture, lived-in futures",
    },
}

# ── Shot Types ───────────────────────────────────────────────────────────────

SHOT_TYPES = ["EWS", "WS", "MWS", "MS", "MCU", "CU", "ECU", "OTS", "POV", "Insert"]
SHOT_LABELS = {
    "EWS": "Extreme Wide Shot",
    "WS": "Wide Shot",
    "MWS": "Medium Wide Shot",
    "MS": "Medium Shot",
    "MCU": "Medium Close-Up",
    "CU": "Close-Up",
    "ECU": "Extreme Close-Up",
    "OTS": "Over-the-Shoulder",
    "POV": "Point of View",
    "Insert": "Insert / Detail",
}


# ── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class Shot:
    number: int
    shot_type: str
    description: str
    camera_movement: str
    duration_seconds: int
    director_note: str = ""


@dataclass
class KeyframePrompt:
    shot_number: int
    prompt: str


@dataclass
class VideoPrompt:
    shot_number: int
    platform: str
    prompt: str


@dataclass
class SceneBreakdown:
    scene_description: str
    director_style: str
    shots: list = field(default_factory=list)
    keyframe_prompts: list = field(default_factory=list)
    video_prompts: list = field(default_factory=list)


# ── Scene Analyzer ───────────────────────────────────────────────────────────

def analyze_scene(description: str) -> dict:
    """Extract scene elements from a text description (rule-based heuristic)."""
    desc_lower = description.lower()

    elements = {
        "setting": "interior" if any(w in desc_lower for w in ["inside", "interior", "room", "station", "house", "building"]) else "exterior",
        "time_of_day": "night" if any(w in desc_lower for w in ["night", "dark", "midnight", "evening"]) else "day",
        "mood": "tense" if any(w in desc_lower for w in ["danger", "chase", "fight", "tense", "fear"]) else
                "melancholy" if any(w in desc_lower for w in ["alone", "lonely", "rain", "loss", "abandon"]) else
                "wonder" if any(w in desc_lower for w in ["discover", "beautiful", "garden", "light", "awe"]) else "neutral",
        "has_character": any(w in desc_lower for w in ["person", "man", "woman", "character", "astronaut", "detective", "child", "figure"]),
        "has_nature": any(w in desc_lower for w in ["garden", "tree", "flower", "water", "rain", "forest", "ocean", "vine"]),
        "has_architecture": any(w in desc_lower for w in ["building", "station", "room", "corridor", "door", "wall", "ceiling", "window"]),
        "scale": "epic" if any(w in desc_lower for w in ["vast", "massive", "space", "mountain", "city", "ocean"]) else "intimate",
    }
    return elements


# ── Shot List Generator ──────────────────────────────────────────────────────

def generate_shot_list(scene_desc: str, director_key: str, elements: dict) -> list:
    """Generate a structured shot list based on scene and director style."""
    style = DIRECTORS.get(director_key, DIRECTORS["spielberg"])

    shots = []

    # Shot 1: Establishing
    if elements["scale"] == "epic":
        shots.append(Shot(
            number=1,
            shot_type="EWS",
            description=f"Establishing shot — vast environment surrounding the scene. {style['signature'].split(',')[0].capitalize()}.",
            camera_movement=style["movement"].split(",")[0].strip(),
            duration_seconds=8,
            director_note=f"Lens: {style['lens'].split(',')[0]}. {style['lighting'].split(',')[0].capitalize()}.",
        ))
    else:
        shots.append(Shot(
            number=1,
            shot_type="WS",
            description=f"Establishing wide of the space — setting context and atmosphere.",
            camera_movement=style["movement"].split(",")[0].strip(),
            duration_seconds=6,
            director_note=f"Lens: {style['lens'].split(',')[0]}. {style['lighting'].split(',')[0].capitalize()}.",
        ))

    # Shot 2: Approach / Transition
    shots.append(Shot(
        number=2,
        shot_type="MS" if elements["has_character"] else "MWS",
        description="Subject enters or is revealed within the environment — transitional moment building anticipation.",
        camera_movement=style["movement"].split(",")[1].strip() if "," in style["movement"] else "static hold",
        duration_seconds=5,
        director_note=f"Color: {style['color_grade'].split(',')[0]}. Composition: {style['composition'].split(',')[0]}.",
    ))

    # Shot 3: Key detail / reaction
    shots.append(Shot(
        number=3,
        shot_type="CU" if elements["has_character"] else "Insert",
        description="Key detail or character reaction — the emotional pivot point of the scene.",
        camera_movement="static hold with shallow depth of field",
        duration_seconds=4,
        director_note=f"{style['signature'].split(',')[0].capitalize()}. {style['composition'].split(',')[1].strip().capitalize() if ',' in style['composition'] else ''}.",
    ))

    # Shot 4: The reveal / climax
    shots.append(Shot(
        number=4,
        shot_type="WS",
        description="The reveal — full scope of the scene's central visual becomes clear.",
        camera_movement=style["movement"].split(",")[0].strip(),
        duration_seconds=10,
        director_note=f"Full {style['name']} treatment: {style['lighting']}. {style['color_grade'].split(',')[0]}.",
    ))

    # Shot 5: Contemplation / aftermath
    if elements["mood"] in ("wonder", "melancholy"):
        shots.append(Shot(
            number=5,
            shot_type="MCU",
            description="Contemplative beat — subject absorbs the scene, lingering emotional resonance.",
            camera_movement="imperceptible slow push-in",
            duration_seconds=7,
            director_note=f"Hold the moment. {style['signature']}.",
        ))
    else:
        shots.append(Shot(
            number=5,
            shot_type="MWS",
            description="Final composition — subject and environment in visual harmony or tension.",
            camera_movement="slow pull-back to reveal full tableau",
            duration_seconds=6,
            director_note=f"{style['signature']}.",
        ))

    return shots


# ── Keyframe Prompt Generator ────────────────────────────────────────────────

def generate_keyframe_prompts(shots: list, scene_desc: str, director_key: str) -> list:
    """Build detailed image-gen prompts per shot, infused with director style."""
    style = DIRECTORS.get(director_key, DIRECTORS["spielberg"])
    prompts = []

    for shot in shots:
        shot_label = SHOT_LABELS.get(shot.shot_type, shot.shot_type)
        prompt_parts = [
            f"{shot_label} of scene:",
            shot.description.rstrip("."),
            f"— {style['name']}-inspired composition,",
            f"lens: {style['lens']},",
            f"lighting: {style['lighting']},",
            f"color: {style['color_grade']},",
            f"framing: {style['composition'].split(',')[0]},",
            "cinematic 2.39:1 aspect ratio, photorealistic, 8K detail, film grain.",
        ]
        prompts.append(KeyframePrompt(
            shot_number=shot.number,
            prompt=" ".join(prompt_parts),
        ))

    return prompts


# ── Video Prompt Generator ───────────────────────────────────────────────────

PLATFORM_TEMPLATES = {
    "runway": "Camera: {movement}. Scene: {description}. Style: {style_note}. Duration: {duration}s. Cinematic 24fps, smooth continuous motion, {color_grade}.",
    "kling": "{description}. {movement}. {style_note}. {color_grade}. Film quality, {duration} seconds.",
    "veo": "Generate a {duration}-second cinematic clip: {description}. Camera does {movement}. Visual style: {style_note}. Color palette: {color_grade}. Professional film look.",
}


def generate_video_prompts(shots: list, director_key: str, platform: str = "runway") -> list:
    """Generate platform-specific video prompts."""
    style = DIRECTORS.get(director_key, DIRECTORS["spielberg"])
    template = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES["runway"])
    prompts = []

    for shot in shots:
        prompt = template.format(
            movement=shot.camera_movement,
            description=shot.description.rstrip("."),
            style_note=f"{style['name']} style — {style['signature']}",
            duration=shot.duration_seconds,
            color_grade=style["color_grade"],
        )
        prompts.append(VideoPrompt(
            shot_number=shot.number,
            platform=platform,
            prompt=prompt,
        ))

    return prompts


# ── Main Pipeline ────────────────────────────────────────────────────────────

def process_scene(scene_description: str, director: str = "tarkovsky", platform: str = "runway") -> SceneBreakdown:
    """Full pipeline: scene description → shot list + keyframe + video prompts."""
    director_key = director.lower().replace(" ", "_").replace("-", "_")
    if director_key not in DIRECTORS:
        # Fuzzy match
        for key in DIRECTORS:
            if director_key in key or key in director_key:
                director_key = key
                break
        else:
            director_key = "spielberg"

    elements = analyze_scene(scene_description)
    shots = generate_shot_list(scene_description, director_key, elements)
    keyframes = generate_keyframe_prompts(shots, scene_description, director_key)
    video_prompts = generate_video_prompts(shots, director_key, platform)

    return SceneBreakdown(
        scene_description=scene_description,
        director_style=DIRECTORS[director_key]["name"],
        shots=shots,
        keyframe_prompts=keyframes,
        video_prompts=video_prompts,
    )


# ── Pretty Printer ───────────────────────────────────────────────────────────

def print_breakdown(breakdown: SceneBreakdown):
    """Print a formatted scene breakdown to stdout."""
    bar = "=" * 72

    print(f"\n{bar}")
    print(f"  DIRECTOR SKILL — AI FILMMAKING")
    print(f"  Style: {breakdown.director_style}")
    print(f"{bar}\n")

    print(f"  SCENE: {breakdown.scene_description}\n")

    # Shot List
    print(f"{'─' * 72}")
    print(f"  SHOT LIST")
    print(f"{'─' * 72}")
    for shot in breakdown.shots:
        label = SHOT_LABELS.get(shot.shot_type, shot.shot_type)
        print(f"\n  [{shot.number}] {shot.shot_type} — {label}  ({shot.duration_seconds}s)")
        print(f"      {shot.description}")
        print(f"      Camera: {shot.camera_movement}")
        if shot.director_note:
            print(f"      Note:   {shot.director_note}")

    # Keyframe Prompts
    print(f"\n{'─' * 72}")
    print(f"  KEYFRAME PROMPTS (image generation)")
    print(f"{'─' * 72}")
    for kf in breakdown.keyframe_prompts:
        wrapped = textwrap.fill(kf.prompt, width=68, initial_indent="      ", subsequent_indent="      ")
        print(f"\n  [Shot {kf.shot_number}]")
        print(wrapped)

    # Video Prompts
    print(f"\n{'─' * 72}")
    print(f"  VIDEO PROMPTS ({breakdown.video_prompts[0].platform.upper()})")
    print(f"{'─' * 72}")
    for vp in breakdown.video_prompts:
        wrapped = textwrap.fill(vp.prompt, width=68, initial_indent="      ", subsequent_indent="      ")
        print(f"\n  [Shot {vp.shot_number}]")
        print(wrapped)

    print(f"\n{bar}")
    print(f"  Total shots: {len(breakdown.shots)}  |  "
          f"Total duration: {sum(s.duration_seconds for s in breakdown.shots)}s")
    print(f"{bar}\n")


# ── JSON Export ──────────────────────────────────────────────────────────────

def export_json(breakdown: SceneBreakdown) -> str:
    """Export breakdown as JSON for downstream tools."""
    data = {
        "scene": breakdown.scene_description,
        "director": breakdown.director_style,
        "shots": [asdict(s) for s in breakdown.shots],
        "keyframe_prompts": [asdict(k) for k in breakdown.keyframe_prompts],
        "video_prompts": [asdict(v) for v in breakdown.video_prompts],
    }
    return json.dumps(data, indent=2)


# ── CLI Entry Point ──────────────────────────────────────────────────────────

DEMO_SCENES = [
    {
        "scene": "A lone astronaut discovers a garden growing inside an abandoned space station.",
        "director": "tarkovsky",
        "platform": "runway",
    },
    {
        "scene": "A detective walks through a rain-soaked neon alley at midnight, searching for a missing person.",
        "director": "wong_kar_wai",
        "platform": "kling",
    },
    {
        "scene": "A child opens a mysterious door at the end of a long symmetrical hallway in a grand hotel.",
        "director": "kubrick",
        "platform": "veo",
    },
]


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        json_mode = True
    else:
        json_mode = False

    if len(sys.argv) > 2:
        # Custom scene: python director_skill.py "scene" "director" ["platform"]
        scene = sys.argv[1] if not json_mode else sys.argv[2]
        director = sys.argv[2] if not json_mode else (sys.argv[3] if len(sys.argv) > 3 else "spielberg")
        platform = sys.argv[3] if (not json_mode and len(sys.argv) > 3) else "runway"
        demos = [{"scene": scene, "director": director, "platform": platform}]
    else:
        demos = DEMO_SCENES

    for i, demo in enumerate(demos):
        breakdown = process_scene(demo["scene"], demo["director"], demo["platform"])
        if json_mode:
            print(export_json(breakdown))
        else:
            print_breakdown(breakdown)

        if i < len(demos) - 1:
            print("\n" + "▓" * 72 + "\n")


if __name__ == "__main__":
    main()
