#!/usr/bin/env python3
"""
Nemotron-Labs Diffusion Language Model — Deployment Demo

Simulates the three generation modes (Autoregressive, Diffusion, Self-Speculation)
to illustrate how Diffusion LMs generate text differently from standard AR models.

No GPU or model download required — uses mock token generation to demonstrate
the conceptual difference and expected throughput characteristics.
"""

import time
import random
import argparse
import json
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Mock vocabulary / token simulation
# ---------------------------------------------------------------------------

SAMPLE_RESPONSES = {
    "Explain diffusion language models.": (
        "Diffusion language models generate text by iteratively refining a sequence "
        "of masked tokens in parallel, rather than producing one token at a time from "
        "left to right. Starting from a fully masked sequence, the model predicts all "
        "tokens simultaneously, then selectively re-masks the least confident predictions "
        "and refines them over multiple denoising steps. This parallel generation strategy "
        "leads to significantly higher GPU utilization and faster inference compared to "
        "traditional autoregressive models, while maintaining comparable output quality."
    ),
    "What are the advantages of parallel token generation?": (
        "Parallel token generation offers several key advantages over sequential decoding. "
        "First, it dramatically improves GPU compute utilization by processing multiple "
        "tokens per forward pass instead of one. Second, it enables token revision — the "
        "model can reconsider and fix earlier tokens based on later context. Third, it "
        "provides a flexible compute budget: you can reduce refinement steps to trade "
        "accuracy for speed. Finally, it naturally supports fill-in-the-middle tasks since "
        "the model is trained to predict tokens at any position, not just the next one."
    ),
    "default": (
        "NVIDIA Nemotron-Labs Diffusion Language Models represent a new paradigm in text "
        "generation. Unlike autoregressive models that generate one token at a time, these "
        "models use masked diffusion to generate blocks of 32 tokens in parallel. Through "
        "iterative denoising, the model refines all positions simultaneously, achieving up "
        "to 4x real-world throughput on B200 GPUs while matching or exceeding the accuracy "
        "of comparable autoregressive models like Qwen3 8B."
    ),
}

# ---------------------------------------------------------------------------
# Generation mode simulators
# ---------------------------------------------------------------------------

@dataclass
class GenerationResult:
    mode: str
    tokens: List[str]
    total_tokens: int
    wall_time_ms: float
    tokens_per_second: float
    forward_passes: int
    tokens_per_forward_pass: float
    steps_detail: Optional[List[dict]] = field(default_factory=list)


def tokenize(text: str) -> List[str]:
    """Simple whitespace + punctuation tokenizer for demo purposes."""
    tokens = []
    current = ""
    for ch in text:
        if ch in " \t\n":
            if current:
                tokens.append(current)
                current = ""
        elif ch in ".,;:!?—()[]{}":
            if current:
                tokens.append(current)
                current = ""
            tokens.append(ch)
        else:
            current += ch
    if current:
        tokens.append(current)
    return tokens


MASK = "[MASK]"


def simulate_autoregressive(text: str, verbose: bool = False) -> GenerationResult:
    """Simulate standard left-to-right autoregressive generation."""
    tokens = tokenize(text)
    n = len(tokens)
    steps = []

    # AR generates 1 token per forward pass
    base_latency_per_token_ms = 4.0  # ~250 tok/s baseline on B200
    start = time.time()

    for i, tok in enumerate(tokens):
        time.sleep(base_latency_per_token_ms / 1000.0)
        if verbose and i % 10 == 0:
            steps.append({
                "step": i + 1,
                "action": f"decode token {i+1}/{n}",
                "generated": tok,
                "sequence": " ".join(tokens[:i+1]) + " ...",
            })

    wall_ms = (time.time() - start) * 1000
    return GenerationResult(
        mode="Autoregressive",
        tokens=tokens,
        total_tokens=n,
        wall_time_ms=wall_ms,
        tokens_per_second=n / (wall_ms / 1000) if wall_ms > 0 else 0,
        forward_passes=n,
        tokens_per_forward_pass=1.0,
        steps_detail=steps,
    )


