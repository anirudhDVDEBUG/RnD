"""
Task router: classifies tasks and routes them to the appropriate model.

Frontend patterns → Gemini
Backend patterns  → Codex
Ambiguous/general → Claude (orchestrator fallback)
"""

import re
from dataclasses import dataclass, field
from typing import Literal

ModelName = Literal["gemini", "codex", "claude"]
QualityTier = Literal["draft", "standard", "production"]

FRONTEND_SIGNALS = [
    r"\b(react|vue|svelte|angular|next\.?js|nuxt)\b",
    r"\b(css|scss|sass|tailwind|styled|html|jsx|tsx)\b",
    r"\b(component|ui|layout|page|widget|modal|dialog|tooltip)\b",
    r"\b(button|form|input|dropdown|navbar|sidebar|card|grid)\b",
    r"\b(animation|transition|responsive|mobile|viewport)\b",
    r"\b(dom|canvas|svg|webgl|browser)\b",
    r"\bfront.?end\b",
]

BACKEND_SIGNALS = [
    r"\b(api|rest|graphql|grpc|endpoint|route|controller)\b",
    r"\b(database|sql|postgres|mysql|mongo|redis|prisma|orm)\b",
    r"\b(server|express|fastapi|django|flask|node\.?js)\b",
    r"\b(auth|jwt|oauth|session|middleware|cors)\b",
    r"\b(docker|kubernetes|k8s|deploy|ci.?cd|terraform)\b",
    r"\b(queue|worker|cron|migration|seed|schema)\b",
    r"\bback.?end\b",
]

QUALITY_CONFIGS = {
    "draft": {"max_iterations": 1, "run_tests": False, "review": False, "description": "Fast iteration, minimal review"},
    "standard": {"max_iterations": 2, "run_tests": True, "review": False, "description": "Balanced speed and quality"},
    "production": {"max_iterations": 3, "run_tests": True, "review": True, "description": "Full review, testing, validation"},
}


@dataclass
class RoutingResult:
    task: str
    model: ModelName
    confidence: float
    frontend_score: int
    backend_score: int
    matched_signals: list[str] = field(default_factory=list)
    quality_tier: QualityTier = "standard"


def _count_matches(text: str, patterns: list[str]) -> tuple[int, list[str]]:
    text_lower = text.lower()
    score = 0
    matched = []
    for pattern in patterns:
        hits = re.findall(pattern, text_lower, re.IGNORECASE)
        if hits:
            score += len(hits)
            matched.append(f"{pattern} ({len(hits)}x)")
    return score, matched


def route_task(task: str, quality_tier: QualityTier = "standard") -> RoutingResult:
    """Classify a task description and return the optimal model routing."""
    fe_score, fe_matched = _count_matches(task, FRONTEND_SIGNALS)
    be_score, be_matched = _count_matches(task, BACKEND_SIGNALS)

    total = fe_score + be_score
    if total == 0:
        model: ModelName = "claude"
        confidence = 0.5
        matched = []
    elif fe_score > be_score:
        model = "gemini"
        confidence = min(0.95, 0.6 + (fe_score - be_score) / max(total, 1) * 0.4)
        matched = fe_matched
    elif be_score > fe_score:
        model = "codex"
        confidence = min(0.95, 0.6 + (be_score - fe_score) / max(total, 1) * 0.4)
        matched = be_matched
    else:
        model = "claude"
        confidence = 0.55
        matched = fe_matched + be_matched

    return RoutingResult(
        task=task,
        model=model,
        confidence=round(confidence, 2),
        frontend_score=fe_score,
        backend_score=be_score,
        matched_signals=matched,
        quality_tier=quality_tier,
    )
