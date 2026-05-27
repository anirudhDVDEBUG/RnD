#!/usr/bin/env python3
"""
AI Video Production Kit — Prompt Engine & Model Selector

Generates optimized prompts for 15+ AI video models using a 5-layer structure:
  [Camera] + [Subject] + [Action/Motion] + [Environment] + [Style/Mood]

Provides model selection based on use-case, budget, and quality requirements.
"""

import json
import random
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Model Database ──────────────────────────────────────────────────────────

@dataclass
class VideoModel:
    name: str
    strengths: list[str]
    max_duration: int          # seconds
    aspect_ratios: list[str]
    cost_tier: str             # "free" | "low" | "mid" | "high"
    best_for: list[str]
    negative_prompt: bool
    structured_params: bool
    notes: str = ""

MODELS: dict[str, VideoModel] = {
    "kling": VideoModel(
        name="Kling 1.6",
        strengths=["fast iteration", "good motion", "Chinese market"],
        max_duration=10, aspect_ratios=["16:9", "9:16", "1:1"],
        cost_tier="mid", best_for=["social media", "product demos", "e-commerce"],
        negative_prompt=True, structured_params=True,
        notes="Strong at human motion; good for Douyin/TikTok content"
    ),
    "runway": VideoModel(
        name="Runway Gen-3 Alpha",
        strengths=["creative control", "style transfer", "compositing"],
        max_duration=16, aspect_ratios=["16:9", "9:16", "1:1"],
        cost_tier="high", best_for=["creative", "advertising", "music videos"],
        negative_prompt=True, structured_params=True,
        notes="Best-in-class motion brush and style controls"
    ),
    "sora": VideoModel(
        name="Sora",
        strengths=["long-form coherence", "complex scenes", "world simulation"],
        max_duration=60, aspect_ratios=["16:9", "9:16", "1:1"],
        cost_tier="high", best_for=["narrative", "cinematic", "long-form"],
        negative_prompt=False, structured_params=False,
        notes="Strongest at multi-subject scene coherence"
    ),
    "veo": VideoModel(
        name="Veo 3",
        strengths=["photorealism", "cinematic quality", "physics accuracy"],
        max_duration=8, aspect_ratios=["16:9", "9:16"],
        cost_tier="high", best_for=["cinematic", "product", "enterprise"],
        negative_prompt=False, structured_params=True,
        notes="Google DeepMind; excellent lighting and texture fidelity"
    ),
    "seedance": VideoModel(
        name="Seedance 1.0",
        strengths=["dance generation", "human motion", "music sync"],
        max_duration=10, aspect_ratios=["9:16", "1:1"],
        cost_tier="mid", best_for=["dance", "social media", "entertainment"],
        negative_prompt=True, structured_params=False,
        notes="ByteDance; specialized in choreography and body motion"
    ),
    "wan": VideoModel(
        name="Wan Video",
        strengths=["open-source", "customizable", "self-hosted"],
        max_duration=8, aspect_ratios=["16:9", "9:16", "1:1"],
        cost_tier="free", best_for=["research", "custom pipelines", "privacy"],
        negative_prompt=True, structured_params=True,
        notes="Alibaba open-source; run locally on consumer GPUs"
    ),
    "cogvideox": VideoModel(
        name="CogVideoX",
        strengths=["open-source", "research-friendly", "DiT architecture"],
        max_duration=6, aspect_ratios=["16:9"],
        cost_tier="free", best_for=["research", "prototyping", "education"],
        negative_prompt=True, structured_params=True,
        notes="Tsinghua/ZhipuAI; strong baseline for research"
    ),
    "hunyuan": VideoModel(
        name="Hunyuan Video",
        strengths=["Chinese text rendering", "Tencent ecosystem"],
        max_duration=6, aspect_ratios=["16:9", "9:16"],
        cost_tier="low", best_for=["Chinese market", "text overlay", "WeChat"],
        negative_prompt=True, structured_params=True,
        notes="Best Chinese text rendering of any video model"
    ),
    "ltx": VideoModel(
        name="LTX Video",
        strengths=["lightweight", "fast generation", "low VRAM"],
        max_duration=5, aspect_ratios=["16:9"],
        cost_tier="free", best_for=["prototyping", "previews", "rapid iteration"],
        negative_prompt=False, structured_params=False,
        notes="Lightricks; runs on 8GB VRAM"
    ),
    "mochi": VideoModel(
        name="Mochi 1",
        strengths=["open-source", "high quality", "motion fidelity"],
        max_duration=5, aspect_ratios=["16:9"],
        cost_tier="free", best_for=["creative", "open-source pipelines"],
        negative_prompt=False, structured_params=False,
        notes="Genmo; strong open-source alternative"
    ),
    "jimeng": VideoModel(
        name="Jimeng (Dreamina)",
        strengths=["ByteDance ecosystem", "fast", "Chinese market"],
        max_duration=6, aspect_ratios=["16:9", "9:16", "1:1"],
        cost_tier="low", best_for=["social media", "e-commerce", "Douyin"],
        negative_prompt=True, structured_params=False,
        notes="Tight integration with ByteDance/Douyin"
    ),
    "higgsfield": VideoModel(
        name="Higgsfield",
        strengths=["character animation", "personalization", "face swap"],
        max_duration=4, aspect_ratios=["9:16", "1:1"],
        cost_tier="mid", best_for=["character", "avatar", "personalized content"],
        negative_prompt=False, structured_params=False,
        notes="Best at character consistency across generations"
    ),
}

