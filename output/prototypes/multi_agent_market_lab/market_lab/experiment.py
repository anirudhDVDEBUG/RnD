"""Experiment tracking for multi-agent research runs."""
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ExperimentStatus(Enum):
    PLANNED = "planned"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Experiment:
    """A research experiment with hypothesis, parameters, and results."""
    name: str
    hypothesis: str
    parameters: dict = field(default_factory=dict)
    success_metrics: dict = field(default_factory=dict)
    status: ExperimentStatus = ExperimentStatus.PLANNED
    results: list = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    iteration_limit: int = 10

    def start(self):
        self.status = ExperimentStatus.RUNNING
        self.start_time = time.time()

    def complete(self, outcome: dict):
        self.status = ExperimentStatus.COMPLETED
        self.end_time = time.time()
        self.results.append(outcome)

    def record_iteration(self, data: dict):
        self.results.append({"iteration": len(self.results) + 1, "timestamp": time.time(), **data})

    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time if self.start_time else 0.0

    def evaluate(self) -> dict[str, Any]:
        """Evaluate experiment against success metrics."""
        evaluation = {}
        for metric, threshold in self.success_metrics.items():
            if metric == "min_signals":
                total = sum(r.get("signals_found", 0) for r in self.results)
                evaluation[metric] = {"target": threshold, "actual": total, "passed": total >= threshold}
            elif metric == "min_confidence":
                confidences = [r.get("avg_confidence", 0) for r in self.results if "avg_confidence" in r]
                avg = sum(confidences) / len(confidences) if confidences else 0
                evaluation[metric] = {"target": threshold, "actual": round(avg, 3), "passed": avg >= threshold}
        return evaluation


class ExperimentTracker:
    """Manages multiple experiments and their lifecycle."""

    def __init__(self):
        self.experiments: dict[str, Experiment] = {}

    def create(self, name: str, hypothesis: str, **kwargs) -> Experiment:
        exp = Experiment(name=name, hypothesis=hypothesis, **kwargs)
        self.experiments[name] = exp
        return exp

    def get(self, name: str) -> Experiment:
        return self.experiments[name]

    def list_active(self) -> list[Experiment]:
        return [e for e in self.experiments.values() if e.status == ExperimentStatus.RUNNING]

    def summary(self) -> dict:
        return {
            "total": len(self.experiments),
            "running": len([e for e in self.experiments.values() if e.status == ExperimentStatus.RUNNING]),
            "completed": len([e for e in self.experiments.values() if e.status == ExperimentStatus.COMPLETED]),
            "experiments": {name: e.status.value for name, e in self.experiments.items()},
        }
