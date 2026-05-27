"""Phase 3: Implementation Plan — ordered task list from architecture."""

from dataclasses import dataclass, field
from typing import List
from .architect import Architecture
from .spec import Spec


@dataclass
class Task:
    id: int
    component: str
    action: str
    requirements: List[str] = field(default_factory=list)
    status: str = "pending"  # pending | in_progress | done

    def mark_done(self):
        self.status = "done"


@dataclass
class Plan:
    tasks: List[Task] = field(default_factory=list)

    def next_task(self):
        for t in self.tasks:
            if t.status == "pending":
                return t
        return None

    def progress(self) -> dict:
        done = sum(1 for t in self.tasks if t.status == "done")
        return {
            "total": len(self.tasks),
            "done": done,
            "percent": round(100 * done / max(len(self.tasks), 1)),
        }

    def summary(self) -> str:
        prog = self.progress()
        lines = [f"Plan: {prog['total']} tasks ({prog['percent']}% complete)"]
        for t in self.tasks:
            marker = {"pending": "[ ]", "in_progress": "[~]", "done": "[x]"}[t.status]
            lines.append(f"  {marker} T{t.id}: {t.action} ({t.component})")
            if t.requirements:
                lines.append(f"       reqs: {', '.join(t.requirements)}")
        return "\n".join(lines)


def create_plan(spec: Spec, arch: Architecture) -> Plan:
    """Generate ordered implementation plan from architecture."""
    order = arch.dependency_order()
    tasks = []
    task_id = 1

    for comp_name in order:
        comp = next((c for c in arch.components if c.name == comp_name), None)
        if not comp:
            continue
        tasks.append(Task(
            id=task_id,
            component=comp.name,
            action=f"Implement {comp.name} ({comp.responsibility})",
            requirements=comp.requirements_covered[:],
        ))
        task_id += 1

    return Plan(tasks=tasks)
