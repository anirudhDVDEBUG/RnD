#!/usr/bin/env python3
"""
AI Short Film Prompt Generator

Generates structured, model-optimized video generation prompts for AI short films.
Based on the methodology behind "Zombie Scavenger" by Mx-Shell.

Supports: Sora, Kling, Veo, Seedance, Jimeng
"""

import json
import textwrap
import argparse
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------

SUPPORTED_MODELS = ["sora", "kling", "veo", "seedance", "jimeng"]

MODEL_STYLE_HINTS = {
    "sora": "photorealistic, physically accurate, natural camera motion, cinematic depth of field",
    "kling": "dynamic motion, fluid character animation, action-driven cinematography",
    "veo": "cinematic composition, professional color grading, filmic grain, anamorphic bokeh",
    "seedance": "stylized movement, rhythmic flow, expressive motion dynamics",
    "jimeng": "high-detail character rendering, Asian aesthetic influence, vivid color palette",
}

SHOT_TYPES = [
    "Extreme wide shot",
    "Wide shot",
    "Medium wide shot",
    "Medium shot",
    "Medium close-up",
    "Close-up",
    "Extreme close-up",
    "Over-the-shoulder",
    "POV",
    "Low angle",
    "High angle",
    "Dutch angle",
]

CAMERA_MOVES = [
    "static",
    "slow pan left",
    "slow pan right",
    "tilt up",
    "tilt down",
    "slow push-in",
    "pull-back",
    "tracking shot",
    "dolly zoom",
    "crane up",
    "handheld shake",
    "orbit",
]


@dataclass
class Character:
    name: str
    description: str


@dataclass
class Shot:
    number: str
    shot_type: str
    camera_move: str
    prompt: str
    duration_sec: int = 8


@dataclass
class Scene:
    number: int
    title: str
    narrative_beat: str
    duration_sec: int
    shots: list = field(default_factory=list)


@dataclass
class ShortFilm:
    title: str
    genre: str
    tone: str
    setting: str
    target_model: str
    aspect_ratio: str
    visual_style: str
    color_palette: str
    characters: list = field(default_factory=list)
    scenes: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def build_prompt(shot_type: str, camera_move: str, subject: str,
                 environment: str, action: str, lighting: str,
                 atmosphere: str, model: str) -> str:
    """Assemble a generation-ready prompt following the template."""
    style = MODEL_STYLE_HINTS.get(model, MODEL_STYLE_HINTS["sora"])
    parts = [
        f"{shot_type}, {camera_move}.",
        f"{subject} in {environment}.",
        f"{action}.",
        f"{lighting}, {atmosphere}.",
        f"{style}, 4K.",
    ]
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Demo film: "Last Light" (post-apocalyptic sci-fi, 90 seconds)
# ---------------------------------------------------------------------------

