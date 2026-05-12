"""
ERPAVal Task Classifier — determines the best entry point and phase emphasis
for a given development task.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class TaskType(Enum):
    BUG_FIX = "bug_fix"
    NEW_FEATURE = "new_feature"
    REFACTOR = "refactor"
    SIMPLE_CHANGE = "simple_change"
    UNKNOWN = "unknown"


@dataclass
class Classification:
    task_type: TaskType
    confidence: float
    entry_phase: str
    emphasized_phases: List[str]
    reasoning: str


# Keyword-based classification rules
RULES = {
    TaskType.BUG_FIX: {
        "keywords": ["bug", "fix", "broken", "error", "crash", "fail", "issue",
                      "regression", "wrong", "incorrect", "not working", "timeout",
                      "exception", "traceback", "null", "undefined"],
        "entry_phase": "explore",
        "emphasized_phases": ["explore", "validate"],
    },
    TaskType.NEW_FEATURE: {
        "keywords": ["add", "new", "feature", "implement", "create", "build",
                      "introduce", "support", "enable", "integration"],
        "entry_phase": "explore",
        "emphasized_phases": ["research", "plan"],
    },
    TaskType.REFACTOR: {
        "keywords": ["refactor", "clean", "reorganize", "restructure", "optimize",
                      "simplify", "extract", "rename", "move", "decouple",
                      "performance", "speed up"],
        "entry_phase": "explore",
        "emphasized_phases": ["plan", "validate"],
    },
    TaskType.SIMPLE_CHANGE: {
        "keywords": ["update", "change", "modify", "tweak", "adjust", "bump",
                      "config", "typo", "text", "label", "color", "style"],
        "entry_phase": "explore",
        "emphasized_phases": ["validate"],
    },
}


def classify_task(description: str) -> Classification:
    """Classify a task description and return routing information."""
    desc_lower = description.lower()
    scores: Dict[TaskType, float] = {}

    for task_type, rule in RULES.items():
        hits = sum(1 for kw in rule["keywords"] if kw in desc_lower)
        scores[task_type] = hits / len(rule["keywords"])

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    if best_score < 0.05:
        best_type = TaskType.UNKNOWN
        rule = {
            "entry_phase": "explore",
            "emphasized_phases": ["explore", "research", "plan", "act", "validate", "compound"],
        }
        reasoning = "No strong signal detected; running full six-phase cycle."
    else:
        rule = RULES[best_type]
        reasoning = f"Detected {best_type.value} pattern (confidence {best_score:.0%})."

    return Classification(
        task_type=best_type,
        confidence=best_score,
        entry_phase=rule["entry_phase"],
        emphasized_phases=rule["emphasized_phases"],
        reasoning=reasoning,
    )