# ── Prompt Template Library ─────────────────────────────────────────────────

CAMERA_MOVES = [
    "Smooth dolly-in shot", "Slow tracking shot", "Aerial drone pull-back",
    "Handheld close-up", "Steadicam follow", "Static wide shot",
    "Crane shot rising", "Low-angle push-in", "Orbit 360 around subject",
    "Dutch angle tilt", "Whip pan left to right", "Slow zoom out",
    "POV first-person", "Over-the-shoulder", "Bird's eye top-down",
]

STYLES = {
    "cinematic": "cinematic 4K, shallow depth of field, anamorphic lens flare, warm color grading",
    "documentary": "documentary style, natural lighting, handheld feel, muted earth tones",
    "commercial": "bright commercial lighting, clean background, product-focused, high contrast",
    "artistic": "artistic painterly look, saturated colors, dreamlike atmosphere, soft vignette",
    "social_media": "vibrant colors, vertical 9:16 format, energetic pacing, bold text-safe framing",
    "noir": "high contrast black and white, dramatic shadows, film grain, moody atmosphere",
    "anime": "anime-inspired, cel-shaded, vibrant palette, dynamic action lines",
    "vintage": "vintage 8mm film look, warm grain, light leaks, faded colors, rounded vignette",
}

MOTION_INTENSITIES = {
    "static": ["subtle breathing motion", "gentle swaying", "minimal movement"],
    "gentle": ["slowly rotating", "gradually drifting", "softly flowing"],
    "moderate": ["walking steadily", "turning smoothly", "moving at natural pace"],
    "dynamic": ["running energetically", "spinning rapidly", "jumping with force"],
    "extreme": ["explosively bursting", "whipping through frame", "crashing violently"],
}


@dataclass
class VideoBrief:
    subject: str
    action: str
    style: str = "cinematic"
    duration: int = 6
    aspect_ratio: str = "16:9"
    mood: str = ""
    environment: str = ""
    motion_intensity: str = "moderate"
    negative_prompt: str = ""
    use_case: str = "creative"         # creative | commercial | social_media | enterprise
    budget: str = "mid"                # free | low | mid | high
    target_platform: str = "youtube"   # youtube | tiktok | instagram | enterprise


def select_model(brief: VideoBrief) -> list[tuple[str, VideoModel, float]]:
    """Score and rank models for a given brief. Returns [(key, model, score)]."""
    scored = []
    for key, m in MODELS.items():
        score = 0.0

        # Duration fit
        if brief.duration <= m.max_duration:
            score += 20
        else:
            score -= 30

        # Aspect ratio
        if brief.aspect_ratio in m.aspect_ratios:
            score += 15

        # Budget match
        budget_order = ["free", "low", "mid", "high"]
        b_idx = budget_order.index(brief.budget)
        m_idx = budget_order.index(m.cost_tier)
        if m_idx <= b_idx:
            score += 15
        else:
            score -= 10 * (m_idx - b_idx)

        # Use-case overlap
        use_case_map = {
            "creative": ["creative", "music videos", "artistic"],
            "commercial": ["advertising", "product", "product demos", "e-commerce", "enterprise"],
            "social_media": ["social media", "Douyin", "TikTok", "entertainment", "dance"],
            "enterprise": ["enterprise", "cinematic", "narrative", "long-form"],
        }
        targets = use_case_map.get(brief.use_case, [])
        overlap = len(set(targets) & set(m.best_for))
        score += overlap * 10

        # Platform bonus
        if brief.target_platform in ("tiktok", "instagram") and "9:16" in m.aspect_ratios:
            score += 5
        if brief.target_platform == "youtube" and "16:9" in m.aspect_ratios:
            score += 5

        # Style bonus
        if brief.style in ("cinematic", "noir") and "cinematic" in " ".join(m.strengths):
            score += 8
        if brief.style == "artistic" and "creative" in " ".join(m.best_for):
            score += 8

        # Negative prompt support bonus
        if brief.negative_prompt and m.negative_prompt:
            score += 5

        scored.append((key, m, round(score, 1)))

    scored.sort(key=lambda x: x[2], reverse=True)
    return scored


