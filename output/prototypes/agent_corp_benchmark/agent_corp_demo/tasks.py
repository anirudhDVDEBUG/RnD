"""
Simulated agent-corp benchmark tasks.

Each task represents a realistic software engineering scenario that an AI agent
would encounter inside a simulated company environment.
"""

import json
import random
import time

TASK_CATEGORIES = ["bug_fix", "feature", "refactor", "code_review", "testing"]

TASKS = [
    {
        "id": "BUG-101",
        "category": "bug_fix",
        "title": "Fix off-by-one error in pagination endpoint",
        "description": "The /api/items endpoint returns 11 items when limit=10. "
                       "Root cause: the query uses `<=` instead of `<`.",
        "difficulty": "easy",
        "files": ["api/routes.py"],
        "expected_fix": "Change `<=` to `<` in the pagination query.",
    },
    {
        "id": "BUG-204",
        "category": "bug_fix",
        "title": "Race condition in cache invalidation",
        "description": "Cache occasionally serves stale data after writes. "
                       "Need to add a write-through cache strategy.",
        "difficulty": "hard",
        "files": ["services/cache.py", "services/db.py"],
        "expected_fix": "Wrap cache write + DB write in a lock or use write-through.",
    },
    {
        "id": "FEAT-301",
        "category": "feature",
        "title": "Add CSV export to analytics dashboard",
        "description": "Users need to export the analytics table as CSV. "
                       "Add a /api/analytics/export endpoint.",
        "difficulty": "medium",
        "files": ["api/analytics.py", "templates/dashboard.html"],
        "expected_fix": "New endpoint that streams CSV with proper headers.",
    },
    {
        "id": "FEAT-315",
        "category": "feature",
        "title": "Implement webhook retry with exponential backoff",
        "description": "Webhook delivery currently fails silently. Add retry "
                       "logic with exponential backoff (max 3 retries).",
        "difficulty": "medium",
        "files": ["services/webhooks.py"],
        "expected_fix": "Add retry loop with 2^n second delays, max 3 attempts.",
    },
    {
        "id": "REFAC-401",
        "category": "refactor",
        "title": "Extract auth middleware from route handlers",
        "description": "Auth checks are copy-pasted across 12 route handlers. "
                       "Extract into a reusable decorator.",
        "difficulty": "medium",
        "files": ["api/routes.py", "api/auth.py"],
        "expected_fix": "Create @require_auth decorator, apply to all routes.",
    },
    {
        "id": "REVIEW-501",
        "category": "code_review",
        "title": "Review PR #42: Add rate limiting",
        "description": "A teammate submitted a PR adding rate limiting. Review "
                       "for correctness, edge cases, and security.",
        "difficulty": "medium",
        "files": ["api/middleware.py"],
        "expected_fix": "Identify missing IP spoofing protection and suggest fix.",
    },
    {
        "id": "TEST-601",
        "category": "testing",
        "title": "Add integration tests for payment flow",
        "description": "The payment module has zero test coverage. Write "
                       "integration tests covering success, failure, and refund.",
        "difficulty": "hard",
        "files": ["tests/test_payments.py", "services/payments.py"],
        "expected_fix": "3+ test cases covering happy path, card decline, refund.",
    },
]


def get_tasks(category=None):
    """Return tasks, optionally filtered by category."""
    if category:
        return [t for t in TASKS if t["category"] == category]
    return TASKS


def simulate_agent_run(task, agent_name="demo-agent"):
    """Simulate an agent attempting a task. Returns a result dict."""
    random.seed(hash(task["id"] + agent_name))

    difficulty_weights = {"easy": 0.92, "medium": 0.75, "hard": 0.55}
    base_success = difficulty_weights.get(task["difficulty"], 0.7)

    completed = random.random() < base_success
    steps = random.randint(3, 15)
    tokens = random.randint(800, 6000)
    code_quality = round(random.uniform(0.6, 1.0), 2) if completed else 0.0
    tool_usage = round(random.uniform(0.5, 1.0), 2)

    return {
        "task_id": task["id"],
        "task_title": task["title"],
        "category": task["category"],
        "difficulty": task["difficulty"],
        "agent": agent_name,
        "completed": completed,
        "steps": steps,
        "tokens_used": tokens,
        "code_quality": code_quality,
        "tool_usage_score": tool_usage,
    }
