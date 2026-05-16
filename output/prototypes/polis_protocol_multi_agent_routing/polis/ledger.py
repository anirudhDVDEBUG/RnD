"""Lessons ledger: append-only log of agent run outcomes."""
from __future__ import annotations
import json, os
from dataclasses import dataclass, asdict
from datetime import date
from typing import List, Optional

@dataclass
class LessonEntry:
    date: str
    task_type: str
    agent: str
    task_description: str
    outcome: str          # "success" | "partial" | "failure"
    reward: float         # 0.0 – 1.0
    lesson: str

class Ledger:
    def __init__(self, path: str):
        self.path = path
        self.entries: List[LessonEntry] = []
        if os.path.exists(path):
            self._load()

    def _load(self) -> None:
        with open(self.path) as f:
            data = json.load(f)
        self.entries = [LessonEntry(**e) for e in data]

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w") as f:
            json.dump([asdict(e) for e in self.entries], f, indent=2)

    def append(self, entry: LessonEntry) -> None:
        self.entries.append(entry)
        self.save()

    def replay_into(self, router) -> int:
        """Replay historical lessons into a bandit router to warm-start it."""
        for e in self.entries:
            router.update(e.task_type, e.agent, e.reward)
        return len(self.entries)

    def to_markdown(self) -> str:
        lines = ["# Lessons Ledger\n"]
        for e in self.entries:
            lines.append(f"## {e.date} - {e.task_description}")
            lines.append(f"- **Agent:** {e.agent}")
            lines.append(f"- **Task type:** {e.task_type}")
            lines.append(f"- **Outcome:** {e.outcome}")
            lines.append(f"- **Reward:** {e.reward:.2f}")
            lines.append(f"- **Lesson:** {e.lesson}")
            lines.append("")
        return "\n".join(lines)
