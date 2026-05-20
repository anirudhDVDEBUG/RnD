"""
Model registry and provider adapters for AI video generation.
Supports: Seedance 2.0, Kling, Wan, Veo, OmniHuman.
"""

import os
import time
import json
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VideoResult:
    model: str
    prompt: str
    file_path: str
    duration_sec: float
    resolution: str
    status: str  # "success" | "failed"
    metadata: dict = field(default_factory=dict)


MODEL_REGISTRY = {
    "seedance": {
        "name": "Seedance 2.0",
        "modes": ["text-to-video", "image-to-video"],
        "best_for": "High-quality motion, dance/movement",
        "env_key": "SEEDANCE_API_KEY",
        "default_resolution": "1280x720",
        "max_duration": 10,
    },
    "kling": {
        "name": "Kling",
        "modes": ["text-to-video", "image-to-video"],
        "best_for": "General-purpose video generation",
        "env_key": "KLING_API_KEY",
        "default_resolution": "1280x720",
        "max_duration": 10,
    },
    "wan": {
        "name": "Wan",
        "modes": ["text-to-video"],
        "best_for": "Creative/artistic video generation",
        "env_key": "WAN_API_KEY",
        "default_resolution": "1024x576",
        "max_duration": 8,
    },
    "veo": {
        "name": "Veo",
        "modes": ["text-to-video"],
        "best_for": "Photorealistic video generation",
        "env_key": "VEO_API_KEY",
        "default_resolution": "1920x1080",
        "max_duration": 8,
    },
    "omnihuman": {
        "name": "OmniHuman",
        "modes": ["image-to-video"],
        "best_for": "Human animation, talking heads",
        "env_key": "OMNIHUMAN_API_KEY",
        "default_resolution": "1024x1024",
        "max_duration": 15,
    },
}


def select_model(prompt: str, mode: str = "text-to-video", preferred: Optional[str] = None) -> str:
    """Auto-select the best model based on prompt content and mode."""
    if preferred and preferred in MODEL_REGISTRY:
        info = MODEL_REGISTRY[preferred]
        if mode in info["modes"]:
            return preferred
        raise ValueError(f"{info['name']} does not support {mode}")

    if mode == "image-to-video":
        # Prefer OmniHuman for people, Seedance otherwise
        lower = prompt.lower()
        if any(w in lower for w in ["person", "human", "face", "talking", "portrait"]):
            return "omnihuman"
        return "seedance"

    # Text-to-video heuristics
    lower = prompt.lower()
    if any(w in lower for w in ["dance", "movement", "motion", "choreograph"]):
        return "seedance"
    if any(w in lower for w in ["realistic", "photorealistic", "cinematic", "4k"]):
        return "veo"
    if any(w in lower for w in ["artistic", "stylized", "anime", "watercolor", "abstract"]):
        return "wan"
    return "kling"  # general-purpose default


def generate_video(
    prompt: str,
    mode: str = "text-to-video",
    model_key: Optional[str] = None,
    image_path: Optional[str] = None,
    output_dir: str = "output",
    mock: bool = False,
) -> VideoResult:
    """Generate a video using the specified or auto-selected model."""
    model_key = model_key or select_model(prompt, mode)
    model_info = MODEL_REGISTRY[model_key]

    if mode == "image-to-video" and not image_path:
        raise ValueError("image_path required for image-to-video mode")

    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    out_file = os.path.join(output_dir, f"{model_key}_{timestamp}.mp4")

    if mock:
        return _mock_generate(model_key, model_info, prompt, mode, out_file)

    # Real API call path (requires keys)
    api_key = os.environ.get(model_info["env_key"])
    if not api_key:
        raise EnvironmentError(
            f"Missing {model_info['env_key']}. Set it to use {model_info['name']}."
        )

    # Placeholder for real provider SDK calls
    raise NotImplementedError(f"Real API integration for {model_info['name']} not yet wired.")


def _mock_generate(model_key, model_info, prompt, mode, out_file):
    """Simulate video generation for demo/testing."""
    # Simulate processing time
    time.sleep(random.uniform(0.3, 0.8))

    # Write a small placeholder file
    with open(out_file, "wb") as f:
        # Write a minimal mock binary header so the file isn't empty
        header = f"MOCK_VIDEO|model={model_key}|prompt={prompt[:80]}|mode={mode}".encode()
        f.write(header)
        f.write(b"\x00" * 256)

    return VideoResult(
        model=model_info["name"],
        prompt=prompt,
        file_path=out_file,
        duration_sec=random.uniform(3.0, model_info["max_duration"]),
        resolution=model_info["default_resolution"],
        status="success",
        metadata={"mode": mode, "mock": True},
    )
