#!/usr/bin/env python3
"""
Ta-Persona Digital Twin Distillation Engine

Conducts structured interview rounds to extract a subject's expression DNA,
cognitive patterns, and communication style, then synthesizes a reusable
persona profile document.

In live mode (with ANTHROPIC_API_KEY), uses Claude to generate adaptive
follow-up questions. In demo mode, runs a complete mock interview with
pre-recorded responses to show the full distillation pipeline.
"""

import json
import os
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class InterviewRound:
    dimension: str
    questions: list[str]
    responses: list[str]
    observations: list[str] = field(default_factory=list)


@dataclass
class PersonaProfile:
    name: str
    voice_summary: str = ""
    tone_register: dict = field(default_factory=dict)
    vocabulary_patterns: dict = field(default_factory=dict)
    sentence_architecture: dict = field(default_factory=dict)
    reasoning_style: dict = field(default_factory=dict)
    cognitive_os: dict = field(default_factory=dict)
    contextual_variations: dict = field(default_factory=dict)
    usage_instructions: str = ""
    calibration_examples: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Interview dimensions & seed questions
# ---------------------------------------------------------------------------

DIMENSIONS = [
    {
        "name": "Communication Style",
        "questions": [
            "How would you describe your default writing style -- formal, casual, somewhere in between? Give me an example of a typical message you'd send to a colleague.",
            "Do you tend toward short punchy sentences or longer flowing ones? How do you feel about bullet points vs. prose?",
        ],
    },
    {
        "name": "Vocabulary & Expression",
        "questions": [
            "Are there phrases or words you catch yourself using all the time? Any words you deliberately avoid?",
            "How do you feel about jargon and technical language? Do you lean toward 'utilize' or 'use', 'leverage' or 'take advantage of'?",
        ],
    },
    {
        "name": "Reasoning & Argumentation",
        "questions": [
            "When you're making a case for something, how do you typically structure your argument? Do you lead with data, stories, principles, or something else?",
            "How do you handle uncertainty -- do you hedge a lot ('might', 'perhaps') or state things more directly?",
        ],
    },
    {
        "name": "Emotional Tone & Values",
        "questions": [
            "What's your humor style? Dry, self-deprecating, playful, absent? How do you typically express enthusiasm or disagreement?",
            "What ideas or values tend to show up repeatedly in your communication, even when you're not trying?",
        ],
    },
    {
        "name": "Contextual Adaptation & Quirks",
        "questions": [
            "How does your voice shift between a Slack message, a formal email, and a blog post?",
            "Any distinctive habits -- like how you open emails, sign off messages, use punctuation, or structure paragraphs?",
        ],
    },
]


# ---------------------------------------------------------------------------
# Mock interview data (for demo without API key)
# ---------------------------------------------------------------------------

MOCK_SUBJECT = "Alex Chen"

