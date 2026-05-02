#!/usr/bin/env python3
"""
Demo: Run the AI-Native 4-Phase Workflow on a sample e-commerce project.

This generates all the artifacts that would coordinate multiple AI agents
working in parallel — architecture docs, contracts, task boards, and
integration reports.
"""

import os
import sys
from workflow_engine import run_full_pipeline, generate_architecture_md

DEMO_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "demo_output")


def demo_ecommerce_platform():
    """Scenario: Greenfield e-commerce API with 4 modules, 4 agents."""
    modules_spec = [
        {
            "name": "auth",
            "responsibility": "User registration, login, JWT token management",
            "files": ["src/auth/routes.py", "src/auth/models.py", "src/auth/service.py"],
            "dependencies": [],
        },
        {
            "name": "catalog",
            "responsibility": "Product CRUD, search, categories",
            "files": ["src/catalog/routes.py", "src/catalog/models.py", "src/catalog/service.py"],
            "dependencies": [],
        },
        {
            "name": "cart",
            "responsibility": "Shopping cart management, item add/remove/update",
            "files": ["src/cart/routes.py", "src/cart/models.py", "src/cart/service.py"],
            "dependencies": ["auth", "catalog"],
        },
        {
            "name": "checkout",
            "responsibility": "Order placement, payment processing, order history",
            "files": ["src/checkout/routes.py", "src/checkout/models.py", "src/checkout/service.py"],
            "dependencies": ["auth", "cart"],
        },
    ]

    plan, integration = run_full_pipeline(
        project_name="ShopFlow API",
        description="E-commerce REST API with auth, catalog, cart, and checkout modules",
        tech_stack=["Python 3.12", "FastAPI", "PostgreSQL", "SQLAlchemy", "pytest"],
        modules_spec=modules_spec,
        output_dir=DEMO_OUTPUT_DIR,
    )
    return plan, integration


def demo_existing_codebase():
    """Scenario: Adding features to an existing monolith being split into modules."""
    modules_spec = [
        {
            "name": "user_profile",
            "responsibility": "Existing user model — add profile pic upload and bio fields",
            "files": ["app/models/user.py", "app/views/profile.py"],
            "dependencies": [],
        },
        {
            "name": "notifications",
            "responsibility": "New module — email + push notification service",
            "files": ["app/notifications/sender.py", "app/notifications/templates.py"],
            "dependencies": ["user_profile"],
        },
        {
            "name": "analytics",
            "responsibility": "New module — event tracking and dashboard data",
            "files": ["app/analytics/tracker.py", "app/analytics/dashboard.py"],
            "dependencies": ["user_profile"],
        },
    ]

    plan, integration = run_full_pipeline(
        project_name="Acme App Modernization",
        description="Adding notifications and analytics to existing Django monolith",
        tech_stack=["Python 3.11", "Django 4.2", "Celery", "Redis", "pytest"],
        modules_spec=modules_spec,
        output_dir=os.path.join(DEMO_OUTPUT_DIR, "existing_codebase"),
    )
    return plan, integration


def print_sample_artifact():
    """Print one generated artifact so the user sees concrete output."""
    artifact_path = os.path.join(DEMO_OUTPUT_DIR, "ARCHITECTURE.md")
    if os.path.exists(artifact_path):
        print("\n" + "=" * 60)
        print("  SAMPLE ARTIFACT: ARCHITECTURE.md")
        print("=" * 60)
        with open(artifact_path) as f:
            print(f.read())

    task_path = os.path.join(DEMO_OUTPUT_DIR, "TASK_BOARD.md")
    if os.path.exists(task_path):
        print("\n" + "=" * 60)
        print("  SAMPLE ARTIFACT: TASK_BOARD.md")
        print("=" * 60)
        with open(task_path) as f:
            print(f.read())


def print_anti_patterns():
    """Quick-reference anti-pattern table."""
    print("\n" + "=" * 60)
    print("  ANTI-PATTERN QUICK REFERENCE")
    print("=" * 60)
    anti_patterns = [
        ("Skip contracts", "Agents make incompatible assumptions",
         "Always define interfaces in Phase 2"),
        ("Shared mutable state", "Agents overwrite each other",
         "Branch-per-task, merge at Phase 4"),
        ("Vague task scope", "Wrong output or scope-creep",
         "Clear inputs/outputs/boundaries per task"),
        ("Edit contracts mid-build", "Breaks in-progress work",
         "Freeze contracts during Phase 3"),
        ("Monolithic tasks", "Agent loses context",
         "Small, focused, independently testable"),
        ("No integration tests", "Modules fail together",
         "Contract-compliance tests in Phase 2"),
    ]
    print(f"\n{'Anti-Pattern':<26} {'Risk':<35} {'Fix'}")
    print("-" * 100)
    for name, risk, fix in anti_patterns:
        print(f"{name:<26} {risk:<35} {fix}")
    print()


def main():
    print("\n" + "#" * 60)
    print("#  AI-Native Development Workflow — 4-Phase Framework Demo")
    print("#" * 60)

    # Scenario 1: Greenfield
    print("\n>>> SCENARIO 1: Greenfield Project (e-commerce API)")
    demo_ecommerce_platform()

    # Scenario 2: Existing codebase
    print("\n>>> SCENARIO 2: Existing Codebase (Django monolith modernization)")
    demo_existing_codebase()

    # Show sample artifacts
    print_sample_artifact()

    # Anti-patterns
    print_anti_patterns()

    # Summary
    print("=" * 60)
    print("  Generated artifacts in: demo_output/")
    print("  Files:")
    for root, dirs, files in os.walk(DEMO_OUTPUT_DIR):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), DEMO_OUTPUT_DIR)
            print(f"    - demo_output/{rel}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
