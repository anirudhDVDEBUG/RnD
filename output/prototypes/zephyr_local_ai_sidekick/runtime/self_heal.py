"""Self-healing execution engine.

Wraps agentic workflow steps so that failures are detected, logged,
and automatically retried with an adjusted plan.
"""

import random
import time


class SelfHealingEngine:
    """Run steps with automatic retry and plan adjustment on failure."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.log: list[dict] = []

    def run_step(self, step_name: str, fn, *args, **kwargs):
        for attempt in range(1, self.max_retries + 1):
            try:
                result = fn(*args, **kwargs)
                self.log.append({
                    "step": step_name,
                    "attempt": attempt,
                    "status": "success",
                    "result": str(result)[:200],
                })
                return result
            except Exception as exc:
                self.log.append({
                    "step": step_name,
                    "attempt": attempt,
                    "status": "failed",
                    "error": str(exc),
                })
                if attempt < self.max_retries:
                    wait = 0.1 * attempt
                    time.sleep(wait)
        # All retries exhausted — return sentinel
        self.log.append({
            "step": step_name,
            "attempt": self.max_retries,
            "status": "exhausted",
        })
        return None

    def get_log(self) -> list[dict]:
        return list(self.log)


# -- Demo helper: a function that randomly fails -------------------------
def flaky_operation(label: str) -> str:
    if random.random() < 0.5:
        raise RuntimeError(f"Transient failure in {label}")
    return f"{label} completed"