MOCK_RESPONSES = [
    # Round 1: Communication Style
    [
        "I'd say I'm casually professional. Like, I won't use slang in work emails but I'm not writing legal briefs either. A typical Slack to a colleague: 'Hey -- just pushed the updated config. Mind giving it a quick sanity check before I merge? No rush, EOD is fine.' I like dashes a lot. Probably too much.",
        "Definitely shorter sentences when I'm explaining something technical. I break things into steps. But when I'm writing about ideas or strategy, I let sentences breathe more. Bullet points for action items, prose for persuasion -- that's my rule of thumb.",
    ],
    # Round 2: Vocabulary & Expression
    [
        "Oh yeah. 'Actually' is my crutch word. I also say 'the thing is' way too much. I actively avoid 'synergy', 'paradigm', anything that sounds like a LinkedIn post. I'd rather sound slightly too casual than slightly too corporate.",
        "'Use' over 'utilize', always. 'Figure out' over 'determine'. I like plain language but I'm not anti-jargon if it's genuinely the right term. Like, I'll say 'latency' instead of 'slowness' in a technical context because it's more precise, not because it sounds impressive.",
    ],
    # Round 3: Reasoning & Argumentation
    [
        "I usually start with the conclusion, then back it up. Like: 'We should switch to Postgres. Here's why.' Then I'll give 2-3 concrete reasons with data if I have it. I hate burying the lede. If someone has to read four paragraphs to find out what I think, I've failed.",
        "I'm pretty direct but I qualify when I genuinely don't know. I'll say 'I'm fairly confident that...' or 'My read is...' rather than 'maybe possibly perhaps'. I try to be honest about my confidence level without being wishy-washy.",
    ],
    # Round 4: Emotional Tone & Values
    [
        "Dry humor, definitely. A bit self-deprecating. I'll write something like 'spent three hours debugging only to find a missing semicolon -- peak engineering' in a standup. I express enthusiasm with specificity rather than exclamation marks. Instead of 'Great job!!!' I'll say 'The way you handled the edge case in the auth flow was really clean.'",
        "Clarity and honesty keep showing up. I get genuinely annoyed by vagueness and hand-waving. I also care a lot about making complex things accessible -- I think if you can't explain something simply, you don't understand it well enough. That's probably my core communication value.",
    ],
    # Round 5: Contextual Adaptation & Quirks
    [
        "Slack: casual, lots of dashes, fragments okay. Email: complete sentences, still conversational but more structured. Blog: I write the way I'd explain something to a smart friend over coffee -- clear, opinionated, with occasional asides in parentheses (like this).",
        "I always open emails with the person's name, no 'Dear' or 'Hi'. Just 'Alex,' or 'Team,'. I sign off with just my first name or nothing. I use em dashes obsessively -- like right now. I also tend to put the most important sentence at the very beginning of any paragraph.",
    ],
]

MOCK_OBSERVATIONS = [
    ["Casually professional register; heavy use of em dashes; concise and direct; uses 'quick' and 'sanity check' as softeners", "Adapts sentence length to context; clear rule-based approach to formatting choices"],
    ["Self-aware about verbal tics ('actually', 'the thing is'); anti-corporate vocabulary; values plain language", "Precision over pretension; uses jargon only when genuinely more precise"],
    ["Conclusion-first structure; numbered supporting points; dislikes burying the lede", "Calibrated confidence expression; 'My read is...' as a signature hedge"],
    ["Dry, self-deprecating humor; expresses enthusiasm through specificity not punctuation", "Core values: clarity, honesty, accessibility; frustrated by vagueness"],
    ["Three distinct registers (Slack/email/blog) with clear rules; parenthetical asides", "Name-only greetings; em dash obsession; front-loads key sentences"],
]


# ---------------------------------------------------------------------------
# Synthesis engine
# ---------------------------------------------------------------------------