def create_demo_film() -> ShortFilm:
    """Return a fully-specified demo short film with 4 scenes / 10 shots."""

    film = ShortFilm(
        title="Last Light",
        genre="Post-apocalyptic sci-fi",
        tone="Melancholic, tense, quietly hopeful",
        setting="Abandoned coastal city, 2087",
        target_model="veo",
        aspect_ratio="16:9",
        visual_style="Desaturated realism with occasional warm highlight accents",
        color_palette="Steel blues, concrete grays, amber sunset tones",
    )

    film.characters = [
        Character(
            name="Maren",
            description=(
                "Woman in her mid-30s, short dark hair with a streak of gray, "
                "weathered olive skin, wearing a patched navy utility jacket over "
                "a faded red henley, cargo pants, scuffed boots. Carries a dented "
                "aluminum canteen clipped to her belt."
            ),
        ),
        Character(
            name="The Beacon",
            description=(
                "A towering derelict lighthouse on a crumbling concrete pier, "
                "upper windows shattered, rust streaks down white-painted walls, "
                "a faint amber light flickering in the lantern room."
            ),
        ),
    ]

    # -- Scene 1: The Wasteland --
    s1 = Scene(1, "The Wasteland", "Establish the desolate world and introduce Maren.", 25)
    s1.shots = [
        Shot("1.1", "Extreme wide shot", "slow crane up",
             build_prompt(
                 "Extreme wide shot", "slow crane up",
                 "A lone figure walks along a cracked coastal highway",
                 "an abandoned city skyline half-submerged in rising seawater, rusted vehicles lining the road",
                 "The figure moves steadily forward, wind pulling at her jacket",
                 "Overcast late-afternoon light, sun barely visible through haze",
                 "desolate, vast, muted color palette", "veo"), 10),
        Shot("1.2", "Medium shot", "tracking shot",
             build_prompt(
                 "Medium shot", "tracking shot",
                 "Maren — woman mid-30s, short dark hair with gray streak, patched navy utility jacket, faded red henley",
                 "the broken highway, tide pools forming in potholes",
                 "She glances at a hand-drawn map, then looks toward the horizon with determination",
                 "Diffused overcast daylight, cool steel-blue tones",
                 "somber, resolute mood", "veo"), 8),
        Shot("1.3", "Close-up", "static",
             build_prompt(
                 "Close-up", "static",
                 "Maren's hands holding a creased paper map with a circled destination marked 'BEACON'",
                 "blurred background of wet asphalt and abandoned cars",
                 "Her thumb traces the route, a drop of rain lands on the paper",
                 "Soft diffused light, shallow depth of field",
                 "intimate, contemplative", "veo"), 7),
    ]

    # -- Scene 2: The Approach --
    s2 = Scene(2, "The Approach", "Maren spots the lighthouse; tension builds.", 20)
    s2.shots = [
        Shot("2.1", "Wide shot", "slow push-in",
             build_prompt(
                 "Wide shot", "slow push-in",
                 "A derelict lighthouse on a crumbling concrete pier jutting into gray churning sea",
                 "rocky shoreline littered with debris, stormy sky",
                 "Waves crash against the pier, sending spray into the air",
                 "Dramatic storm light, dark clouds with a sliver of golden sunset breaking through",
                 "foreboding, dramatic scale", "veo"), 8),
        Shot("2.2", "Over-the-shoulder", "static",
             build_prompt(
                 "Over-the-shoulder", "static",
                 "Maren seen from behind, silhouetted against the lighthouse",
                 "rocky beach foreground, turbulent ocean midground, lighthouse background",
                 "She pauses, adjusts her jacket, and takes a breath before stepping onto the pier",
                 "Backlit sunset rim light, lens flare",
                 "anticipation, isolation", "veo"), 7),
    ]

    # -- Scene 3: The Climb --
    s3 = Scene(3, "The Climb", "Maren enters the lighthouse and ascends the spiral stairs.", 25)
    s3.shots = [
        Shot("3.1", "Low angle", "tilt up",
             build_prompt(
                 "Low angle", "tilt up",
                 "Maren pushes open a heavy rusted metal door at the base of the lighthouse",
                 "interior of a cylindrical stone stairwell, debris on the floor, faded maritime murals on walls",
                 "The door groans open, dust particles float in a shaft of light from a crack above",
                 "Single beam of exterior light cutting through darkness, volumetric dust",
                 "claustrophobic, mysterious", "veo"), 8),
        Shot("3.2", "Extreme wide shot", "slow crane up",
             build_prompt(
                 "Extreme wide shot", "slow crane up through center of spiral staircase",
                 "Maren climbing a rusted iron spiral staircase inside the lighthouse",
                 "vertiginous spiral staircase viewed from below, peeling paint, exposed brick",
                 "She grips the railing and climbs steadily, her footsteps echoing",
                 "Dim ambient light, warm amber glow increasing from above",
                 "vertigo-inducing, atmospheric tension", "veo"), 10),
        Shot("3.3", "Medium close-up", "handheld shake",
             build_prompt(
                 "Medium close-up", "subtle handheld shake",
                 "Maren's face as she reaches the lantern room, amber light washing over her features",
                 "lantern room interior, old Fresnel lens visible behind her",
                 "Her expression shifts from exhaustion to wonder as she sees something off-screen",
                 "Warm amber lantern light mixed with cool exterior storm light",
                 "emotional turning point, awe", "veo"), 7),
    ]

    # -- Scene 4: Last Light --
    s4 = Scene(4, "Last Light", "Maren activates the beacon — hope in the wasteland.", 20)
    s4.shots = [
        Shot("4.1", "Close-up", "slow push-in",
             build_prompt(
                 "Close-up", "slow push-in",
                 "Maren's hand reaching for an old brass switch on a control panel",
                 "dusty control panel with analog dials and cracked glass gauges",
                 "Her fingers close around the switch and pull it down with a satisfying click",
                 "Warm practical light from a single overhead bulb flickering to life",
                 "decisive, pivotal moment", "veo"), 6),
        Shot("4.2", "Extreme wide shot", "pull-back",
             build_prompt(
                 "Extreme wide shot", "slow pull-back aerial",
                 "The lighthouse beacon ignites, casting a sweeping beam of amber light across the dark ocean",
                 "aerial view of the coastline at twilight, the ruined city behind, endless ocean ahead",
                 "The beam rotates steadily, illuminating sheets of rain and distant waves",
                 "Twilight blue hour, single warm amber beam cutting through storm",
                 "epic, hopeful, bittersweet beauty", "veo"), 10),
    ]

    film.scenes = [s1, s2, s3, s4]
    return film


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_markdown(film: ShortFilm) -> str:
    """Render the film as a structured Markdown prompt document."""
    lines = []
    lines.append(f"# {film.title} — AI Video Generation Prompts\n")

    lines.append("## Style Guide\n")
    lines.append(f"- **Visual style:** {film.visual_style}")
    lines.append(f"- **Color palette:** {film.color_palette}")
    lines.append(f"- **Genre / Tone:** {film.genre} — {film.tone}")
    lines.append(f"- **Setting:** {film.setting}")
    lines.append(f"- **Aspect ratio:** {film.aspect_ratio}")
    lines.append(f"- **Target model:** {film.target_model.capitalize()}")
    lines.append(f"- **Model style hints:** {MODEL_STYLE_HINTS[film.target_model]}")
    lines.append("")

    lines.append("## Character Reference\n")
    for c in film.characters:
        lines.append(f"### {c.name}")
        lines.append(f"{c.description}\n")

    total_shots = 0
    total_duration = 0
    for scene in film.scenes:
        lines.append(f"---\n\n## Scene {scene.number}: {scene.title}\n")
        lines.append(f"**Narrative beat:** {scene.narrative_beat}  ")
        lines.append(f"**Duration:** ~{scene.duration_sec}s\n")

        for shot in scene.shots:
            total_shots += 1
            total_duration += shot.duration_sec
            lines.append(f"### Shot {shot.number}")
            lines.append(f"- **Type:** {shot.shot_type}, {shot.camera_move}")
            lines.append(f"- **Duration:** ~{shot.duration_sec}s")
            lines.append(f"- **Prompt:**\n")
            wrapped = textwrap.fill(shot.prompt, width=80)
            lines.append(f"```\n{wrapped}\n```\n")

    lines.append("---\n")
    lines.append(f"**Total shots:** {total_shots}  ")
    lines.append(f"**Estimated runtime:** ~{total_duration}s  ")
    lines.append(f"**Target model:** {film.target_model.capitalize()}\n")
    return "\n".join(lines)


