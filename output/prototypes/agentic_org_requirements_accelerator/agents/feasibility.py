"""Technical Feasibility Agent: Estimate complexity and flag risks."""

from typing import Dict, List
from intake import Requirement

COMPLEXITY_KEYWORDS = {
    "XL": ["ai-powered", "machine learning", "recommendation", "behavior", "prediction"],
    "L": ["microservice", "concurrent", "encrypted", "payment", "gateway", "pipeline"],
    "M": ["dashboard", "analytics", "a/b test", "seo", "notification", "email"],
    "S": ["search", "filter", "category", "sort", "export"],
}

RISK_KEYWORDS = {
    "high": ["10,000 concurrent", "sub-200ms", "aes-256", "tls 1.3", "apple pay"],
    "medium": ["multiple payment", "real-time", "automated testing", "staged rollout"],
    "low": ["keyword", "category", "structured data", "csv"],
}

EFFORT_MAP = {"XL": "3-5 sprints", "L": "2-3 sprints", "M": "1-2 sprints", "S": "0.5-1 sprint"}
POINTS_MAP = {"XL": 21, "L": 13, "M": 8, "S": 5}


def _estimate_complexity(text: str) -> str:
    text_lower = text.lower()
    for size, keywords in COMPLEXITY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return size
    return "M"


def _assess_risk(text: str) -> str:
    text_lower = text.lower()
    for level, keywords in RISK_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return level
    return "low"


def run(requirements: List[Requirement]) -> List[Dict]:
    estimates = []
    for req in requirements:
        complexity = _estimate_complexity(req.text)
        risk = _assess_risk(req.text)
        estimates.append({
            "requirement_id": req.id,
            "text": req.text,
            "complexity": complexity,
            "effort": EFFORT_MAP[complexity],
            "story_points": POINTS_MAP[complexity],
            "risk_level": risk,
            "risk_notes": _risk_note(req, risk),
            "suggested_phase": _phase(req.priority, complexity),
        })
    return estimates


def _risk_note(req: Requirement, risk: str) -> str:
    if risk == "high":
        return f"Requires spike/PoC before commitment. Consider prototyping '{req.text[:50]}...' in isolation."
    elif risk == "medium":
        return "Standard complexity but involves third-party integration or performance tuning."
    return "Straightforward implementation with well-known patterns."


def _phase(priority: str, complexity: str) -> int:
    if priority == "critical":
        return 1
    if priority == "high" and complexity in ("S", "M"):
        return 1
    if priority == "high":
        return 2
    return 3