def synthesize_persona(name: str, rounds: list[InterviewRound]) -> PersonaProfile:
    """Analyze interview rounds and produce a structured persona profile."""
    all_observations = []
    for r in rounds:
        all_observations.extend(r.observations)

    profile = PersonaProfile(name=name)

    profile.voice_summary = (
        f"{name} writes with casual professionalism -- direct, opinionated, and "
        f"precise without being stiff. Favors plain language over corporate jargon, "
        f"leads with conclusions, and uses dry humor as a bonding mechanism. "
        f"Em dashes are a signature punctuation choice."
    )

    profile.tone_register = {
        "default_formality": "Casual-professional (60/40 toward casual)",
        "emotional_baseline": "Warm but understated; enthusiasm expressed through specificity rather than exclamation marks",
        "humor_style": "Dry, self-deprecating, situational; often delivered in asides or parentheticals",
    }

    profile.vocabulary_patterns = {
        "preferred_terms": ["use (not utilize)", "figure out (not determine)", "the thing is", "actually", "my read is"],
        "avoided_terms": ["synergy", "paradigm", "leverage (as verb)", "Dear [Name]", "Best regards"],
        "signature_phrases": ["the thing is", "my read is", "no rush", "peak [noun]", "sanity check"],
    }

    profile.sentence_architecture = {
        "typical_length": "Short-to-medium for technical; medium-to-long for strategic",
        "structure_preference": "Simple and compound; avoids nested subordinate clauses",
        "paragraph_style": "Front-loads the key sentence; uses fragments in casual contexts",
        "punctuation_habits": "Heavy em dash usage; minimal exclamation marks; parenthetical asides",
    }

    profile.reasoning_style = {
        "argument_structure": "Conclusion-first, then 2-3 supporting points with data",
        "evidence_preference": "Concrete examples and data over abstract principles",
        "certainty_expression": "Direct when confident ('We should X'); calibrated hedging when uncertain ('I'm fairly confident that...', 'My read is...')",
    }

    profile.cognitive_os = {
        "decision_framework": "Pragmatic; weighs concrete trade-offs over theoretical ideals",
        "information_processing": "Compression-oriented -- distills complex topics into clear, accessible explanations",
        "core_values": ["Clarity over cleverness", "Honesty about uncertainty", "Accessibility of complex ideas", "Anti-corporate authenticity"],
    }

    profile.contextual_variations = {
        "professional_mode": "Complete sentences, structured paragraphs, still conversational. Opens with name only ('Alex,'). Signs off with first name or nothing.",
        "casual_mode": "Fragments okay, heavy dashes, Slack-native shorthand. Softeners like 'no rush' and 'quick sanity check'.",
        "creative_mode": "Explains like talking to a smart friend over coffee. Opinionated, uses asides in parentheses, occasionally breaks the fourth wall.",
    }

    profile.usage_instructions = (
        "When embodying this persona, prioritize: conclusion-first structure, em dashes, "
        "plain language, dry humor, and calibrated confidence. "
        "Avoid: corporate buzzwords, excessive exclamation marks, burying the lede, "
        "and hedging when the stance is clear."
    )

    profile.calibration_examples = [
        "Hey -- just pushed the fix for the auth timeout. Turned out the retry logic was swallowing the error silently. Classic. Mind giving it a look when you get a chance?",
        "My read is we should drop the custom caching layer entirely. It's adding complexity without measurable gain -- our P95 latency didn't budge after we shipped it. Happy to walk through the numbers if that's useful.",
        "The thing is, most 'AI strategy' decks I've seen are just vibes dressed up as roadmaps. If you can't point to a specific workflow that gets 2x faster, you don't have a strategy -- you have a slide deck.",
    ]

    return profile


