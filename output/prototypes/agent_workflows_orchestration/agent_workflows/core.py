"""Core runtime: Workflow, Step, Adapter, and FakeAdapter."""

from __future__ import annotations

import json
import os
import sqlite3
import textwrap
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Adapter base + fake adapter
# ---------------------------------------------------------------------------

class Adapter:
    """Base class for LLM adapters."""

    def call(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement call()")


class FakeAdapter(Adapter):
    """Deterministic offline adapter — no API keys needed."""

    def call(self, prompt: str) -> str:
        summary = prompt[:80].replace("\n", " ")
        return (
            f"[FakeAdapter] Simulated response for: {summary}…\n"
            f"Lorem ipsum result with {len(prompt)} chars of input processed."
        )


# ---------------------------------------------------------------------------
# Step
# ---------------------------------------------------------------------------

@dataclass
class Step:
    prompt: str
    name: Optional[str] = None
    result: Optional[str] = None
    status: str = "pending"  # pending | running | done | failed
    cost_usd: float = 0.0
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def run(self, adapter: Adapter) -> str:
        self.status = "running"
        self.result = adapter.call(self.prompt)
        self.cost_usd = 0.002  # simulated cost per call
        self.status = "done"
        return self.result


# ---------------------------------------------------------------------------
# Journal (SQLite)
# ---------------------------------------------------------------------------

class Journal:
    """Durable SQLite run journal for resume support."""

    def __init__(self, db_path: str = "owf_journal.sqlite"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS runs ("
            "  run_id TEXT PRIMARY KEY,"
            "  workflow TEXT,"
            "  started_at TEXT,"
            "  status TEXT,"
            "  total_cost REAL DEFAULT 0"
            ")"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS steps ("
            "  step_id TEXT PRIMARY KEY,"
            "  run_id TEXT,"
            "  name TEXT,"
            "  prompt TEXT,"
            "  result TEXT,"
            "  status TEXT,"
            "  cost REAL DEFAULT 0,"
            "  FOREIGN KEY(run_id) REFERENCES runs(run_id)"
            ")"
        )
        self.conn.commit()

    def new_run(self, workflow_name: str) -> str:
        run_id = uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO runs VALUES (?, ?, datetime('now'), 'running', 0)",
            (run_id, workflow_name),
        )
        self.conn.commit()
        return run_id

    def log_step(self, run_id: str, step: Step):
        self.conn.execute(
            "INSERT OR REPLACE INTO steps VALUES (?, ?, ?, ?, ?, ?, ?)",
            (step.step_id, run_id, step.name or step.step_id,
             step.prompt, step.result, step.status, step.cost_usd),
        )
        self.conn.commit()

    def finish_run(self, run_id: str, status: str, total_cost: float):
        self.conn.execute(
            "UPDATE runs SET status=?, total_cost=? WHERE run_id=?",
            (status, total_cost, run_id),
        )
        self.conn.commit()

    def list_runs(self) -> List[Dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT run_id, workflow, started_at, status, total_cost FROM runs "
            "ORDER BY started_at DESC"
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def get_completed_step_ids(self, run_id: str) -> set:
        cur = self.conn.execute(
            "SELECT step_id FROM steps WHERE run_id=? AND status='done'",
            (run_id,),
        )
        return {row[0] for row in cur.fetchall()}


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

class Workflow:
    """Orchestrator: fan-out, pipeline, validate, budget, resume."""

    def __init__(self, name: str = "workflow", journal_path: str = "owf_journal.sqlite"):
        self.name = name
        self.steps: List[Step] = []
        self.journal = Journal(journal_path)
        self._budget: Optional[float] = None
        self._total_cost: float = 0.0
        self._adapter: Optional[Adapter] = None

    # -- building blocks ---------------------------------------------------

    def fan_out(
        self,
        prompt: str,
        topics: List[str],
        adapter: str = "fake",
    ) -> List[Step]:
        """Create parallel steps by expanding {topic} in the prompt."""
        steps = []
        for topic in topics:
            s = Step(prompt=prompt.replace("{topic}", topic), name=f"fan-out:{topic}")
            self.steps.append(s)
            steps.append(s)
        return steps

    def pipeline(self, steps: List[Step], then: Step) -> Step:
        """Chain: run *steps* first, feed concatenated results into *then*."""
        then.name = then.name or "pipeline:aggregator"
        # Store predecessor references so run() executes in order
        then._predecessors = steps  # type: ignore[attr-defined]
        self.steps.append(then)
        return then

    def validate(self, step: Step, schema: Dict[str, Any]) -> None:
        """Attach a validation schema to a step (checked after execution)."""
        step._schema = schema  # type: ignore[attr-defined]

    # -- execution ---------------------------------------------------------

    def run(
        self,
        budget: Optional[float] = None,
        adapter: Any = None,
        resume_run_id: Optional[str] = None,
    ) -> str:
        self._budget = budget

        # Resolve adapter
        if adapter is None or adapter == "fake":
            self._adapter = FakeAdapter()
        elif isinstance(adapter, str):
            self._adapter = FakeAdapter()  # fallback for demo
        elif isinstance(adapter, Adapter):
            self._adapter = adapter
        else:
            self._adapter = FakeAdapter()

        # Journal
        if resume_run_id:
            run_id = resume_run_id
            done_ids = self.journal.get_completed_step_ids(run_id)
            print(f"  Resuming run {run_id} — {len(done_ids)} steps already done")
        else:
            run_id = self.journal.new_run(self.name)
            done_ids = set()

        print(f"  Run ID : {run_id}")
        print(f"  Steps  : {len(self.steps)}")
        if budget:
            print(f"  Budget : ${budget:.2f}")
        print()

        for step in self.steps:
            if step.step_id in done_ids:
                print(f"  [skip] {step.name} (already done)")
                continue

            # Budget guard
            if self._budget and self._total_cost >= self._budget:
                print(f"  [budget] ${self._total_cost:.4f} >= ${self._budget:.2f} — pausing")
                self.journal.finish_run(run_id, "paused:budget", self._total_cost)
                return run_id

            # Execute predecessors' results into prompt if pipeline step
            preds = getattr(step, "_predecessors", None)
            if preds:
                combined = "\n---\n".join(p.result or "" for p in preds)
                step.prompt = f"{step.prompt}\n\nInput:\n{combined}"

            print(f"  [run]  {step.name}")
            step.run(self._adapter)
            self._total_cost += step.cost_usd
            self.journal.log_step(run_id, step)

            # Validate
            schema = getattr(step, "_schema", None)
            if schema:
                min_len = schema.get("minLength", 0)
                if step.result and len(step.result) >= min_len:
                    print(f"  [pass] validation (len={len(step.result)} >= {min_len})")
                else:
                    print(f"  [FAIL] validation (len={len(step.result or '')} < {min_len})")
                    step.status = "failed"
                    self.journal.log_step(run_id, step)

        self.journal.finish_run(run_id, "completed", self._total_cost)
        print(f"\n  Total cost: ${self._total_cost:.4f}")
        return run_id
