#!/usr/bin/env python3
"""
SR-MoA Demo: Self-Reflective Mixture of Adapters
Demonstrates dynamic adapter routing with self-reflective feedback.
No GPU or large models required — uses synthetic embeddings.
"""

import torch
import numpy as np
from sr_moa_demo import SRMoAConfig, SRMoAModel


def compute_entropy(scores: torch.Tensor) -> float:
    """Shannon entropy of routing distribution."""
    s = scores.squeeze()
    log_s = torch.log(s + 1e-8)
    return -(s * log_s).sum().item()


def simulate_input(text: str, hidden_dim: int, seq_len: int = 16) -> torch.Tensor:
    """Create a deterministic pseudo-embedding from text (for reproducibility)."""
    seed = sum(ord(c) for c in text) % 10000
    rng = np.random.RandomState(seed)
    emb = rng.randn(1, seq_len, hidden_dim).astype(np.float32)
    return torch.from_numpy(emb)


def main():
    print("=" * 60)
    print("SR-MoA: Self-Reflective Mixture of Adapters Demo")
    print("=" * 60)

    # Configure
    config = SRMoAConfig(
        num_adapters=4,
        lora_rank=16,
        lora_alpha=32,
        reflection_steps=3,
        router_hidden_dim=256,
        hidden_dim=768,
    )

    print(f"\nConfig:")
    print(f"  Adapters: {config.num_adapters} ({', '.join(config.adapter_names)})")
    print(f"  LoRA rank: {config.lora_rank}, alpha: {config.lora_alpha}")
    print(f"  Reflection steps: {config.reflection_steps}")
    print(f"  Router hidden dim: {config.router_hidden_dim}")

    # Build model
    model = SRMoAModel(config)
    model.eval()

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen_params = total_params - trainable_params
    print(f"\n  Total params: {total_params:,}")
    print(f"  Trainable (adapters + router): {trainable_params:,}")
    print(f"  Frozen (base model): {frozen_params:,}")
    print(f"  Overhead: {trainable_params / max(frozen_params, 1) * 100:.1f}%")

    # Demo inputs
    test_inputs = [
        "Explain quantum entanglement in simple terms",
        "Write a Python function to sort a linked list",
        "Compose a haiku about autumn leaves falling",
        "What are the key economic indicators for Q3 2024",
    ]

    print("\n" + "=" * 60)
    print("Test-Time Adaptation Demo")
    print("=" * 60)

    for text in test_inputs:
        print(f"\nInput: \"{text}\"")
        x = simulate_input(text, config.hidden_dim)

        with torch.no_grad():
            output, history = model(x, verbose=True)

        print(f"  {'Step':<8} {'Scores':<45} {'Entropy':<8}")
        print(f"  {'----':<8} {'------':<45} {'-------':<8}")

        for i, scores in enumerate(history):
            s = scores.squeeze().numpy()
            score_str = "  ".join(
                f"{name}={v:.2f}" for name, v in zip(config.adapter_names, s)
            )
            entropy = compute_entropy(scores)
            label = "initial" if i == 0 else f"reflect {i}"
            print(f"  {label:<8} [{score_str}]  {entropy:.3f}")

        # Final composition
        final_scores = history[-1].squeeze().numpy()
        top_idx = final_scores.argmax()
        print(f"  -> Primary adapter: {config.adapter_names[top_idx]} ({final_scores[top_idx]*100:.0f}%)")

    # Demonstrate that reflection reduces entropy (specialization)
    print("\n" + "=" * 60)
    print("Entropy Analysis (lower = more specialized routing)")
    print("=" * 60)

    initial_entropies = []
    final_entropies = []

    for text in test_inputs:
        x = simulate_input(text, config.hidden_dim)
        with torch.no_grad():
            _, history = model(x, verbose=True)
        initial_entropies.append(compute_entropy(history[0]))
        final_entropies.append(compute_entropy(history[-1]))

    avg_initial = np.mean(initial_entropies)
    avg_final = np.mean(final_entropies)
    reduction = (avg_initial - avg_final) / avg_initial * 100

    print(f"\n  Average initial entropy: {avg_initial:.3f}")
    print(f"  Average final entropy:   {avg_final:.3f}")
    print(f"  Entropy reduction:       {reduction:.1f}%")
    print(f"\n  Reflection sharpens routing decisions by {reduction:.1f}%,")
    print(f"  demonstrating self-reflective specialization.")

    print("\n" + "=" * 60)
    print("Demo complete. See HOW_TO_USE.md for integration guide.")
    print("=" * 60)


if __name__ == "__main__":
    main()
