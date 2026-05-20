"""
Self-improving quality-control loop for AI-generated videos.

Scores each video on multiple dimensions, refines the prompt if quality
is below threshold, and retains successful prompt patterns for future use.
"""

import json
import os
import random
from dataclasses import dataclass, field
from typing import List, Optional

from models import VideoResult, generate_video


@dataclass
class QualityScore:
    motion_coherence: float   # 0-1
    prompt_adherence: float   # 0-1
    visual_fidelity: float    # 0-1
    overall: float = 0.0

    def __post_init__(self):
        self.overall = round(
            0.35 * self.motion_coherence
            + 0.40 * self.prompt_adherence
            + 0.25 * self.visual_fidelity,
            3,
        )


@dataclass
class LoopResult:
    final_video: VideoResult
    iterations: int
    scores: List[QualityScore]
    prompt_history: List[str]
    accepted: bool


PROMPT_HISTORY_FILE = "prompt_history.json"


def _load_prompt_history() -> list:
    if os.path.exists(PROMPT_HISTORY_FILE):
        with open(PROMPT_HISTORY_FILE) as f:
            return json.load(f)
    return []


def _save_prompt_history(history: list):
    with open(PROMPT_HISTORY_FILE, "w") as f:
        json.dump(history[-50:], f, indent=2)  # keep last 50


def evaluate_video(result: VideoResult, mock: bool = False) -> QualityScore:
    """Score a generated video on quality dimensions."""
    if mock:
        # Simulate scores that tend to improve with better prompts
        base = random.uniform(0.45, 0.95)
        return QualityScore(
            motion_coherence=round(min(1.0, base + random.uniform(-0.1, 0.15)), 3),
            prompt_adherence=round(min(1.0, base + random.uniform(-0.05, 0.2)), 3),
            visual_fidelity=round(min(1.0, base + random.uniform(-0.1, 0.1)), 3),
        )
    # Real evaluation would use a vision model or CLIP-based scorer
    raise NotImplementedError("Real quality evaluation requires a vision model.")


def refine_prompt(original: str, score: QualityScore, iteration: int) -> str:
    """Refine a prompt based on quality feedback."""
    additions = []

    if score.motion_coherence < 0.6:
        additions.append("smooth continuous motion, steady camera")
    if score.prompt_adherence < 0.6:
        additions.append("exactly matching the described scene")
    if score.visual_fidelity < 0.6:
        additions.append("high detail, sharp focus, professional quality")

    # Pull from successful history
    history = _load_prompt_history()
    if history:
        # Borrow a quality modifier from a past success
        past = random.choice(history)
        if "quality_modifiers" in past:
            additions.append(past["quality_modifiers"])

    if not additions:
        additions.append("enhanced quality, cinematic lighting")

    refined = f"{original}, {', '.join(additions)}"
    return refined


def quality_loop(
    prompt: str,
    mode: str = "text-to-video",
    model_key: Optional[str] = None,
    image_path: Optional[str] = None,
    threshold: float = 0.7,
    max_iterations: int = 3,
    mock: bool = False,
    output_dir: str = "output",
) -> LoopResult:
    """Run the self-improving generation loop."""
    scores = []
    prompt_history = [prompt]
    current_prompt = prompt
    result = None

    for i in range(max_iterations):
        result = generate_video(
            prompt=current_prompt,
            mode=mode,
            model_key=model_key,
            image_path=image_path,
            output_dir=output_dir,
            mock=mock,
        )

        score = evaluate_video(result, mock=mock)
        scores.append(score)

        if score.overall >= threshold:
            # Save successful pattern
            history = _load_prompt_history()
            history.append({
                "prompt": current_prompt,
                "model": result.model,
                "score": score.overall,
                "quality_modifiers": current_prompt.split(", ")[-1] if ", " in current_prompt else "",
            })
            _save_prompt_history(history)

            return LoopResult(
                final_video=result,
                iterations=i + 1,
                scores=scores,
                prompt_history=prompt_history,
                accepted=True,
            )

        # Refine and retry
        current_prompt = refine_prompt(prompt, score, i)
        prompt_history.append(current_prompt)

    return LoopResult(
        final_video=result,
        iterations=max_iterations,
        scores=scores,
        prompt_history=prompt_history,
        accepted=scores[-1].overall >= threshold if scores else False,
    )
