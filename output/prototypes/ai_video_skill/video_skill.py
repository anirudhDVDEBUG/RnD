#!/usr/bin/env python3
"""
AI Video Skill — end-to-end demo.

Demonstrates multi-model video generation with a self-improving quality loop.
Runs in mock mode by default (no API keys needed).
"""

import argparse
import json
import sys

from models import MODEL_REGISTRY, select_model
from quality_loop import quality_loop


def print_banner():
    print("=" * 60)
    print("  AI Video Skill — Multi-Model Generation + Quality Loop")
    print("=" * 60)
    print()


def print_model_table():
    print("Supported Models:")
    print(f"  {'Model':<16} {'Modes':<35} {'Best For'}")
    print(f"  {'-'*15}  {'-'*34}  {'-'*30}")
    for key, info in MODEL_REGISTRY.items():
        modes = ", ".join(info["modes"])
        print(f"  {info['name']:<16} {modes:<35} {info['best_for']}")
    print()


def run_demo(prompt, mode="text-to-video", model=None, threshold=0.7, max_iter=3):
    """Run a single generation with the quality loop."""
    chosen = model or select_model(prompt, mode)
    model_info = MODEL_REGISTRY[chosen]

    print(f"Prompt:    {prompt}")
    print(f"Mode:      {mode}")
    print(f"Model:     {model_info['name']} (auto-selected)" if not model else f"Model:     {model_info['name']}")
    print(f"Threshold: {threshold}")
    print(f"Max iters: {max_iter}")
    print()

    result = quality_loop(
        prompt=prompt,
        mode=mode,
        model_key=chosen,
        threshold=threshold,
        max_iterations=max_iter,
        mock=True,
        output_dir="output",
    )

    print(f"--- Quality Loop Results ---")
    for i, score in enumerate(result.scores):
        status = "PASS" if score.overall >= threshold else "RETRY"
        print(
            f"  Iteration {i+1}: "
            f"motion={score.motion_coherence:.2f}  "
            f"adherence={score.prompt_adherence:.2f}  "
            f"fidelity={score.visual_fidelity:.2f}  "
            f"overall={score.overall:.3f}  [{status}]"
        )

    if len(result.prompt_history) > 1:
        print(f"\n  Prompt refined {len(result.prompt_history)-1} time(s):")
        for j, p in enumerate(result.prompt_history):
            label = "original" if j == 0 else f"refined-{j}"
            print(f"    [{label}] {p[:100]}{'...' if len(p)>100 else ''}")

    print(f"\nFinal video: {result.final_video.file_path}")
    print(f"Resolution:  {result.final_video.resolution}")
    print(f"Duration:    {result.final_video.duration_sec:.1f}s")
    print(f"Accepted:    {'Yes' if result.accepted else 'No (below threshold)'}")
    print(f"Iterations:  {result.iterations}")
    return result


def main():
    parser = argparse.ArgumentParser(description="AI Video Skill demo")
    parser.add_argument("--prompt", type=str, help="Text prompt for video generation")
    parser.add_argument("--mode", choices=["text-to-video", "image-to-video"], default="text-to-video")
    parser.add_argument("--model", choices=list(MODEL_REGISTRY.keys()), default=None)
    parser.add_argument("--threshold", type=float, default=0.7)
    parser.add_argument("--max-iter", type=int, default=3)
    parser.add_argument("--all-models", action="store_true", help="Run demo across all text-to-video models")
    args = parser.parse_args()

    print_banner()
    print_model_table()

    if args.all_models:
        prompts = [
            ("A dancer performing ballet in a moonlit garden", "seedance"),
            ("A busy Tokyo street at sunset, cinematic 4K", "veo"),
            ("Watercolor animation of koi fish in a pond", "wan"),
            ("A cat playing piano in a cozy living room", "kling"),
        ]
        print("=" * 60)
        print("  Running multi-model demo (mock mode)")
        print("=" * 60)
        for prompt, model in prompts:
            print(f"\n{'─' * 50}")
            run_demo(prompt, model=model, threshold=args.threshold, max_iter=args.max_iter)
        print(f"\n{'─' * 50}")
        print("\nAll demos complete.")
    elif args.prompt:
        run_demo(args.prompt, mode=args.mode, model=args.model,
                 threshold=args.threshold, max_iter=args.max_iter)
    else:
        # Default demo
        print("Running default demo (use --prompt for custom, --all-models for full sweep)\n")
        run_demo(
            "A golden retriever running through autumn leaves in slow motion",
            threshold=args.threshold,
            max_iter=args.max_iter,
        )


if __name__ == "__main__":
    main()
