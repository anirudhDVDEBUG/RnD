#!/usr/bin/env python3
"""
Yang Tao Perspective — Cognitive Distillation Engine

Applies Yang Tao's entrepreneurial thinking frameworks to business scenarios.
Runs entirely offline with no API keys or external dependencies.
"""

import sys
import textwrap
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

FRAMEWORKS = {
    "accumulation": {
        "name": "Accumulation Thinking (做有积累的事)",
        "description": "Does this work compound over time?",
        "keywords": ["build", "long-term", "compound", "content", "course", "community",
                     "newsletter", "audience", "brand", "ip", "writing", "teach"],
        "questions": [
            "Will this asset grow in value if you do nothing for 6 months?",
            "Can each unit of work serve multiple future customers?",
            "Are you building on owned platforms or rented ones?",
        ],
        "principle": "Reject work that resets to zero each month. Prioritize assets that appreciate.",
    },
    "trust_currency": {
        "name": "Trust as Currency (信任即货币)",
        "description": "How does this build or spend trust?",
        "keywords": ["monetize", "sell", "paid", "charge", "price", "community",
                     "followers", "audience", "customers", "convert", "launch"],
        "questions": [
            "How many trust deposits have you made before this withdrawal?",
            "Would your audience recommend you to a friend right now?",
            "Is your price proportional to the trust you've accumulated?",
        ],
        "principle": "Never withdraw more trust than you've deposited. Price is a trust thermometer.",
    },
    "content_pipeline": {
        "name": "Content-to-Business Pipeline (内容变现管道)",
        "description": "How does content become revenue?",
        "keywords": ["content", "write", "video", "post", "social", "media",
                     "newsletter", "blog", "youtube", "twitter", "tiktok", "douyin"],
        "questions": [
            "What's your content → trust → product → revenue chain?",
            "Which stage is the bottleneck right now?",
            "Are you creating content that filters for buyers or just viewers?",
        ],
        "principle": "Content without a pipeline is a hobby. Map every post to a business outcome.",
    },
    "grassroots_path": {
        "name": "Grassroots Entrepreneurship (平民创业路径)",
        "description": "Can this start with zero capital and low risk?",
        "keywords": ["start", "bootstrap", "side", "hustle", "freelance", "solo",
                     "quit", "job", "capital", "investment", "risk", "money"],
        "questions": [
            "Can you validate this in 7 days with <$100?",
            "What's the smallest version that generates $1 of revenue?",
            "Does this require permission from anyone to start?",
        ],
        "principle": "The best businesses start embarrassingly small. Find your $1 before your $1M.",
    },
    "cognitive_leverage": {
        "name": "Cognitive Leverage (认知杠杆)",
        "description": "Where does a thinking shift create outsized results?",
        "keywords": ["strategy", "approach", "framework", "think", "perspective",
                     "opportunity", "niche", "market", "position", "differentiate"],
        "questions": [
            "What does everyone else believe that's wrong here?",
            "What would change if you 10x'd the price?",
            "Who's already proven this model in an adjacent market?",
        ],
        "principle": "The biggest ROI comes from thinking differently, not working harder.",
    },
}


@dataclass
class FrameworkResult:
    name: str
    relevance_score: float
    questions: List[str]
    principle: str
    description: str


@dataclass
class Analysis:
    input_text: str
    sharp_insight: str
    frameworks: List[FrameworkResult]
    action_steps: List[str]