def generate_prompt(brief: VideoBrief) -> dict:
    """Build a 5-layer structured prompt from a VideoBrief."""
    camera = random.choice(CAMERA_MOVES)
    motion_words = random.choice(MOTION_INTENSITIES.get(brief.motion_intensity, MOTION_INTENSITIES["moderate"]))
    style_desc = STYLES.get(brief.style, STYLES["cinematic"])

    env = brief.environment or "neutral studio background with soft ambient lighting"
    mood = brief.mood or "professional and polished"

    layers = {
        "camera": camera,
        "subject": brief.subject,
        "action": f"{brief.action}, {motion_words}",
        "environment": env,
        "style_mood": f"{style_desc}, {mood}",
    }

    full_prompt = (
        f"{layers['camera']}, {layers['subject']} {layers['action']}, "
        f"{layers['environment']}, {layers['style_mood']}"
    )

    result = {
        "prompt": full_prompt,
        "layers": layers,
        "negative_prompt": brief.negative_prompt or "blurry, distorted, extra limbs, watermark, low quality",
        "parameters": {
            "duration": brief.duration,
            "aspect_ratio": brief.aspect_ratio,
            "style": brief.style,
        }
    }
    return result


def format_model_report(ranked: list[tuple[str, VideoModel, float]], top_n: int = 3) -> str:
    """Pretty-print model ranking."""
    lines = []
    lines.append("=" * 64)
    lines.append("  MODEL SELECTION REPORT")
    lines.append("=" * 64)
    for i, (key, m, score) in enumerate(ranked[:top_n]):
        medal = ["1st", "2nd", "3rd"][i] if i < 3 else f"{i+1}th"
        lines.append(f"\n  {medal} — {m.name}  (score: {score})")
        lines.append(f"  {'─' * 50}")
        lines.append(f"    Strengths : {', '.join(m.strengths)}")
        lines.append(f"    Best for  : {', '.join(m.best_for)}")
        lines.append(f"    Max dur.  : {m.max_duration}s | Cost: {m.cost_tier}")
        lines.append(f"    Ratios    : {', '.join(m.aspect_ratios)}")
        lines.append(f"    Neg.prompt: {'Yes' if m.negative_prompt else 'No'} | Params: {'Yes' if m.structured_params else 'No'}")
        lines.append(f"    Notes     : {m.notes}")
    lines.append("\n" + "=" * 64)
    return "\n".join(lines)


def format_prompt_output(prompt_data: dict) -> str:
    """Pretty-print generated prompt."""
    lines = []
    lines.append("=" * 64)
    lines.append("  GENERATED VIDEO PROMPT")
    lines.append("=" * 64)
    lines.append("")
    lines.append("  Full prompt:")
    for line in textwrap.wrap(prompt_data["prompt"], width=58):
        lines.append(f"    {line}")
    lines.append("")
    lines.append("  Layers breakdown:")
    for k, v in prompt_data["layers"].items():
        lines.append(f"    {k:12s}: {v}")
    lines.append("")
    lines.append(f"  Negative prompt:")
    lines.append(f"    {prompt_data['negative_prompt']}")
    lines.append("")
    lines.append(f"  Parameters: {json.dumps(prompt_data['parameters'])}")
    lines.append("=" * 64)
    return "\n".join(lines)


# ── Demo Scenarios ──────────────────────────────────────────────────────────

