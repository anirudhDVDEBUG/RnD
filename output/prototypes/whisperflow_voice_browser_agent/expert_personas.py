"""Multi-persona expert routing: pick the right specialist for the task."""


PERSONAS = {
    "navigator": {
        "name": "Navigator",
        "description": "Specializes in URL routing, site discovery, and page navigation.",
        "keywords": ["go to", "open", "navigate", "visit", "back", "forward"],
    },
    "searcher": {
        "name": "Searcher",
        "description": "Expert at filling search forms and finding information.",
        "keywords": ["search", "find", "look up", "query", "google"],
    },
    "reader": {
        "name": "Reader",
        "description": "Extracts and summarizes visible page content.",
        "keywords": ["read", "summarize", "extract", "what does", "tell me"],
    },
    "interactor": {
        "name": "Interactor",
        "description": "Handles clicks, form fills, scrolling, and UI interactions.",
        "keywords": ["click", "scroll", "type", "fill", "select", "press", "submit"],
    },
    "analyst": {
        "name": "Analyst",
        "description": "Compares data, makes decisions, and provides recommendations.",
        "keywords": ["compare", "best", "recommend", "analyze", "which"],
    },
}


def route_to_expert(command: str) -> dict:
    """Pick the best persona for a given voice command."""
    cmd_lower = command.lower()
    scores: dict[str, int] = {}
    for key, persona in PERSONAS.items():
        score = sum(1 for kw in persona["keywords"] if kw in cmd_lower)
        scores[key] = score

    best = max(scores, key=scores.get)
    chosen = PERSONAS[best]
    print(f"[expert] Routing to: {chosen['name']} — {chosen['description']}")
    return chosen
