#!/usr/bin/env python3
"""
Simon Willison Newsletter AI Roundup - Summarizer & Tracker

Fetches and summarizes key AI/LLM developments from Simon Willison's
monthly newsletter. Uses mock data for demo (real usage requires
GitHub Sponsors access or the free archive).
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ModelRelease:
    name: str
    provider: str
    price_input: str
    price_output: str
    price_delta: Optional[str]
    highlights: list[str]


@dataclass
class NewsletterSection:
    title: str
    summary: str
    items: list[str]


@dataclass
class NewsletterRoundup:
    month: str
    year: int
    sections: list[NewsletterSection]
    model_releases: list[ModelRelease]
    tools_picks: list[str]


def load_mock_newsletter() -> dict:
    """Load mock newsletter data representing April 2026 edition."""
    return {
        "month": "April",
        "year": 2026,
        "source": "https://simonwillison.net/2026/May/4/april-newsletter/#atom-everything",
        "sections": [
            {
                "title": "Major Model Releases",
                "summary": "Two headline launches dominated April: Anthropic's Opus 4.7 and OpenAI's GPT-5.5. Both arrived with significant price increases over predecessors, signaling a shift toward premium-tier reasoning models.",
                "items": [
                    "Opus 4.7 launched at $25/$75 per M tokens (up from $15/$75 for Opus 4.5)",
                    "GPT-5.5 launched at $20/$60 per M tokens with 1M context window",
                    "Both models show step-function improvements on ARC-AGI and GPQA benchmarks",
                ]
            },
            {
                "title": "Claude Mythos & Security Research",
                "summary": "Anthropic introduced Claude Mythos, a specialized variant focused on creative and narrative tasks. Separately, new LLM security research revealed prompt injection vectors in tool-use chains.",
                "items": [
                    "Claude Mythos: creative-writing variant with enhanced narrative coherence",
                    "New research on indirect prompt injection via MCP tool responses",
                    "Anthropic published updated responsible disclosure guidelines for AI security",
                ]
            },
            {
                "title": "Image & Multimodal Generation",
                "summary": "ChatGPT Images 2.0 shipped with dramatically improved text rendering and style consistency. Competing offerings from Midjourney V7 and Stable Diffusion 4 also arrived.",
                "items": [
                    "ChatGPT Images 2.0: near-perfect text rendering in generated images",
                    "Midjourney V7 beta launched with video generation capabilities",
                    "Stable Diffusion 4 released as open-weights with commercial license",
                ]
            },
            {
                "title": "Other Notable Releases",
                "summary": "A busy month across the industry with smaller but impactful launches from Google, Meta, and several startups.",
                "items": [
                    "Gemini 2.5 Flash: $0.15/$0.60 per M tokens, competitive with Haiku",
                    "Llama 4 Maverick: 400B MoE model, strong on multilingual tasks",
                    "Mistral Large 3: 123B model with improved code generation",
                    "Qwen 3 family: multiple sizes from 0.6B to 235B",
                ]
            },
        ],
        "model_releases": [
            {"name": "Opus 4.7", "provider": "Anthropic", "price_input": "$25/M", "price_output": "$75/M", "price_delta": "+67% input vs Opus 4.5", "highlights": ["Extended thinking", "1M context", "Tool use improvements"]},
            {"name": "GPT-5.5", "provider": "OpenAI", "price_input": "$20/M", "price_output": "$60/M", "price_delta": "+33% vs GPT-5", "highlights": ["1M context", "Native multimodal", "Improved reasoning"]},
            {"name": "Claude Mythos", "provider": "Anthropic", "price_input": "$8/M", "price_output": "$24/M", "price_delta": "New tier", "highlights": ["Creative writing focus", "Narrative coherence", "Long-form output"]},
            {"name": "Gemini 2.5 Flash", "provider": "Google", "price_input": "$0.15/M", "price_output": "$0.60/M", "price_delta": "-25% vs 2.0 Flash", "highlights": ["Speed optimized", "Multimodal", "Thinking mode"]},
        ],
        "tools_picks": [
            "uv - Python package manager (now with workspace support)",
            "files-to-prompt - CLI to concatenate files for LLM context",
            "llm-claude-4 - Plugin for the llm CLI supporting Claude 4.x models",
            "shot-scraper - Automated screenshots for documentation",
            "sqlite-utils - CLI for manipulating SQLite databases",
        ]
    }


def format_roundup(data: dict) -> str:
    """Format newsletter data into a readable roundup."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  SIMON WILLISON'S AI ROUNDUP - {data['month'].upper()} {data['year']}")
    lines.append(f"{'='*60}")
    lines.append(f"  Source: {data['source']}")
    lines.append("")

    for section in data["sections"]:
        lines.append(f"\n## {section['title']}")
        lines.append(f"   {section['summary']}")
        lines.append("")
        for item in section["items"]:
            lines.append(f"   - {item}")

    lines.append(f"\n{'─'*60}")
    lines.append("\n## Model Pricing Comparison")
    lines.append(f"  {'Model':<18} {'Provider':<12} {'Input':<10} {'Output':<10} {'Delta'}")
    lines.append(f"  {'─'*18} {'─'*12} {'─'*10} {'─'*10} {'─'*20}")
    for m in data["model_releases"]:
        lines.append(f"  {m['name']:<18} {m['provider']:<12} {m['price_input']:<10} {m['price_output']:<10} {m['price_delta']}")

    lines.append(f"\n{'─'*60}")
    lines.append("\n## What I'm Using (Simon's Picks)")
    for tool in data["tools_picks"]:
        lines.append(f"   * {tool}")

    lines.append(f"\n{'='*60}")
    lines.append("  End of roundup. Full newsletter requires GitHub Sponsors ($10/mo).")
    lines.append(f"  Free archive (prior month): github.com/simonw/monthly-newsletter-archive")
    lines.append(f"{'='*60}\n")

    return "\n".join(lines)


def export_json(data: dict) -> str:
    """Export structured roundup as JSON for programmatic use."""
    roundup = NewsletterRoundup(
        month=data["month"],
        year=data["year"],
        sections=[NewsletterSection(**s) for s in data["sections"]],
        model_releases=[ModelRelease(**m) for m in data["model_releases"]],
        tools_picks=data["tools_picks"],
    )
    return json.dumps(asdict(roundup), indent=2)


def main():
    print("Loading April 2026 newsletter data (mock)...\n")
    data = load_mock_newsletter()

    if "--json" in sys.argv:
        print(export_json(data))
    else:
        print(format_roundup(data))

    if "--export" in sys.argv:
        output_path = "roundup_april_2026.json"
        with open(output_path, "w") as f:
            f.write(export_json(data))
        print(f"\nExported structured data to {output_path}")


if __name__ == "__main__":
    main()
