#!/usr/bin/env python3
"""
vibe_planner.py — Converts a natural-language feature request into a
structured vibe-coding plan following the 4-step methodology:
  1. Ground the Vibe (context)
  2. Describe Intent (not implementation)
  3. Iteration Plan (conversation steps)
  4. Validation Checklist (harden)

No API keys required — runs locally with pure heuristics.
"""

import re
import sys
import textwrap
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Keyword banks for heuristic analysis
# ---------------------------------------------------------------------------
STACK_HINTS = {
    "react": "React", "next": "Next.js", "nextjs": "Next.js",
    "vue": "Vue", "nuxt": "Nuxt", "svelte": "Svelte",
    "angular": "Angular", "express": "Express", "fastapi": "FastAPI",
    "flask": "Flask", "django": "Django", "rails": "Rails",
    "typescript": "TypeScript", "python": "Python", "rust": "Rust",
    "go": "Go", "tailwind": "Tailwind CSS", "prisma": "Prisma",
    "postgres": "PostgreSQL", "sqlite": "SQLite", "mongo": "MongoDB",
    "redis": "Redis", "graphql": "GraphQL", "rest": "REST API",
    "docker": "Docker", "aws": "AWS", "gcp": "GCP",
}

UI_KEYWORDS = {
    "button", "form", "modal", "dialog", "dropdown", "menu", "sidebar",
    "navbar", "header", "footer", "card", "table", "list", "grid",
    "search", "filter", "sort", "pagination", "tab", "toggle", "slider",
    "input", "textarea", "checkbox", "radio", "select", "tooltip",
    "toast", "notification", "badge", "avatar", "carousel", "chart",
    "dashboard", "layout", "page", "component", "widget",
}

BEHAVIOR_KEYWORDS = {
    "click", "hover", "submit", "load", "scroll", "drag", "drop",
    "type", "focus", "blur", "change", "select", "resize", "animate",
    "fetch", "send", "receive", "store", "cache", "debounce", "throttle",
    "validate", "authenticate", "authorize", "redirect", "navigate",
    "upload", "download", "stream", "poll", "webhook",
}

EDGE_CASE_SIGNALS = {
    "error", "fail", "empty", "null", "undefined", "timeout", "slow",
    "offline", "no results", "loading", "retry", "fallback", "invalid",
    "duplicate", "overflow", "limit", "permission", "denied", "expired",
    "conflict", "race condition",
}


@dataclass
class VibePlan:
    feature_name: str = ""
    detected_stack: list = field(default_factory=list)
    ui_elements: list = field(default_factory=list)
    behaviors: list = field(default_factory=list)
    edge_cases: list = field(default_factory=list)
    iteration_steps: list = field(default_factory=list)
    validation_items: list = field(default_factory=list)


def extract_feature_name(text: str) -> str:
    """Pull a concise feature name from the request."""
    # Try to find quoted names first
    quoted = re.findall(r'["\']([^"\']+)["\']', text)
    if quoted:
        return quoted[0]
    # Try "a/an <noun>" pattern
    match = re.search(r'\b(?:build|create|add|make|implement|need)\s+(?:a|an|the)\s+(.+?)(?:\.|,|that|which|with|for|\n|$)', text, re.I)
    if match:
        name = match.group(1).strip()
        return name[:60] if len(name) > 60 else name
    # Fallback: first sentence
    first = text.split(".")[0].strip()
    return first[:60] if len(first) > 60 else first


def detect_keywords(text: str, keyword_set) -> list:
    """Find which keywords from a set appear in the text."""
    lower = text.lower()
    found = []
    for kw in sorted(keyword_set):
        if isinstance(keyword_set, dict):
            if kw in lower:
                found.append(keyword_set[kw])
        else:
            if kw in lower:
                found.append(kw)
    return found


def generate_iteration_steps(plan: VibePlan) -> list:
    """Build a recommended iteration sequence."""
    steps = []
    if plan.detected_stack:
        steps.append(f"Ground context: state stack as {', '.join(plan.detected_stack)}")
    else:
        steps.append("Ground context: specify your tech stack and point to existing patterns")

    if plan.ui_elements:
        steps.append(f"Describe the UI: request {', '.join(plan.ui_elements[:4])} components")
    steps.append(f"Describe the core behavior: '{plan.feature_name}'")

    if plan.behaviors:
        steps.append(f"Specify interactions: {', '.join(plan.behaviors[:5])}")
    else:
        steps.append("Specify interactions: describe what happens on user actions")

    steps.append("Review first output — steer with directional feedback, don't rewrite")
    steps.append("Commit the working increment before requesting changes")

    if plan.edge_cases:
        steps.append(f"Handle edge cases: {', '.join(plan.edge_cases[:4])}")
    else:
        steps.append("Ask: 'What happens on error, empty state, or slow network?'")

    steps.append("Request tests covering happy path, edge cases, and error states")
    steps.append("Ask agent to self-review for security, performance, and a11y")
    return steps


