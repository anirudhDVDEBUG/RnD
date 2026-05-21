"""
Sprint Orchestrator — Multi-chat sprint coordination engine.

Simulates how a Claude Code skill would decompose a project goal into
parallel tasks, assign them to virtual agents, execute in phases,
and produce a sprint report.
"""

import json
import time
import random
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class PhaseStatus(Enum):
    WAITING = "waiting"
    ACTIVE = "active"
    DONE = "done"


@dataclass
class Task:
    id: str
    title: str
    description: str
    agent: str
    phase: int = 0
    files: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    duration_ms: int = 0
    output: str = ""


@dataclass
class Phase:
    number: int
    name: str
    tasks: list[Task] = field(default_factory=list)
    status: PhaseStatus = PhaseStatus.WAITING


@dataclass
class SprintPlan:
    name: str
    objective: str
    phases: list[Phase] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Planner: decomposes a goal into a phased sprint plan
# ---------------------------------------------------------------------------

DEMO_PROJECTS = {
    "saas_landing_page": {
        "name": "SaaS Landing Page Sprint",
        "objective": "Build a responsive SaaS landing page with pricing, testimonials, and a signup form",
        "phases": [
            {
                "number": 1,
                "name": "Foundation & Parallel Components",
                "tasks": [
                    {
                        "id": "1a",
                        "title": "Hero section & navigation",
                        "description": "Build responsive hero with CTA and sticky nav bar",
                        "agent": "Agent-A",
                        "files": ["src/components/Hero.tsx", "src/components/Nav.tsx"],
                    },
                    {
                        "id": "1b",
                        "title": "Pricing cards component",
                        "description": "Create 3-tier pricing cards with toggle for monthly/annual",
                        "agent": "Agent-B",
                        "files": ["src/components/Pricing.tsx", "src/data/plans.json"],
                    },
                    {
                        "id": "1c",
                        "title": "Testimonials carousel",
                        "description": "Build auto-rotating testimonials with avatar, quote, role",
                        "agent": "Agent-C",
                        "files": ["src/components/Testimonials.tsx", "src/data/testimonials.json"],
                    },
                ],
            },
            {
                "number": 2,
                "name": "Integration & Forms",
                "tasks": [
                    {
                        "id": "2a",
                        "title": "Signup form with validation",
                        "description": "Email + password form with client-side validation and API stub",
                        "agent": "Agent-A",
                        "files": ["src/components/SignupForm.tsx", "src/api/auth.ts"],
                        "depends_on": ["1a"],
                    },
                    {
                        "id": "2b",
                        "title": "Page assembly & routing",
                        "description": "Wire all components into a single-page layout with smooth scroll",
                        "agent": "Agent-B",
                        "files": ["src/App.tsx", "src/styles/global.css"],
                        "depends_on": ["1a", "1b", "1c"],
                    },
                ],
            },
            {
                "number": 3,
                "name": "QA & Polish",
                "tasks": [
                    {
                        "id": "3a",
                        "title": "Responsive testing & fixes",
                        "description": "Verify all breakpoints, fix layout issues on mobile/tablet",
                        "agent": "Agent-A",
                        "files": ["src/styles/responsive.css"],
                        "depends_on": ["2a", "2b"],
                    },
                    {
                        "id": "3b",
                        "title": "Accessibility & Lighthouse audit",
                        "description": "Fix a11y issues, optimize LCP, ensure Lighthouse > 90",
                        "agent": "Agent-C",
                        "files": ["src/components/*.tsx"],
                        "depends_on": ["2a", "2b"],
                    },
                ],
            },
        ],
        "acceptance_criteria": [
            "All 3 pricing tiers render correctly with toggle",
            "Signup form validates and submits without errors",
            "Lighthouse performance score > 90",
            "Responsive layout works on 320px-1920px widths",
            "All testimonials rotate with accessible controls",
        ],
    },
    "cli_tool": {
        "name": "CLI Analytics Tool Sprint",
        "objective": "Build a CLI tool that fetches analytics data, processes it, and generates markdown reports",
        "phases": [
            {
                "number": 1,
                "name": "Core Modules",
                "tasks": [
                    {
                        "id": "1a",
                        "title": "CLI argument parser",
                        "description": "Build argparse-based CLI with subcommands: fetch, report, config",
                        "agent": "Agent-A",
                        "files": ["src/cli.py", "src/config.py"],
                    },
                    {
                        "id": "1b",
                        "title": "Data fetcher module",
                        "description": "HTTP client that pulls analytics from REST API with retry logic",
                        "agent": "Agent-B",
                        "files": ["src/fetcher.py", "src/models.py"],
                    },
                    {
                        "id": "1c",
                        "title": "Markdown report generator",
                        "description": "Jinja2 templates that render analytics data into .md reports",
                        "agent": "Agent-C",
                        "files": ["src/reporter.py", "templates/report.md.j2"],
                    },
                ],
            },
            {
                "number": 2,
                "name": "Integration",
                "tasks": [
                    {
                        "id": "2a",
                        "title": "Pipeline wiring",
                        "description": "Connect fetch -> process -> report pipeline in main entrypoint",
                        "agent": "Agent-A",
                        "files": ["src/main.py"],
                        "depends_on": ["1a", "1b", "1c"],
                    },
                    {
                        "id": "2b",
                        "title": "Unit tests",
                        "description": "Pytest tests for fetcher, reporter, and CLI",
                        "agent": "Agent-B",
                        "files": ["tests/test_fetcher.py", "tests/test_reporter.py"],
                        "depends_on": ["1a", "1b", "1c"],
                    },
                ],
            },
        ],
        "acceptance_criteria": [
            "CLI accepts --format markdown|json flag",
            "Fetcher retries 3x on transient errors",
            "Report renders valid markdown with tables",
            "All unit tests pass",
        ],
    },
}


