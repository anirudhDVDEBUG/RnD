"""
ERPAVal Lessons Store — persistent compounding knowledge base that grows
with every completed development cycle.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


LESSONS_FILE = os.path.join(os.path.dirname(__file__), "lessons.json")


@dataclass
class Lesson:
    task: str
    category: str  # architecture, gotcha, testing, convention, pattern
    insight: str
    timestamp: str
    tags: List[str]


def load_lessons(path: Optional[str] = None) -> List[Lesson]:
    """Load all lessons from the store."""
    path = path or LESSONS_FILE
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = json.load(f)
    return [Lesson(**entry) for entry in data]


def save_lessons(lessons: List[Lesson], path: Optional[str] = None) -> None:
    """Persist the lessons list."""
    path = path or LESSONS_FILE
    with open(path, "w") as f:
        json.dump([asdict(l) for l in lessons], f, indent=2)


def add_lesson(task: str, category: str, insight: str,
               tags: Optional[List[str]] = None,
               path: Optional[str] = None) -> Lesson:
    """Add a new lesson and persist it."""
    lesson = Lesson(
        task=task,
        category=category,
        insight=insight,
        timestamp=datetime.now().isoformat(),
        tags=tags or [],
    )
    lessons = load_lessons(path)
    lessons.append(lesson)
    save_lessons(lessons, path)
    return lesson


def search_lessons(query: str, path: Optional[str] = None) -> List[Lesson]:
    """Search lessons by keyword match against insight and tags."""
    query_lower = query.lower()
    results = []
    for lesson in load_lessons(path):
        if (query_lower in lesson.insight.lower()
                or query_lower in lesson.task.lower()
                or any(query_lower in t.lower() for t in lesson.tags)):
            results.append(lesson)
    return results


def format_lessons(lessons: List[Lesson]) -> str:
    """Pretty-print lessons for display."""
    if not lessons:
        return "  (none)"
    lines = []
    for i, l in enumerate(lessons, 1):
        lines.append(f"  {i}. [{l.category}] {l.insight}")
        lines.append(f"     Task: {l.task} | Tags: {', '.join(l.tags)}")
    return "\n".join(lines)
