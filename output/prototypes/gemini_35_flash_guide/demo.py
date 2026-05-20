#!/usr/bin/env python3
"""
Gemini 3.5 Flash Guide — interactive demo (no API key required).

Simulates the Claude Code skill experience: given a user question about
Gemini 3.5 Flash, the skill matches trigger phrases and returns the
relevant section from SKILL.md.
"""

import json
import re
import sys
import textwrap
from pathlib import Path

# ── Load skill metadata ──────────────────────────────────────────────
SKILL_PATH = Path(__file__).parent / "SKILL.md"
SKILL_TEXT = SKILL_PATH.read_text()

# ── Pricing data (mock, based on public announcements) ────────────
PRICING = {
    "gemini-2.0-flash": {"input_1m": 0.10, "output_1m": 0.40, "context": "1M"},
    "gemini-2.5-flash": {"input_1m": 0.15, "output_1m": 0.60, "context": "1M"},
    "gemini-3-flash-preview": {"input_1m": 0.20, "output_1m": 0.80, "context": "1M"},
    "gemini-3.5-flash": {"input_1m": 0.30, "output_1m": 1.20, "context": "1M"},
}

MODEL_SPEC = {
    "model_id": "gemini-3.5-flash",
    "knowledge_cutoff": "January 2025",
    "max_input_tokens": 1_048_576,
    "max_output_tokens": 65_536,
    "computer_use": False,
    "release_status": "GA",
}

# ── Trigger matching ─────────────────────────────────────────────────
TRIGGERS = [
    r"gemini.?3\.?5.?flash",
    r"gemini flash pricing",
    r"google i/?o 2026",
    r"migrat.*flash",
    r"gemini-3\.5-flash",
    r"gemini-3-flash-preview",
]


def matches_trigger(text: str) -> bool:
    lower = text.lower()
    return any(re.search(t, lower) for t in TRIGGERS)


# ── Section extractor ────────────────────────────────────────────────
def extract_section(heading_fragment: str) -> str:
    """Pull a ##-level section out of SKILL.md by heading substring."""
    pattern = rf"(## .*{re.escape(heading_fragment)}.*?)(?=\n## |\Z)"
    m = re.search(pattern, SKILL_TEXT, re.S | re.I)
    return m.group(1).strip() if m else ""


# ── Demo scenarios ───────────────────────────────────────────────────
SCENARIOS = [
    {
        "question": "What's the model ID for the latest Gemini Flash?",
        "handler": "spec",
    },
    {
        "question": "How does Gemini 3.5 Flash pricing compare to older Flash models?",
        "handler": "pricing",
    },
    {
        "question": "Show me a Python snippet to call Gemini 3.5 Flash.",
        "handler": "api",
    },
    {
        "question": "How do I migrate from gemini-3-flash-preview?",
        "handler": "migration",
    },
]


def handle_spec() -> str:
    lines = ["Model Specifications for Gemini 3.5 Flash", "=" * 44]
    for k, v in MODEL_SPEC.items():
        label = k.replace("_", " ").title()
        lines.append(f"  {label:.<30} {v}")
    return "\n".join(lines)


def handle_pricing() -> str:
    lines = [
        "Flash-Family Pricing Comparison (per 1M tokens)",
        "=" * 50,
        f"  {'Model':<28} {'Input':>8}  {'Output':>8}",
        "  " + "-" * 46,
    ]
    for model, p in PRICING.items():
        lines.append(
            f"  {model:<28} ${p['input_1m']:<7.2f}  ${p['output_1m']:<7.2f}"
        )
    lines.append("")
    lines.append(
        "  Note: 3.5 Flash is ~3x the input cost and ~3x the output cost"
    )
    lines.append("  compared to 2.0 Flash. Still the cheapest in the Gemini lineup.")
    return "\n".join(lines)


def handle_api() -> str:
    return textwrap.dedent("""\
        Python SDK snippet (google-generativeai >= 0.8.0)
        ==================================================

        import google.generativeai as genai

        genai.configure(api_key="YOUR_API_KEY")
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content("Summarize recent AI model releases.")
        print(response.text)

        Curl equivalent
        ================
        curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=$API_KEY" \\
          -H 'Content-Type: application/json' \\
          -d '{"contents":[{"parts":[{"text":"Summarize recent AI model releases."}]}]}'
    """)


def handle_migration() -> str:
    return textwrap.dedent("""\
        Migration Checklist: gemini-3-flash-preview -> gemini-3.5-flash
        =================================================================

        1. Replace model ID
           - Old: gemini-3-flash-preview  (or gemini-2.5-flash)
           - New: gemini-3.5-flash

        2. Feature check
           - Computer use: NOT available in 3.5 Flash
           - All other Gemini 3.x features: supported

        3. Test output quality
           - Run your eval suite — outputs may differ on identical prompts

        4. Update cost projections
           - Input:  $0.20 -> $0.30 per 1M tokens  (+50%)
           - Output: $0.80 -> $1.20 per 1M tokens  (+50%)

        5. Check API surface
           - New Interactions API (beta) available for server-side
             conversation history — evaluate if useful for your workflow
    """)


HANDLERS = {
    "spec": handle_spec,
    "pricing": handle_pricing,
    "api": handle_api,
    "migration": handle_migration,
}


# ── Main ─────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Gemini 3.5 Flash Guide — Claude Code Skill Demo")
    print("=" * 60)
    print()

    for i, scenario in enumerate(SCENARIOS, 1):
        q = scenario["question"]
        triggered = matches_trigger(q)
        handler = HANDLERS[scenario["handler"]]

        print(f"--- Scenario {i}/{len(SCENARIOS)} ---")
        print(f"User: {q}")
        print(f"Trigger matched: {triggered}")
        print()
        print(handler())
        print()

    # Summary
    print("=" * 60)
    print("  Skill coverage summary")
    print("=" * 60)
    print(f"  Trigger patterns:  {len(TRIGGERS)}")
    print(f"  Model spec fields: {len(MODEL_SPEC)}")
    print(f"  Pricing models:    {len(PRICING)}")
    print(f"  SKILL.md size:     {len(SKILL_TEXT)} chars")
    print()
    print("  Install: cp -r gemini_35_flash_guide ~/.claude/skills/")
    print("  Then ask Claude Code about Gemini 3.5 Flash to activate.")
    print()


if __name__ == "__main__":
    main()
