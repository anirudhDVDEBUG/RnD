"""
Orchestrator: takes a list of tasks, routes each one, calls the model,
and collects results. Supports autonomous mode (run all without prompts).
"""

from dataclasses import dataclass, field
from .router import route_task, RoutingResult, QualityTier, QUALITY_CONFIGS
from .models import call_model, ModelResponse


@dataclass
class TaskResult:
    routing: RoutingResult
    response: ModelResponse


@dataclass
class WorkflowRun:
    quality_tier: QualityTier
    autonomous: bool
    results: list[TaskResult] = field(default_factory=list)
    total_tokens: int = 0
    total_latency_ms: int = 0

    @property
    def model_breakdown(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.results:
            m = r.routing.model
            counts[m] = counts.get(m, 0) + 1
        return counts


def run_workflow(
    tasks: list[str],
    quality_tier: QualityTier = "standard",
    autonomous: bool = False,
) -> WorkflowRun:
    """Execute the full multi-model workflow on a list of tasks."""
    run = WorkflowRun(quality_tier=quality_tier, autonomous=autonomous)

    for task in tasks:
        routing = route_task(task, quality_tier=quality_tier)
        response = call_model(routing.model, task, quality_tier=quality_tier)

        # In production quality tier, simulate a review pass
        config = QUALITY_CONFIGS[quality_tier]
        if config["review"]:
            review = call_model("claude", f"Review: {task}", quality_tier="draft")
            response.tokens_used += review.tokens_used
            response.latency_ms += review.latency_ms

        result = TaskResult(routing=routing, response=response)
        run.results.append(result)
        run.total_tokens += response.tokens_used
        run.total_latency_ms += response.latency_ms

    return run