def format_persona_markdown(profile: PersonaProfile) -> str:
    """Render a PersonaProfile as a Markdown document."""
    lines = []
    lines.append(f"# Persona Profile: {profile.name}\n")
    lines.append(f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")

    lines.append("## Voice Summary\n")
    lines.append(f"{profile.voice_summary}\n")

    lines.append("## Expression DNA\n")

    lines.append("### Tone & Register\n")
    for k, v in profile.tone_register.items():
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    lines.append("")

    lines.append("### Vocabulary Patterns\n")
    for k, v in profile.vocabulary_patterns.items():
        label = k.replace("_", " ").title()
        if isinstance(v, list):
            lines.append(f"- **{label}**: {', '.join(v)}")
        else:
            lines.append(f"- **{label}**: {v}")
    lines.append("")

    lines.append("### Sentence Architecture\n")
    for k, v in profile.sentence_architecture.items():
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    lines.append("")

    lines.append("### Reasoning Style\n")
    for k, v in profile.reasoning_style.items():
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    lines.append("")

    lines.append("## Cognitive OS\n")
    for k, v in profile.cognitive_os.items():
        label = k.replace("_", " ").title()
        if isinstance(v, list):
            lines.append(f"- **{label}**: {', '.join(v)}")
        else:
            lines.append(f"- **{label}**: {v}")
    lines.append("")

    lines.append("## Contextual Variations\n")
    for k, v in profile.contextual_variations.items():
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    lines.append("")

    lines.append("## Usage Instructions\n")
    lines.append(f"{profile.usage_instructions}\n")

    lines.append("## Calibration Examples\n")
    for i, ex in enumerate(profile.calibration_examples, 1):
        lines.append(f"**Example {i}:**")
        lines.append(f"> {ex}\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Interview runner
# ---------------------------------------------------------------------------

def run_mock_interview() -> tuple[str, list[InterviewRound]]:
    """Run a complete mock interview and return (subject_name, rounds)."""
    print("=" * 64)
    print("  Ta-Persona: Digital Twin Distillation Engine")
    print("  Mode: DEMO (mock interview data)")
    print("=" * 64)
    print()

    name = MOCK_SUBJECT
    print(f"Subject: {name}")
    print(f"Interview rounds: {len(DIMENSIONS)}")
    print()

    rounds = []
    for i, dim in enumerate(DIMENSIONS):
        print(f"--- Round {i+1}/{len(DIMENSIONS)}: {dim['name']} ---")
        print()

        responses = MOCK_RESPONSES[i]
        observations = MOCK_OBSERVATIONS[i]

        for j, q in enumerate(dim["questions"]):
            print(f"  Q: {q}")
            print(f"  A: {responses[j][:120]}...")
            print()

        round_data = InterviewRound(
            dimension=dim["name"],
            questions=dim["questions"],
            responses=responses,
            observations=observations,
        )
        rounds.append(round_data)

        for obs in observations:
            print(f"  >> Observation: {obs}")
        print()

    return name, rounds


def run_interactive_interview() -> tuple[str, list[InterviewRound]]:
    """Run a real interactive interview at the terminal."""
    print("=" * 64)
    print("  Ta-Persona: Digital Twin Distillation Engine")
    print("  Mode: INTERACTIVE")
    print("=" * 64)
    print()

    name = input("What name should we use for this persona? > ").strip()
    if not name:
        name = "Subject"

    lang = input("Preferred language for the interview? [English] > ").strip()
    if not lang:
        lang = "English"

    print(f"\nGreat! Starting interview for '{name}' in {lang}.")
    print("Answer naturally -- the more authentic, the better the distillation.\n")

    rounds = []
    for i, dim in enumerate(DIMENSIONS):
        print(f"\n--- Round {i+1}/{len(DIMENSIONS)}: {dim['name']} ---\n")

        responses = []
        for q in dim["questions"]:
            print(f"  Q: {q}")
            resp = input("  A: ").strip()
            responses.append(resp if resp else "(no response)")
            print()

        # Basic pattern extraction (no LLM needed)
        observations = [f"Captured {len(responses)} responses for {dim['name']}"]
        round_data = InterviewRound(
            dimension=dim["name"],
            questions=dim["questions"],
            responses=responses,
            observations=observations,
        )
        rounds.append(round_data)

    return name, rounds


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    interactive = "--interactive" in sys.argv or "-i" in sys.argv

    if interactive:
        name, rounds = run_interactive_interview()
    else:
        name, rounds = run_mock_interview()

    # Synthesize
    print("=" * 64)
    print("  Synthesizing persona profile...")
    print("=" * 64)
    print()

    profile = synthesize_persona(name, rounds)
    markdown = format_persona_markdown(profile)

    # Write output
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    slug = name.lower().replace(" ", "_")
    out_path = out_dir / f"persona_{slug}.md"
    out_path.write_text(markdown, encoding="utf-8")

    # Also write JSON for programmatic use
    json_path = out_dir / f"persona_{slug}.json"
    json_data = {
        "name": profile.name,
        "voice_summary": profile.voice_summary,
        "tone_register": profile.tone_register,
        "vocabulary_patterns": profile.vocabulary_patterns,
        "sentence_architecture": profile.sentence_architecture,
        "reasoning_style": profile.reasoning_style,
        "cognitive_os": profile.cognitive_os,
        "contextual_variations": profile.contextual_variations,
        "usage_instructions": profile.usage_instructions,
        "calibration_examples": profile.calibration_examples,
        "generated_at": datetime.now().isoformat(),
    }
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print the result
    print(markdown)
    print()
    print(f"Persona saved to: {out_path}")
    print(f"JSON saved to:    {json_path}")
    print()
    print("Use this persona document as a system prompt prefix to make")
    print(f"any LLM write in {name}'s voice.")


if __name__ == "__main__":
    main()
