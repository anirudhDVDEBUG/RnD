"""Decomposition Agent: Break requirements into atomic user stories."""

from typing import Dict, List
from intake import Requirement

# Keyword-based heuristics for splitting compound requirements
SPLIT_MARKERS = [" and ", ", and ", " with ", " including "]

ACCEPTANCE_TEMPLATES = {
    "search": [
        "Given a user on the search page, when they enter a keyword, then matching products are displayed within 500ms",
        "Search results can be filtered and sorted without page reload",
    ],
    "checkout": [
        "Given a user with items in cart, when they select a payment method, then the payment form loads correctly",
        "Order confirmation is displayed and emailed after successful payment",
    ],
    "dashboard": [
        "Given an admin user, when they log in, then the dashboard loads with real-time data",
        "Dashboard supports filtering by date range and export to CSV",
    ],
    "notification": [
        "Given a trigger event, when conditions are met, then notification is sent within 60 seconds",
        "Users can manage notification preferences from their account settings",
    ],
    "security": [
        "All API endpoints require authentication tokens",
        "Sensitive data is never logged or exposed in error messages",
    ],
    "performance": [
        "System maintains target response time under specified concurrent load",
        "Performance degradation triggers automated alerts",
    ],
    "default": [
        "Feature works as described in the requirement",
        "Edge cases are handled gracefully with appropriate error messages",
    ],
}


def _match_template(text: str) -> List[str]:
    text_lower = text.lower()
    for key, criteria in ACCEPTANCE_TEMPLATES.items():
        if key in text_lower:
            return criteria
    return ACCEPTANCE_TEMPLATES["default"]


def _split_requirement(req: Requirement) -> List[Dict]:
    """Split compound requirements into atomic stories."""
    stories = []
    parts = [req.text]
    for marker in SPLIT_MARKERS:
        new_parts = []
        for p in parts:
            new_parts.extend(p.split(marker))
        parts = [p.strip() for p in new_parts if p.strip()]

    for i, part in enumerate(parts):
        story_id = f"{req.id}-S{i+1}" if len(parts) > 1 else f"{req.id}-S1"
        stories.append({
            "story_id": story_id,
            "requirement_id": req.id,
            "title": f"As a user, I want {part[0].lower()}{part[1:]}" if part[0].isupper() else f"As a user, I want to {part}",
            "acceptance_criteria": _match_template(part),
            "source": req.source,
            "priority": req.priority,
            "domain": req.domain,
        })

    return stories


def run(requirements: List[Requirement]) -> List[Dict]:
    """Run decomposition agent on all requirements. Returns list of user stories."""
    all_stories = []
    for req in requirements:
        all_stories.extend(_split_requirement(req))
    return all_stories
