#!/usr/bin/env python3
"""
Voice AI Transport Protocol Evaluator

Evaluates audio transport protocols for voice AI / LLM-powered audio applications.
Scores each protocol on dimensions critical to voice AI reliability and produces
a recommendation with rationale.

Based on Luke Curley's analysis of WebRTC's packet-dropping problem for AI prompts:
https://moq.dev/blog/webrtc-is-the-problem/
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Scoring dimensions (0-10 scale, higher = better for voice AI)
# ---------------------------------------------------------------------------

DIMENSIONS = [
    "delivery_reliability",   # Does every audio packet arrive?
    "latency",                # How low is end-to-end latency?
    "browser_support",        # Works in-browser without plugins?
    "implementation_ease",    # How easy to set up?
    "bidirectional",          # Supports full-duplex audio?
    "scalability",            # Scales to many concurrent sessions?
]

DIMENSION_LABELS = {
    "delivery_reliability": "Delivery Reliability",
    "latency": "Latency",
    "browser_support": "Browser Support",
    "implementation_ease": "Implementation Ease",
    "bidirectional": "Bidirectional Audio",
    "scalability": "Scalability",
}

# Weight each dimension for a voice-AI use case.
# Reliability is king -- a garbled prompt produces garbage output.
VOICE_AI_WEIGHTS = {
    "delivery_reliability": 3.0,
    "latency": 1.5,
    "browser_support": 1.0,
    "implementation_ease": 1.0,
    "bidirectional": 1.2,
    "scalability": 1.0,
}


@dataclass
class Protocol:
    name: str
    scores: dict  # dimension -> 0-10
    notes: str = ""
    pros: list = field(default_factory=list)
    cons: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Built-in protocol database
# ---------------------------------------------------------------------------

PROTOCOLS = [
    Protocol(
        name="WebRTC",
        scores={
            "delivery_reliability": 4,
            "latency": 10,
            "browser_support": 10,
            "implementation_ease": 6,
            "bidirectional": 10,
            "scalability": 7,
        },
        notes="Optimized for human conversation; aggressively drops packets to minimize latency.",
        pros=[
            "Sub-100ms latency in ideal conditions",
            "Native browser support (no plugins)",
            "Battle-tested for video conferencing",
            "Built-in echo cancellation and noise suppression",
        ],
        cons=[
            "Drops audio packets under congestion -- corrupts LLM prompts",
            "No in-browser retransmission option (confirmed by Discord engineering)",
            "TURN/STUN infrastructure overhead",
            "Users would rather wait 200ms than get garbled input",
        ],
    ),
    Protocol(
        name="WebSocket + Opus",
        scores={
            "delivery_reliability": 9,
            "latency": 6,
            "browser_support": 9,
            "implementation_ease": 9,
            "bidirectional": 9,
            "scalability": 7,
        },
        notes="TCP-based reliable delivery with Opus codec. Simple and predictable.",
        pros=[
            "Guaranteed delivery (TCP)",
            "Easy to implement in any language",
            "Works in all browsers",
            "Simple debugging -- standard HTTP upgrade",
        ],
        cons=[
            "Head-of-line blocking under packet loss",
            "Higher latency than UDP-based protocols (~150-300ms)",
            "No built-in echo cancellation",
        ],
    ),
    Protocol(
        name="MoQ (Media over QUIC)",
        scores={
            "delivery_reliability": 9,
            "latency": 8,
            "browser_support": 4,
            "implementation_ease": 4,
            "bidirectional": 8,
            "scalability": 9,
        },
        notes="Next-gen protocol built on QUIC. Reliable delivery without head-of-line blocking.",
        pros=[
            "Reliable delivery with per-stream flow control",
            "Low latency via QUIC (no head-of-line blocking)",
            "Designed for media -- supports prioritization and partial reliability",
            "Scalable pub/sub architecture",
        ],
        cons=[
            "Limited browser support (requires WebTransport)",
            "Still maturing -- fewer libraries and examples",
            "Requires QUIC-capable infrastructure",
        ],
    ),
    Protocol(
        name="gRPC Streaming",
        scores={
            "delivery_reliability": 9,
            "latency": 6,
            "browser_support": 5,
            "implementation_ease": 7,
            "bidirectional": 9,
            "scalability": 8,
        },
        notes="Bidirectional streaming over HTTP/2 with protobuf. Good for structured payloads.",
        pros=[
            "Reliable delivery (HTTP/2 + TCP)",
            "Structured messages with protobuf -- easy to attach metadata",
            "Excellent tooling and code generation",
            "Bidirectional streaming out of the box",
        ],
        cons=[
            "Browser support requires grpc-web proxy",
            "HTTP/2 head-of-line blocking",
            "Higher overhead per message than raw WebSocket",
        ],
    ),
    Protocol(
        name="HTTP/3 Streaming",
        scores={
            "delivery_reliability": 8,
            "latency": 7,
            "browser_support": 6,
            "implementation_ease": 5,
            "bidirectional": 6,
            "scalability": 8,
        },
        notes="QUIC-based HTTP streaming. Good balance of reliability and latency.",
        pros=[
            "No head-of-line blocking (QUIC multiplexing)",
            "Growing browser support",
            "TLS 1.3 built in",
            "Can use Server-Sent Events or WebTransport",
        ],
        cons=[
            "Bidirectional streaming less mature than WebSocket/gRPC",
            "Fewer off-the-shelf audio libraries",
            "Infrastructure may not support QUIC yet",
        ],
    ),
]


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------

def compute_weighted_score(protocol: Protocol, weights: dict) -> float:
    total_weight = sum(weights.values())
    weighted = sum(
        protocol.scores[dim] * weights[dim] for dim in DIMENSIONS
    )
    return round(weighted / total_weight, 2)


@dataclass
class EvaluationResult:
    protocol: str
    weighted_score: float
    raw_scores: dict
    pros: list
    cons: list
    notes: str


def evaluate_all(
    weights: Optional[dict] = None,
    protocols: Optional[list] = None,
) -> list:
    w = weights or VOICE_AI_WEIGHTS
    protos = protocols or PROTOCOLS

    results = []
    for p in protos:
        score = compute_weighted_score(p, w)
        results.append(EvaluationResult(
            protocol=p.name,
            weighted_score=score,
            raw_scores={DIMENSION_LABELS[k]: v for k, v in p.scores.items()},
            pros=p.pros,
            cons=p.cons,
            notes=p.notes,
        ))

    results.sort(key=lambda r: r.weighted_score, reverse=True)
    return results


# ---------------------------------------------------------------------------
# Scenario presets
# ---------------------------------------------------------------------------

SCENARIOS = {
    "voice_ai_default": {
        "label": "Voice AI / LLM Prompt Streaming (default)",
        "weights": VOICE_AI_WEIGHTS,
    },
    "browser_first": {
        "label": "Browser-First Voice App",
        "weights": {
            "delivery_reliability": 2.5,
            "latency": 1.5,
            "browser_support": 3.0,
            "implementation_ease": 1.5,
            "bidirectional": 1.0,
            "scalability": 0.8,
        },
    },
    "server_to_server": {
        "label": "Server-to-Server Audio Pipeline",
        "weights": {
            "delivery_reliability": 3.0,
            "latency": 1.0,
            "browser_support": 0.0,
            "implementation_ease": 1.5,
            "bidirectional": 1.5,
            "scalability": 2.0,
        },
    },
}


# ---------------------------------------------------------------------------
# CLI & pretty-print
# ---------------------------------------------------------------------------

BAR_WIDTH = 20


def bar(score: float, max_score: float = 10.0) -> str:
    filled = int(BAR_WIDTH * score / max_score)
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def print_report(scenario_key: str = "voice_ai_default"):
    scenario = SCENARIOS[scenario_key]
    results = evaluate_all(weights=scenario["weights"])

    print("=" * 68)
    print(f"  VOICE AI TRANSPORT PROTOCOL EVALUATION")
    print(f"  Scenario: {scenario['label']}")
    print("=" * 68)
    print()

    # Summary table
    print(f"  {'Protocol':<22} {'Score':>6}  {'Bar':<{BAR_WIDTH}}  Verdict")
    print(f"  {'─' * 22} {'─' * 6}  {'─' * BAR_WIDTH}  {'─' * 14}")

    for i, r in enumerate(results):
        verdict = "★ RECOMMENDED" if i == 0 else ""
        print(f"  {r.protocol:<22} {r.weighted_score:>6.2f}  {bar(r.weighted_score)}  {verdict}")
    print()

    # Detailed cards
    for i, r in enumerate(results):
        rank = i + 1
        print(f"  ┌─ #{rank} {r.protocol} ─{'─' * (50 - len(r.protocol))}┐")
        print(f"  │ Weighted Score: {r.weighted_score:.2f} / 10.00")
        print(f"  │")
        print(f"  │ {r.notes}")
        print(f"  │")

        # Dimension breakdown
        print(f"  │ Dimension Scores:")
        for dim_label, score in r.raw_scores.items():
            print(f"  │   {dim_label:<24} {score:>2}/10  {bar(score)}")

        print(f"  │")
        print(f"  │ Pros:")
        for pro in r.pros:
            print(f"  │   + {pro}")
        print(f"  │")
        print(f"  │ Cons:")
        for con in r.cons:
            print(f"  │   - {con}")
        print(f"  └{'─' * 58}┘")
        print()

    # Key insight
    winner = results[0]
    print("─" * 68)
    print("  KEY INSIGHT (from Luke Curley / moq.dev):")
    print()
    print("  WebRTC drops audio packets to keep latency low -- great for video")
    print("  calls, but disastrous for voice AI. A garbled prompt produces a")
    print("  garbage LLM response. Users would rather wait 200ms for accurate")
    print("  input than get instant but corrupted audio.")
    print()
    print(f"  For this scenario, {winner.protocol} scores highest ({winner.weighted_score:.2f}/10).")
    if winner.protocol != "WebRTC":
        print(f"  WebRTC ranks lower due to its unreliable delivery model.")
    print("─" * 68)
    print()


def print_json(scenario_key: str = "voice_ai_default"):
    scenario = SCENARIOS[scenario_key]
    results = evaluate_all(weights=scenario["weights"])
    output = {
        "scenario": scenario["label"],
        "weights": scenario["weights"],
        "results": [
            {
                "rank": i + 1,
                "protocol": r.protocol,
                "weighted_score": r.weighted_score,
                "raw_scores": r.raw_scores,
                "pros": r.pros,
                "cons": r.cons,
                "notes": r.notes,
            }
            for i, r in enumerate(results)
        ],
    }
    print(json.dumps(output, indent=2))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate audio transport protocols for voice AI applications."
    )
    parser.add_argument(
        "--scenario",
        choices=list(SCENARIOS.keys()),
        default="voice_ai_default",
        help="Evaluation scenario (default: voice_ai_default)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--all-scenarios",
        action="store_true",
        help="Run evaluation for all built-in scenarios",
    )
    args = parser.parse_args()

    if args.all_scenarios:
        for key in SCENARIOS:
            if args.json:
                print_json(key)
            else:
                print_report(key)
            print()
    elif args.json:
        print_json(args.scenario)
    else:
        print_report(args.scenario)


if __name__ == "__main__":
    main()