def format_json(film: ShortFilm) -> str:
    """Render the film as JSON for programmatic consumption."""
    data = {
        "title": film.title,
        "genre": film.genre,
        "tone": film.tone,
        "setting": film.setting,
        "target_model": film.target_model,
        "aspect_ratio": film.aspect_ratio,
        "visual_style": film.visual_style,
        "color_palette": film.color_palette,
        "model_style_hints": MODEL_STYLE_HINTS[film.target_model],
        "characters": [asdict(c) for c in film.characters],
        "scenes": [],
    }
    for scene in film.scenes:
        scene_data = {
            "number": scene.number,
            "title": scene.title,
            "narrative_beat": scene.narrative_beat,
            "duration_sec": scene.duration_sec,
            "shots": [asdict(s) for s in scene.shots],
        }
        data["scenes"].append(scene_data)
    return json.dumps(data, indent=2)


def format_prompts_only(film: ShortFilm) -> str:
    """Output just the raw prompts, one per line — ready to paste into a model."""
    lines = [f"# Raw prompts for: {film.title}  (model: {film.target_model})\n"]
    for scene in film.scenes:
        for shot in scene.shots:
            lines.append(f"[Shot {shot.number}]")
            lines.append(shot.prompt)
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Re-target a film to a different model
# ---------------------------------------------------------------------------

def retarget_film(film: ShortFilm, new_model: str) -> ShortFilm:
    """Swap style hints for a different target model."""
    film.target_model = new_model
    new_style = MODEL_STYLE_HINTS[new_model]
    old_styles = list(MODEL_STYLE_HINTS.values())

    for scene in film.scenes:
        for shot in scene.shots:
            # Replace the style suffix in each prompt
            for old_style in old_styles:
                if old_style in shot.prompt:
                    shot.prompt = shot.prompt.replace(old_style, new_style)
                    break
    return film


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="AI Short Film Prompt Generator — produce structured video-gen prompts"
    )
    parser.add_argument(
        "--format", choices=["markdown", "json", "prompts"], default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--model", choices=SUPPORTED_MODELS, default=None,
        help="Re-target prompts to a specific model (default: use film's model)"
    )
    parser.add_argument(
        "--scene", type=int, default=None,
        help="Output only the specified scene number"
    )
    parser.add_argument(
        "--list-models", action="store_true",
        help="List supported models and their style hints"
    )
    args = parser.parse_args()

    if args.list_models:
        print("Supported video generation models:\n")
        for model, hints in MODEL_STYLE_HINTS.items():
            print(f"  {model:12s}  {hints}")
        sys.exit(0)

    film = create_demo_film()

    if args.model:
        film = retarget_film(film, args.model)

    if args.scene:
        film.scenes = [s for s in film.scenes if s.number == args.scene]
        if not film.scenes:
            print(f"Error: Scene {args.scene} not found.", file=sys.stderr)
            sys.exit(1)

    formatters = {
        "markdown": format_markdown,
        "json": format_json,
        "prompts": format_prompts_only,
    }
    print(formatters[args.format](film))


if __name__ == "__main__":
    main()