def simulate_diffusion(text: str, block_size: int = 32, refine_steps: int = 4,
                        verbose: bool = False) -> GenerationResult:
    """Simulate masked-diffusion parallel generation."""
    tokens = tokenize(text)
    n = len(tokens)
    num_blocks = (n + block_size - 1) // block_size
    steps = []

    # Diffusion processes block_size tokens per forward pass, with refine_steps
    latency_per_forward_ms = 5.0  # slightly more compute per pass
    total_forward_passes = num_blocks * refine_steps
    start = time.time()

    for b in range(num_blocks):
        block_start = b * block_size
        block_end = min(block_start + block_size, n)
        block_tokens = tokens[block_start:block_end]
        current = [MASK] * len(block_tokens)

        for step in range(refine_steps):
            time.sleep(latency_per_forward_ms / 1000.0)
            # Each step reveals more tokens
            reveal_count = max(1, len(block_tokens) * (step + 1) // refine_steps)
            indices = sorted(random.sample(range(len(block_tokens)), min(reveal_count, len(block_tokens))))
            for idx in indices:
                current[idx] = block_tokens[idx]

            if verbose:
                display = list(current)
                steps.append({
                    "step": b * refine_steps + step + 1,
                    "action": f"block {b+1}/{num_blocks}, refine {step+1}/{refine_steps}",
                    "revealed": reveal_count,
                    "sequence_block": " ".join(display),
                })

        # After final step, ensure all revealed
        for idx in range(len(block_tokens)):
            current[idx] = block_tokens[idx]

    wall_ms = (time.time() - start) * 1000
    return GenerationResult(
        mode="Diffusion (block_size=32)",
        tokens=tokens,
        total_tokens=n,
        wall_time_ms=wall_ms,
        tokens_per_second=n / (wall_ms / 1000) if wall_ms > 0 else 0,
        forward_passes=total_forward_passes,
        tokens_per_forward_pass=n / total_forward_passes if total_forward_passes > 0 else 0,
        steps_detail=steps,
    )


def simulate_self_speculation(text: str, block_size: int = 32, draft_steps: int = 1,
                               verify_steps: int = 1, verbose: bool = False) -> GenerationResult:
    """Simulate linear self-speculation: diffusion draft + causal verify."""
    tokens = tokenize(text)
    n = len(tokens)
    num_blocks = (n + block_size - 1) // block_size
    steps_per_block = draft_steps + verify_steps
    total_forward_passes = num_blocks * steps_per_block
    steps = []

    latency_per_forward_ms = 5.5
    start = time.time()

    for b in range(num_blocks):
        block_start = b * block_size
        block_end = min(block_start + block_size, n)
        block_tokens = tokens[block_start:block_end]

        # Draft phase — diffusion generates candidates
        time.sleep(latency_per_forward_ms / 1000.0 * draft_steps)
        draft = list(block_tokens)  # perfect draft for demo
        # Simulate ~80% acceptance
        for i in range(len(draft)):
            if random.random() < 0.2:
                draft[i] = random.choice(["the", "a", "of", "is"])  # wrong token

        if verbose:
            steps.append({
                "step": b * steps_per_block + 1,
                "action": f"block {b+1}/{num_blocks} — DRAFT (diffusion)",
                "draft": " ".join(draft),
                "accepted_pct": f"{sum(1 for d, t in zip(draft, block_tokens) if d == t) / len(block_tokens) * 100:.0f}%",
            })

        # Verify phase — causal model corrects
        time.sleep(latency_per_forward_ms / 1000.0 * verify_steps)
        verified = list(block_tokens)  # verification fixes all

        if verbose:
            steps.append({
                "step": b * steps_per_block + 2,
                "action": f"block {b+1}/{num_blocks} — VERIFY (causal)",
                "verified": " ".join(verified),
            })

    wall_ms = (time.time() - start) * 1000
    return GenerationResult(
        mode="Self-Speculation (Linear)",
        tokens=tokens,
        total_tokens=n,
        wall_time_ms=wall_ms,
        tokens_per_second=n / (wall_ms / 1000) if wall_ms > 0 else 0,
        forward_passes=total_forward_passes,
        tokens_per_forward_pass=n / total_forward_passes if total_forward_passes > 0 else 0,
        steps_detail=steps,
    )


# ---------------------------------------------------------------------------
# Benchmark comparison
# ---------------------------------------------------------------------------

def run_benchmark(prompt: str, verbose: bool = False) -> dict:
    """Run all three modes and return comparison."""
    response_text = SAMPLE_RESPONSES.get(prompt, SAMPLE_RESPONSES["default"])

    print(f"\n{'='*72}")
    print(f"  PROMPT: {prompt}")
    print(f"{'='*72}")
    print(f"\n  RESPONSE ({len(tokenize(response_text))} tokens):")
    for line in textwrap.wrap(response_text, width=68):
        print(f"    {line}")

    results = []

    print(f"\n{'─'*72}")
    print("  Running Autoregressive mode...")
    ar = simulate_autoregressive(response_text, verbose=verbose)
    results.append(ar)
    print(f"    Done: {ar.tokens_per_second:.0f} tok/s, {ar.forward_passes} forward passes")

    print("  Running Diffusion mode...")
    diff = simulate_diffusion(response_text, verbose=verbose)
    results.append(diff)
    print(f"    Done: {diff.tokens_per_second:.0f} tok/s, {diff.forward_passes} forward passes")

    print("  Running Self-Speculation (Linear) mode...")
    spec = simulate_self_speculation(response_text, verbose=verbose)
    results.append(spec)
    print(f"    Done: {spec.tokens_per_second:.0f} tok/s, {spec.forward_passes} forward passes")

    # Comparison table
    print(f"\n{'─'*72}")
    print(f"  {'Mode':<30} {'Tok/s':>8} {'Fwd Passes':>12} {'Tok/Pass':>10} {'Speedup':>8}")
    print(f"  {'─'*30} {'─'*8} {'─'*12} {'─'*10} {'─'*8}")
    ar_tps = ar.tokens_per_second
    for r in results:
        speedup = r.tokens_per_second / ar_tps if ar_tps > 0 else 0
        print(f"  {r.mode:<30} {r.tokens_per_second:>8.0f} {r.forward_passes:>12} "
              f"{r.tokens_per_forward_pass:>10.1f} {speedup:>7.1f}x")

    # Show detailed steps if verbose
    if verbose:
        for r in results:
            if r.steps_detail:
                print(f"\n  --- {r.mode} Steps ---")
                for s in r.steps_detail[:6]:  # limit output
                    print(f"    {json.dumps(s, indent=None)}")
                if len(r.steps_detail) > 6:
                    print(f"    ... ({len(r.steps_detail) - 6} more steps)")

    print(f"\n{'='*72}")

    return {
        "prompt": prompt,
        "response_tokens": len(tokenize(response_text)),
        "modes": [
            {
                "mode": r.mode,
                "tokens_per_second": round(r.tokens_per_second, 1),
                "forward_passes": r.forward_passes,
                "tokens_per_forward_pass": round(r.tokens_per_forward_pass, 1),
                "speedup_vs_ar": round(r.tokens_per_second / ar_tps, 2) if ar_tps > 0 else 0,
            }
            for r in results
        ],
    }


# ---------------------------------------------------------------------------
# SGLang server launch command generator
# ---------------------------------------------------------------------------

def print_sglang_commands(model: str = "nvidia/Nemotron-Labs-Diffusion-8B-Instruct"):
    """Print the SGLang launch commands for each mode."""
    print(f"\n{'='*72}")
    print("  SGLang Server Launch Commands")
    print(f"{'='*72}\n")

    modes = [
        ("Autoregressive", f"python -m sglang.launch_server \\\n"
         f"    --model {model} \\\n"
         f"    --ar-mode true"),
        ("Diffusion", f"python -m sglang.launch_server \\\n"
         f"    --model {model} \\\n"
         f"    --ar-mode false"),
        ("Self-Speculation", f"python -m sglang.launch_server \\\n"
         f"    --model {model} \\\n"
         f"    --ar-mode false \\\n"
         f"    --speculation-mode linear"),
    ]

    for name, cmd in modes:
        print(f"  # {name} mode")
        print(f"  {cmd}\n")

    print("  # Query (OpenAI-compatible)")
    print(textwrap.dedent(f"""\
      curl http://localhost:30000/v1/chat/completions \\
        -H "Content-Type: application/json" \\
        -d '{{"model": "{model}",
              "messages": [{{"role": "user", "content": "Hello!"}}],
              "max_tokens": 512}}'
    """))


# ---------------------------------------------------------------------------
# Model catalog
# ---------------------------------------------------------------------------

MODEL_CATALOG = [
    {"name": "Nemotron-Labs-Diffusion-3B-Base", "params": "3B", "type": "base"},
    {"name": "Nemotron-Labs-Diffusion-3B-Instruct", "params": "3B", "type": "instruct"},
    {"name": "Nemotron-Labs-Diffusion-8B-Base", "params": "8B", "type": "base"},
    {"name": "Nemotron-Labs-Diffusion-8B-Instruct", "params": "8B", "type": "instruct"},
    {"name": "Nemotron-Labs-Diffusion-14B-Base", "params": "14B", "type": "base"},
    {"name": "Nemotron-Labs-Diffusion-14B-Instruct", "params": "14B", "type": "instruct"},
    {"name": "Nemotron-Labs-Diffusion-8B-VLM", "params": "8B", "type": "vision"},
]


def print_model_catalog():
    print(f"\n{'='*72}")
    print("  Nemotron-Labs Diffusion Model Catalog")
    print(f"{'='*72}\n")
    print(f"  {'Model':<45} {'Params':>7} {'Type':<10}")
    print(f"  {'─'*45} {'─'*7} {'─'*10}")
    for m in MODEL_CATALOG:
        full = f"nvidia/{m['name']}"
        print(f"  {full:<45} {m['params']:>7} {m['type']:<10}")
    print(f"\n  Collection: https://huggingface.co/collections/nvidia/nemotron-labs-diffusion")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Nemotron-Labs Diffusion LM — Deployment Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python nemotron_dlm_demo.py --benchmark
              python nemotron_dlm_demo.py --benchmark --verbose
              python nemotron_dlm_demo.py --commands
              python nemotron_dlm_demo.py --catalog
              python nemotron_dlm_demo.py --all
        """),
    )
    parser.add_argument("--benchmark", action="store_true",
                        help="Run generation mode comparison benchmark")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show step-by-step generation details")
    parser.add_argument("--commands", action="store_true",
                        help="Print SGLang server launch commands")
    parser.add_argument("--catalog", action="store_true",
                        help="Print available model catalog")
    parser.add_argument("--model", default="nvidia/Nemotron-Labs-Diffusion-8B-Instruct",
                        help="Model name for command generation")
    parser.add_argument("--prompt", default=None,
                        help="Custom prompt for benchmark")
    parser.add_argument("--all", action="store_true",
                        help="Run all demos")

    args = parser.parse_args()

    if not any([args.benchmark, args.commands, args.catalog, args.all]):
        args.all = True

    print("\n" + "=" * 72)
    print("  NEMOTRON-LABS DIFFUSION LANGUAGE MODEL — DEPLOYMENT DEMO")
    print("  Parallel token generation via masked diffusion + self-speculation")
    print("=" * 72)

    if args.catalog or args.all:
        print_model_catalog()

    if args.commands or args.all:
        print_sglang_commands(model=args.model)

    if args.benchmark or args.all:
        prompts = [
            args.prompt or "Explain diffusion language models.",
            "What are the advantages of parallel token generation?",
        ]
        all_results = []
        for prompt in prompts:
            result = run_benchmark(prompt, verbose=args.verbose)
            all_results.append(result)

        # Summary
        print(f"\n{'='*72}")
        print("  SUMMARY: Expected Real-World Performance (B200 GPU)")
        print(f"{'='*72}")
        print("""
    Mode                          Throughput       Speedup
    ─────────────────────────     ──────────       ───────
    Autoregressive                ~215 tok/s       1.0x
    Diffusion (block=32)          ~560 tok/s       2.6x
    Self-Speculation (Linear)     ~865 tok/s       4.0x

    * Numbers from NVIDIA benchmarks on B200 GPU
    * Accuracy: +1.2% avg improvement over Qwen3 8B on standard benchmarks
    * Models: 3B / 8B / 14B (Base + Instruct) + 8B VLM
        """)


if __name__ == "__main__":
    main()