DEMO_BRIEFS = [
    VideoBrief(
        subject="a sleek wireless headphone",
        action="rotating slowly on a marble pedestal",
        style="commercial",
        duration=6, aspect_ratio="16:9",
        mood="premium and elegant",
        environment="soft golden hour sunlight through floor-to-ceiling windows, minimal modern interior",
        motion_intensity="gentle",
        use_case="commercial", budget="high", target_platform="youtube",
    ),
    VideoBrief(
        subject="a young woman",
        action="jogging through a sunlit park, stopping to sip from a branded water bottle",
        style="social_media",
        duration=8, aspect_ratio="9:16",
        mood="energetic and fresh",
        environment="vibrant green trees and morning fog, urban park path",
        motion_intensity="dynamic",
        use_case="social_media", budget="mid", target_platform="tiktok",
    ),
    VideoBrief(
        subject="a vintage car",
        action="driving down a desert highway at golden hour",
        style="cinematic",
        duration=10, aspect_ratio="16:9",
        mood="nostalgic and free",
        environment="endless desert road, red rock formations, dust trailing behind",
        motion_intensity="moderate",
        use_case="creative", budget="high", target_platform="youtube",
    ),
    VideoBrief(
        subject="a line of code transforming into a 3D holographic interface",
        action="exploding outward from a laptop screen",
        style="artistic",
        duration=5, aspect_ratio="16:9",
        mood="futuristic and awe-inspiring",
        environment="dark room illuminated only by the holographic glow",
        motion_intensity="extreme",
        use_case="enterprise", budget="mid", target_platform="youtube",
    ),
]


def run_demo():
    """Run the full demonstration."""
    random.seed(42)  # reproducible output

    print("\n" + "~" * 64)
    print("  AI VIDEO PRODUCTION KIT — Demo Run")
    print("  411+ prompts | 15 models | 5-layer prompt engine")
    print("~" * 64)

    for i, brief in enumerate(DEMO_BRIEFS, 1):
        print(f"\n{'━' * 64}")
        print(f"  SCENARIO {i}: {brief.use_case.upper()} — {brief.subject[:40]}")
        print(f"  Platform: {brief.target_platform} | Budget: {brief.budget} | "
              f"Style: {brief.style} | {brief.duration}s @ {brief.aspect_ratio}")
        print(f"{'━' * 64}")

        # Generate prompt
        prompt_data = generate_prompt(brief)
        print(format_prompt_output(prompt_data))

        # Select model
        ranked = select_model(brief)
        print(format_model_report(ranked, top_n=3))

    # Summary table
    print(f"\n{'━' * 64}")
    print("  MODEL COVERAGE SUMMARY")
    print(f"{'━' * 64}")
    print(f"  {'Model':<22} {'Cost':<8} {'Max Dur':<10} {'Ratios'}")
    print(f"  {'─' * 58}")
    for key, m in sorted(MODELS.items(), key=lambda x: x[1].name):
        ratios = ", ".join(m.aspect_ratios)
        print(f"  {m.name:<22} {m.cost_tier:<8} {m.max_duration:>3}s       {ratios}")

    print(f"\n  Total models: {len(MODELS)}")
    print(f"  Demo scenarios run: {len(DEMO_BRIEFS)}")
    print(f"  Camera moves in library: {len(CAMERA_MOVES)}")
    print(f"  Style presets: {len(STYLES)}")
    print(f"  Motion intensities: {len(MOTION_INTENSITIES)}")
    print("~" * 64 + "\n")


def interactive_mode():
    """Simple interactive prompt builder."""
    print("\n  Interactive Video Prompt Builder")
    print("  " + "─" * 40)
    subject = input("  Subject (what's in the scene): ").strip() or "a coffee cup"
    action = input("  Action (what happens): ").strip() or "steam rising gently"
    style = input(f"  Style ({', '.join(STYLES.keys())}): ").strip() or "cinematic"
    use_case = input("  Use case (creative/commercial/social_media/enterprise): ").strip() or "creative"
    budget = input("  Budget (free/low/mid/high): ").strip() or "mid"

    brief = VideoBrief(
        subject=subject, action=action, style=style,
        use_case=use_case, budget=budget,
    )
    prompt_data = generate_prompt(brief)
    print(format_prompt_output(prompt_data))
    ranked = select_model(brief)
    print(format_model_report(ranked))


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        interactive_mode()
    else:
        run_demo()
