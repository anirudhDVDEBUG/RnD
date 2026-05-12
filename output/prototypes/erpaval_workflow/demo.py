#!/usr/bin/env python3
"""
ERPAVal Workflow Demo — runs three different task types through the
six-phase cycle to show classifier routing and lesson compounding.
"""

import os

from erpaval import ERPAValWorkflow
from lessons_store import load_lessons, format_lessons


DEMO_TASKS = [
    "Fix the login timeout bug that causes sessions to expire prematurely",
    "Add Stripe payment integration to the checkout flow",
    "Refactor the user service to decouple database access from business logic",
]


def main():
    # Use a temp file so the demo is self-contained and repeatable
    lessons_path = os.path.join(os.path.dirname(__file__), "_demo_lessons.json")

    # Clean slate
    if os.path.exists(lessons_path):
        os.remove(lessons_path)

    engine = ERPAValWorkflow(lessons_path=lessons_path)

    for i, task in enumerate(DEMO_TASKS, 1):
        print(f"\n{'#' * 64}")
        print(f"  Demo task {i} of {len(DEMO_TASKS)}")
        print(f"{'#' * 64}\n")
        engine.run(task)
        print()

    # Show compounded lessons
    lessons = load_lessons(lessons_path)
    print("\n" + "=" * 64)
    print("  Compounded Lessons Store (after all runs)")
    print("=" * 64)
    print(format_lessons(lessons))
    print()

    # Cleanup
    if os.path.exists(lessons_path):
        os.remove(lessons_path)


if __name__ == "__main__":
    main()