class YangTaoEngine:
    """Applies Yang Tao's cognitive frameworks to a business scenario."""

    def analyze(self, scenario: str) -> Analysis:
        scenario_lower = scenario.lower()
        matched = self._match_frameworks(scenario_lower)
        insight = self._generate_insight(scenario_lower, matched)
        actions = self._generate_actions(scenario_lower, matched)
        return Analysis(
            input_text=scenario,
            sharp_insight=insight,
            frameworks=matched,
            action_steps=actions,
        )

    def _match_frameworks(self, text: str) -> List[FrameworkResult]:
        results = []
        for key, fw in FRAMEWORKS.items():
            score = sum(1 for kw in fw["keywords"] if kw in text)
            relevance = min(score / 3.0, 1.0)
            if relevance > 0.0:
                results.append(FrameworkResult(
                    name=fw["name"],
                    relevance_score=round(relevance, 2),
                    questions=fw["questions"],
                    principle=fw["principle"],
                    description=fw["description"],
                ))
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:3] if results else [FrameworkResult(
            name=FRAMEWORKS["cognitive_leverage"]["name"],
            relevance_score=0.5,
            questions=FRAMEWORKS["cognitive_leverage"]["questions"],
            principle=FRAMEWORKS["cognitive_leverage"]["principle"],
            description=FRAMEWORKS["cognitive_leverage"]["description"],
        )]

    def _generate_insight(self, text: str, frameworks: List[FrameworkResult]) -> str:
        insights = {
            "Accumulation Thinking": (
                "You're asking 'how do I make money?' but the real question is "
                "'what am I building that makes money while I sleep?'"
            ),
            "Trust as Currency": (
                "Monetization isn't a strategy — it's a thermometer. "
                "If you have to 'convince' people to pay, you haven't earned enough trust yet."
            ),
            "Content-to-Business Pipeline": (
                "Content without a funnel is charity. Every post should either "
                "build trust, filter buyers, or deliver value to paying customers."
            ),
            "Grassroots Entrepreneurship": (
                "The gap between 'idea' and 'business' is exactly one paying customer. "
                "Find that customer before you build anything else."
            ),
            "Cognitive Leverage": (
                "Everyone's optimizing the same playbook. "
                "The real edge is finding the question nobody's asking."
            ),
        }
        top_framework = frameworks[0].name if frameworks else ""
        for key, insight in insights.items():
            if key in top_framework:
                return insight
        return insights["Cognitive Leverage"]

    def _generate_actions(self, text: str, frameworks: List[FrameworkResult]) -> List[str]:
        actions = []
        if any("Accumulation" in f.name for f in frameworks):
            actions.append("List your current assets that grow without daily input — if none, that's problem #1")
        if any("Trust" in f.name for f in frameworks):
            actions.append("Survey 10 of your most engaged followers: 'What would you pay $50 for?'")
        if any("Content" in f.name for f in frameworks):
            actions.append("Map your last 10 posts: which ones led to DMs, replies, or sales? Double down on that format")
        if any("Grassroots" in f.name for f in frameworks):
            actions.append("Define the smallest possible offer you can deliver this week for $1+")
        if any("Cognitive" in f.name for f in frameworks):
            actions.append("Find 3 people who've solved a similar problem in a different market — study their model")
        if not actions:
            actions = ["Write down your business in one sentence. If you can't, simplify until you can."]
        actions.append("Block 2 hours this week for execution, not planning")
        actions.append("Share your plan publicly for accountability — even to 1 person")
        return actions[:5]


def format_output(analysis: Analysis) -> str:
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("  YANG TAO PERSPECTIVE — COGNITIVE ANALYSIS")
    lines.append("  杨涛视角 · 认知蒸馏分析")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Scenario: {analysis.input_text}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  SHARP INSIGHT (锐利洞察)")
    lines.append("-" * 60)
    lines.append("")
    for line in textwrap.wrap(f'  "{analysis.sharp_insight}"', width=56):
        lines.append(f"  {line}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  FRAMEWORK ANALYSIS (框架分析)")
    lines.append("-" * 60)

    for i, fw in enumerate(analysis.frameworks, 1):
        lines.append("")
        bar = "█" * int(fw.relevance_score * 10) + "░" * (10 - int(fw.relevance_score * 10))
        lines.append(f"  {i}. {fw.name}")
        lines.append(f"     Relevance: [{bar}] {fw.relevance_score:.0%}")
        lines.append(f"     → {fw.description}")
        lines.append("")
        lines.append("     Key Questions:")
        for q in fw.questions:
            lines.append(f"       ? {q}")
        lines.append("")
        lines.append(f"     Principle: {fw.principle}")

    lines.append("")
    lines.append("-" * 60)
    lines.append("  IMMEDIATE ACTIONS (立即行动)")
    lines.append("-" * 60)
    lines.append("")
    for i, action in enumerate(analysis.action_steps, 1):
        lines.append(f"  [{i}] {action}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Core reminder: 行动大于思考 (Action over theory)")
    lines.append("=" * 60)
    lines.append("")
    return "\n".join(lines)


def main():
    scenarios = [
        "I want to monetize a newsletter about AI tools for freelancers",
        "How to build a personal brand as a solo developer with side projects",
        "I'm thinking of quitting my job to start a content business on social media",
    ]

    if len(sys.argv) > 1:
        scenarios = [" ".join(sys.argv[1:])]

    engine = YangTaoEngine()

    for scenario in scenarios:
        analysis = engine.analyze(scenario)
        print(format_output(analysis))


if __name__ == "__main__":
    main()