def plan_sprint(project_key: str = "saas_landing_page") -> SprintPlan:
    """Build a SprintPlan from a demo project definition."""
    proj = DEMO_PROJECTS[project_key]
    phases = []
    for ph in proj["phases"]:
        tasks = [
            Task(
                id=t["id"],
                title=t["title"],
                description=t["description"],
                agent=t["agent"],
                files=t.get("files", []),
                depends_on=t.get("depends_on", []),
            )
            for t in ph["tasks"]
        ]
        phases.append(Phase(number=ph["number"], name=ph["name"], tasks=tasks))

    return SprintPlan(
        name=proj["name"],
        objective=proj["objective"],
        phases=phases,
        acceptance_criteria=proj["acceptance_criteria"],
    )


# ---------------------------------------------------------------------------
# Executor: simulates parallel agent work
# ---------------------------------------------------------------------------

def _simulate_agent_work(task: Task) -> Task:
    """Simulate an agent completing a task with realistic timing."""
    task.status = TaskStatus.IN_PROGRESS
    # Simulate work duration (50-300ms)
    duration = random.randint(50, 300)
    time.sleep(duration / 1000)
    task.duration_ms = duration
    task.status = TaskStatus.COMPLETED
    file_list = ", ".join(task.files) if task.files else "N/A"
    task.output = f"[{task.agent}] Completed: {task.title} | Files: {file_list}"
    return task


def check_dependencies(task: Task, completed_ids: set[str]) -> bool:
    """Check if all dependencies for a task are satisfied."""
    return all(dep in completed_ids for dep in task.depends_on)


def execute_sprint(plan: SprintPlan, verbose: bool = True) -> dict:
    """Execute the sprint plan phase by phase, simulating parallel agents."""
    completed_ids: set[str] = set()
    total_tasks = sum(len(ph.tasks) for ph in plan.phases)
    completed_count = 0
    timeline: list[dict] = []
    sprint_start = time.time()

    if verbose:
        print(f"\n{'='*64}")
        print(f"  SPRINT: {plan.name}")
        print(f"  Objective: {plan.objective}")
        print(f"  Phases: {len(plan.phases)} | Tasks: {total_tasks}")
        print(f"{'='*64}\n")

    for phase in plan.phases:
        phase.status = PhaseStatus.ACTIVE
        if verbose:
            agents = sorted(set(t.agent for t in phase.tasks))
            print(f"--- Phase {phase.number}: {phase.name} ---")
            print(f"    Agents: {', '.join(agents)} | Tasks: {len(phase.tasks)}")
            print()

        # Verify dependencies before starting phase
        for task in phase.tasks:
            if not check_dependencies(task, completed_ids):
                blocked = [d for d in task.depends_on if d not in completed_ids]
                if verbose:
                    print(f"    [BLOCKED] {task.id}: waiting on {blocked}")
                task.status = TaskStatus.BLOCKED
                continue

        # Execute tasks in this phase (simulated parallel)
        phase_start = time.time()
        for task in phase.tasks:
            if task.status == TaskStatus.BLOCKED:
                continue
            _simulate_agent_work(task)
            completed_ids.add(task.id)
            completed_count += 1
            progress = completed_count / total_tasks * 100
            if verbose:
                print(f"    [{progress:5.1f}%] {task.output}")
            timeline.append({
                "task_id": task.id,
                "agent": task.agent,
                "title": task.title,
                "duration_ms": task.duration_ms,
                "phase": phase.number,
            })

        phase_elapsed = (time.time() - phase_start) * 1000
        phase.status = PhaseStatus.DONE
        if verbose:
            print(f"    Phase {phase.number} done in {phase_elapsed:.0f}ms\n")

    sprint_elapsed = (time.time() - sprint_start) * 1000

    # Acceptance criteria check
    if verbose:
        print(f"{'='*64}")
        print("  ACCEPTANCE CRITERIA")
        print(f"{'='*64}")
        for i, criterion in enumerate(plan.acceptance_criteria, 1):
            # Simulate all passing
            print(f"  [{chr(10003)}] {criterion}")
        print()

    report = {
        "sprint_name": plan.name,
        "objective": plan.objective,
        "total_tasks": total_tasks,
        "completed_tasks": completed_count,
        "phases_completed": len(plan.phases),
        "total_duration_ms": round(sprint_elapsed),
        "acceptance_criteria_passed": len(plan.acceptance_criteria),
        "acceptance_criteria_total": len(plan.acceptance_criteria),
        "timeline": timeline,
        "agents_used": sorted(set(t.agent for ph in plan.phases for t in ph.tasks)),
    }

    if verbose:
        print(f"{'='*64}")
        print("  SPRINT SUMMARY")
        print(f"{'='*64}")
        print(f"  Tasks completed : {report['completed_tasks']}/{report['total_tasks']}")
        print(f"  Phases completed: {report['phases_completed']}/{len(plan.phases)}")
        print(f"  Agents used     : {', '.join(report['agents_used'])}")
        print(f"  Total duration  : {report['total_duration_ms']}ms")
        print(f"  Criteria passed : {report['acceptance_criteria_passed']}/{report['acceptance_criteria_total']}")
        print(f"{'='*64}\n")

    return report