def generate_validation_checklist(plan: VibePlan) -> list:
    """Build the validation/hardening checklist."""
    items = [
        "Feature works for the primary use case (happy path)",
        "Code follows existing project patterns and conventions",
    ]
    if plan.ui_elements:
        items.append("UI components are accessible (keyboard nav, screen reader, contrast)")
    if plan.behaviors:
        items.append("User interactions behave as described")
    items.append("Error states handled gracefully (loading, empty, failure)")
    items.append("No security vulnerabilities (XSS, injection, auth bypass)")
    items.append("Tests written and passing")
    items.append("Code committed at working checkpoint")
    return items


def analyze(text: str) -> VibePlan:
    """Analyze a feature request and produce a structured vibe-coding plan."""
    plan = VibePlan()
    plan.feature_name = extract_feature_name(text)
    plan.detected_stack = detect_keywords(text, STACK_HINTS)
    plan.ui_elements = detect_keywords(text, UI_KEYWORDS)
    plan.behaviors = detect_keywords(text, BEHAVIOR_KEYWORDS)
    plan.edge_cases = detect_keywords(text, EDGE_CASE_SIGNALS)
    plan.iteration_steps = generate_iteration_steps(plan)
    plan.validation_items = generate_validation_checklist(plan)
    return plan


def format_plan(plan: VibePlan) -> str:
    """Render the plan as readable markdown."""
    lines = []
    lines.append("=" * 64)
    lines.append("  VIBE CODING PLAN")
    lines.append("=" * 64)
    lines.append("")
    lines.append(f"Feature: {plan.feature_name}")
    lines.append("")

    # Step 1: Context
    lines.append("--- Step 1: Ground the Vibe (Context) ---")
    if plan.detected_stack:
        lines.append(f"  Detected stack: {', '.join(plan.detected_stack)}")
    else:
        lines.append("  No stack detected — specify your tech stack before starting!")
    lines.append("")

    # Step 2: Intent Analysis
    lines.append("--- Step 2: Intent Analysis ---")
    if plan.ui_elements:
        lines.append(f"  UI elements:  {', '.join(plan.ui_elements)}")
    if plan.behaviors:
        lines.append(f"  Behaviors:    {', '.join(plan.behaviors)}")
    if plan.edge_cases:
        lines.append(f"  Edge cases:   {', '.join(plan.edge_cases)}")
    if not (plan.ui_elements or plan.behaviors or plan.edge_cases):
        lines.append("  Tip: add more behavioral detail — what happens on click, load, error?")
    lines.append("")

    # Step 3: Iteration Plan
    lines.append("--- Step 3: Recommended Iteration Steps ---")
    for i, step in enumerate(plan.iteration_steps, 1):
        lines.append(f"  {i}. {step}")
    lines.append("")

    # Step 4: Validation Checklist
    lines.append("--- Step 4: Validation Checklist ---")
    for item in plan.validation_items:
        lines.append(f"  [ ] {item}")
    lines.append("")

    # Anti-pattern warnings
    lines.append("--- Anti-Pattern Warnings ---")
    warnings = []
    if len(plan.feature_name) > 50:
        warnings.append("Feature scope may be too broad — consider breaking it down")
    if not plan.detected_stack:
        warnings.append("No tech stack mentioned — agent may guess wrong framework")
    if not plan.edge_cases:
        warnings.append("No edge cases mentioned — add error/empty/loading scenarios")
    if not warnings:
        lines.append("  None detected — your request looks well-structured!")
    else:
        for w in warnings:
            lines.append(f"  ! {w}")

    lines.append("")
    lines.append("=" * 64)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Example requests for demo
# ---------------------------------------------------------------------------
EXAMPLES = [
    {
        "title": "React Search Component",
        "request": (
            "I need a search bar component in React with TypeScript and Tailwind "
            "that filters products by name and category. When the user types, "
            "results should update after a 300ms debounce. If no results match, "
            "show a 'No results found' message. Handle the loading state while "
            "fetching from the REST API."
        ),
    },
    {
        "title": "FastAPI Authentication",
        "request": (
            "Build an authentication system with FastAPI and PostgreSQL. "
            "Users should be able to register, login, and get a JWT token. "
            "Handle invalid credentials, expired tokens, and duplicate emails. "
            "Add rate limiting to prevent brute force attacks."
        ),
    },
    {
        "title": "Dashboard Layout (Minimal Detail)",
        "request": (
            "I want a dashboard page."
        ),
    },
]


def main():
    print()
    print("Vibe Coding Planner — Structure your AI coding requests")
    print("=" * 64)
    print()

    if len(sys.argv) > 1:
        # User provided their own request
        text = " ".join(sys.argv[1:])
        plan = analyze(text)
        print(format_plan(plan))
        return

    # Run built-in examples
    for i, example in enumerate(EXAMPLES):
        print(f"Example {i + 1}: {example['title']}")
        print(f"Request: \"{example['request']}\"")
        print()
        plan = analyze(example["request"])
        print(format_plan(plan))
        print()

    print("-" * 64)
    print("Try it yourself:")
    print('  python3 vibe_planner.py "Build a chat widget with Vue and WebSocket..."')
    print()


if __name__ == "__main__":
    main()
