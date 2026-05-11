"""
Mock model backends. In production these would call real APIs.
For demo purposes they simulate latency and return plausible responses.
"""

import time
import random
from dataclasses import dataclass

MOCK_RESPONSES = {
    "gemini": [
        "Created React component with Tailwind styling and responsive breakpoints.",
        "Built interactive form with client-side validation and accessible labels.",
        "Implemented dashboard layout with CSS Grid and animated transitions.",
        "Added dark-mode toggle using CSS custom properties and React context.",
    ],
    "codex": [
        "Generated REST API endpoint with input validation and error handling.",
        "Created database migration with proper indexes and foreign keys.",
        "Implemented JWT auth middleware with refresh-token rotation.",
        "Built background worker with retry logic and dead-letter queue.",
    ],
    "claude": [
        "Analyzed the task, split it into frontend and backend subtasks.",
        "Wrote integration tests covering the full request lifecycle.",
        "Refactored shared types into a common package for both layers.",
        "Generated project documentation and architectural decision records.",
    ],
}


@dataclass
class ModelResponse:
    model: str
    output: str
    tokens_used: int
    latency_ms: int
    quality_tier: str


def call_model(model: str, task: str, quality_tier: str = "standard") -> ModelResponse:
    """Simulate a model call. Returns a mock response with realistic metadata."""
    tier_multiplier = {"draft": 0.5, "standard": 1.0, "production": 1.8}.get(quality_tier, 1.0)

    base_latency = {"gemini": 800, "codex": 1200, "claude": 600}.get(model, 1000)
    simulated_ms = int(base_latency * tier_multiplier * random.uniform(0.8, 1.2))

    # Simulate a brief pause for realism (capped at 0.3s for demo speed)
    time.sleep(min(0.3, simulated_ms / 5000))

    base_tokens = {"gemini": 450, "codex": 520, "claude": 380}.get(model, 400)
    tokens = int(base_tokens * tier_multiplier * random.uniform(0.9, 1.1))

    responses = MOCK_RESPONSES.get(model, MOCK_RESPONSES["claude"])
    output = random.choice(responses)

    return ModelResponse(
        model=model,
        output=output,
        tokens_used=tokens,
        latency_ms=simulated_ms,
        quality_tier=quality_tier,
    )