# ---------------------------------------------------------------------------
# Sprint report generator
# ---------------------------------------------------------------------------

def generate_markdown_report(plan: SprintPlan, report: dict) -> str:
    """Generate a markdown sprint report."""
    lines = [
        f"# Sprint Report: {report['sprint_name']}",
        "",
        f"**Objective:** {report['objective']}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Tasks completed | {report['completed_tasks']}/{report['total_tasks']} |",
        f"| Phases | {report['phases_completed']} |",
        f"| Agents | {', '.join(report['agents_used'])} |",
        f"| Duration | {report['total_duration_ms']}ms |",
        f"| Criteria passed | {report['acceptance_criteria_passed']}/{report['acceptance_criteria_total']} |",
        "",
        "## Phase Breakdown",
        "",
    ]

    for phase in plan.phases:
        lines.append(f"### Phase {phase.number}: {phase.name}")
        lines.append("")
        for task in phase.tasks:
            status_icon = "[x]" if task.status == TaskStatus.COMPLETED else "[ ]"
            deps = f" (depends: {', '.join(task.depends_on)})" if task.depends_on else ""
            lines.append(f"- {status_icon} **{task.id}** {task.title} -> {task.agent}{deps}")
            lines.append(f"  - Files: {', '.join(task.files)}")
            lines.append(f"  - Duration: {task.duration_ms}ms")
        lines.append("")

    lines.append("## Acceptance Criteria")
    lines.append("")
    for criterion in plan.acceptance_criteria:
        lines.append(f"- [x] {criterion}")
    lines.append("")

    lines.append("## Agent Timeline")
    lines.append("")
    lines.append("| Task | Agent | Duration | Phase |")
    lines.append("|------|-------|----------|-------|")
    for entry in report["timeline"]:
        lines.append(
            f"| {entry['task_id']}: {entry['title']} "
            f"| {entry['agent']} "
            f"| {entry['duration_ms']}ms "
            f"| Phase {entry['phase']} |"
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Sprint Orchestrator — multi-agent sprint simulation"
    )
    parser.add_argument(
        "--project",
        choices=list(DEMO_PROJECTS.keys()),
        default="saas_landing_page",
        help="Demo project to orchestrate (default: saas_landing_page)",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Path to write markdown report (optional)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output sprint results as JSON",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose console output",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all demo projects",
    )
    args = parser.parse_args()

    projects = list(DEMO_PROJECTS.keys()) if args.all else [args.project]

    for project_key in projects:
        plan = plan_sprint(project_key)
        report = execute_sprint(plan, verbose=not args.quiet)

        if args.json:
            print(json.dumps(report, indent=2))

        if args.report:
            md = generate_markdown_report(plan, report)
            path = args.report if len(projects) == 1 else args.report.replace(".md", f"_{project_key}.md")
            with open(path, "w") as f:
                f.write(md)
            print(f"Report written to {path}")

        md = generate_markdown_report(plan, report)
        print(md)


if __name__ == "__main__":
    main()
