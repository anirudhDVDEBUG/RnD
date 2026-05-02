"""
AI-Native Development Workflow Engine

Generates the full 4-Phase artifact set for a project, demonstrating how
multiple AI agents can collaborate under shared contracts.
"""

import json
import os
import textwrap
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Data models ──────────────────────────────────────────────────────────────

@dataclass
class Module:
    name: str
    responsibility: str
    owner: str  # agent name
    files: list[str]
    dependencies: list[str] = field(default_factory=list)

@dataclass
class Contract:
    name: str
    provider_module: str
    consumer_modules: list[str]
    interface: dict  # simplified schema

@dataclass
class Task:
    id: str
    title: str
    module: str
    agent: str
    branch: str
    depends_on: list[str] = field(default_factory=list)
    status: str = "pending"

@dataclass
class ProjectPlan:
    name: str
    description: str
    tech_stack: list[str]
    modules: list[Module]
    contracts: list[Contract]
    tasks: list[Task]
    conventions: dict


# ── Phase 1: Align ───────────────────────────────────────────────────────────

def phase1_align(project_name: str, description: str, tech_stack: list[str],
                 modules_spec: list[dict]) -> tuple[list[Module], dict]:
    """Define the blueprint: architecture, conventions, module map."""
    modules = []
    for i, spec in enumerate(modules_spec):
        modules.append(Module(
            name=spec["name"],
            responsibility=spec["responsibility"],
            owner=f"agent-{i + 1}",
            files=spec.get("files", [f"src/{spec['name']}/"]),
            dependencies=spec.get("dependencies", []),
        ))

    conventions = {
        "branch_pattern": "agent/<task-id>-<short-desc>",
        "commit_format": "<type>(<scope>): <description>",
        "file_naming": "snake_case",
        "test_pattern": "tests/test_<module>.py",
        "contract_location": "contracts/",
        "max_agent_scope": "one module per agent",
    }

    return modules, conventions


# ── Phase 2: Design ─────────────────────────────────────────────────────────

def phase2_design(modules: list[Module]) -> tuple[list[Contract], list[Task]]:
    """Define contracts and parallelizable tasks."""
    contracts = []
    tasks = []
    task_counter = 1

    for mod in modules:
        # Auto-generate contracts for inter-module dependencies
        for dep in mod.dependencies:
            contract = Contract(
                name=f"{dep}_to_{mod.name}_contract",
                provider_module=dep,
                consumer_modules=[mod.name],
                interface={
                    "type": "function_call",
                    "functions": [
                        {
                            "name": f"get_{dep}_data",
                            "params": {"id": "string"},
                            "returns": {"data": "object", "status": "string"},
                        }
                    ],
                },
            )
            contracts.append(contract)

        # Create implementation task for each module
        task = Task(
            id=f"TASK-{task_counter:03d}",
            title=f"Implement {mod.name} module",
            module=mod.name,
            agent=mod.owner,
            branch=f"agent/{mod.owner}-{mod.name}",
            depends_on=[f"TASK-{modules.index(m) + 1:03d}"
                        for m in modules if m.name in mod.dependencies],
        )
        tasks.append(task)
        task_counter += 1

        # Create test task for each module
        test_task = Task(
            id=f"TASK-{task_counter:03d}",
            title=f"Write contract tests for {mod.name}",
            module=mod.name,
            agent=mod.owner,
            branch=f"agent/{mod.owner}-{mod.name}",
            depends_on=[task.id],
        )
        tasks.append(test_task)
        task_counter += 1

    return contracts, tasks


# ── Phase 3: Build (simulated) ──────────────────────────────────────────────

def phase3_build(tasks: list[Task]) -> list[Task]:
    """Simulate parallel build execution. Returns tasks with updated status."""
    resolved = set()
    rounds = []
    remaining = list(tasks)

    while remaining:
        # Find tasks whose dependencies are all resolved
        batch = [t for t in remaining
                 if all(d in resolved for d in t.depends_on)]
        if not batch:
            # Mark remaining as blocked
            for t in remaining:
                t.status = "blocked"
            break
        for t in batch:
            t.status = "completed"
            resolved.add(t.id)
            remaining.remove(t)
        rounds.append([t.id for t in batch])

    return tasks, rounds


# ── Phase 4: Integrate ──────────────────────────────────────────────────────

def phase4_integrate(tasks: list[Task], contracts: list[Contract]) -> dict:
    """Simulate integration: merge branches, run contract checks."""
    completed = [t for t in tasks if t.status == "completed"]
    blocked = [t for t in tasks if t.status == "blocked"]

    merge_order = []
    seen_branches = set()
    for t in completed:
        if t.branch not in seen_branches:
            merge_order.append(t.branch)
            seen_branches.add(t.branch)

    contract_checks = []
    for c in contracts:
        contract_checks.append({
            "contract": c.name,
            "provider": c.provider_module,
            "consumers": c.consumer_modules,
            "status": "PASS",
        })

    return {
        "merge_order": merge_order,
        "branches_merged": len(merge_order),
        "contract_checks": contract_checks,
        "all_checks_pass": all(c["status"] == "PASS" for c in contract_checks),
        "tasks_completed": len(completed),
        "tasks_blocked": len(blocked),
    }


# ── Artifact generation ─────────────────────────────────────────────────────

def generate_architecture_md(plan: ProjectPlan) -> str:
    lines = [f"# {plan.name} — Architecture\n"]
    lines.append(f"> {plan.description}\n")
    lines.append(f"## Tech Stack\n")
    for t in plan.tech_stack:
        lines.append(f"- {t}")
    lines.append(f"\n## Modules\n")
    for m in plan.modules:
        deps = f" (depends on: {', '.join(m.dependencies)})" if m.dependencies else ""
        lines.append(f"### {m.name}{deps}")
        lines.append(f"- **Responsibility**: {m.responsibility}")
        lines.append(f"- **Owner**: {m.owner}")
        lines.append(f"- **Files**: {', '.join(m.files)}")
        lines.append("")
    return "\n".join(lines)


def generate_conventions_md(conventions: dict) -> str:
    lines = ["# Coding Conventions\n"]
    for key, val in conventions.items():
        lines.append(f"- **{key.replace('_', ' ').title()}**: `{val}`")
    return "\n".join(lines)


def generate_contracts_json(contracts: list[Contract]) -> str:
    return json.dumps([asdict(c) for c in contracts], indent=2)


def generate_task_board(tasks: list[Task], rounds: list[list[str]]) -> str:
    lines = ["# Task Board\n"]
    lines.append("## Execution Rounds (parallelizable batches)\n")
    for i, batch in enumerate(rounds, 1):
        lines.append(f"**Round {i}** — {len(batch)} tasks in parallel:")
        for tid in batch:
            task = next(t for t in tasks if t.id == tid)
            lines.append(f"  - `{task.id}` {task.title} → `{task.branch}` ({task.agent})")
        lines.append("")

    lines.append("## All Tasks\n")
    lines.append("| ID | Title | Agent | Branch | Status |")
    lines.append("|---|---|---|---|---|")
    for t in tasks:
        lines.append(f"| {t.id} | {t.title} | {t.agent} | `{t.branch}` | {t.status} |")
    return "\n".join(lines)


def generate_claude_md(plan: ProjectPlan) -> str:
    lines = ["# CLAUDE.md — Shared Agent Context\n"]
    lines.append(f"## Project: {plan.name}\n")
    lines.append(f"{plan.description}\n")
    lines.append("## Module Map\n")
    for m in plan.modules:
        lines.append(f"- **{m.name}** ({m.owner}): {m.responsibility}")
    lines.append("\n## Conventions\n")
    for key, val in plan.conventions.items():
        lines.append(f"- {key.replace('_', ' ').title()}: `{val}`")
    lines.append("\n## Contract Locations\n")
    lines.append("- All contracts: `contracts/contracts.json`")
    lines.append("- Architecture: `ARCHITECTURE.md`")
    lines.append("\n## Branch Rules\n")
    lines.append("- One branch per agent-task: `agent/<agent>-<module>`")
    lines.append("- Do NOT modify contracts during Phase 3 (Build)")
    lines.append("- Each agent owns only their assigned module files")
    return "\n".join(lines)


def generate_integration_report(result: dict) -> str:
    lines = ["# Integration Report\n"]
    lines.append(f"## Summary\n")
    lines.append(f"- Tasks completed: {result['tasks_completed']}")
    lines.append(f"- Tasks blocked: {result['tasks_blocked']}")
    lines.append(f"- Branches merged: {result['branches_merged']}")
    lines.append(f"- All contract checks pass: {'YES' if result['all_checks_pass'] else 'NO'}\n")
    lines.append("## Merge Order\n")
    for i, b in enumerate(result["merge_order"], 1):
        lines.append(f"{i}. `{b}`")
    lines.append("\n## Contract Verification\n")
    lines.append("| Contract | Provider | Consumers | Status |")
    lines.append("|---|---|---|---|")
    for c in result["contract_checks"]:
        lines.append(f"| {c['contract']} | {c['provider']} | {', '.join(c['consumers'])} | {c['status']} |")
    return "\n".join(lines)


# ── Full pipeline ────────────────────────────────────────────────────────────

def run_full_pipeline(project_name: str, description: str,
                      tech_stack: list[str], modules_spec: list[dict],
                      output_dir: Optional[str] = None) -> ProjectPlan:
    """Execute all 4 phases and generate artifacts."""
    print(f"\n{'='*60}")
    print(f"  AI-Native 4-Phase Workflow: {project_name}")
    print(f"{'='*60}\n")

    # Phase 1
    print("[Phase 1: ALIGN] Defining architecture & conventions...")
    modules, conventions = phase1_align(project_name, description,
                                         tech_stack, modules_spec)
    print(f"  -> {len(modules)} modules defined, conventions established\n")

    # Phase 2
    print("[Phase 2: DESIGN] Generating contracts & task breakdown...")
    contracts, tasks = phase2_design(modules)
    print(f"  -> {len(contracts)} contracts, {len(tasks)} tasks created\n")

    # Phase 3
    print("[Phase 3: BUILD] Simulating parallel agent execution...")
    tasks, rounds = phase3_build(tasks)
    print(f"  -> {len(rounds)} execution rounds")
    for i, batch in enumerate(rounds, 1):
        print(f"     Round {i}: {len(batch)} tasks in parallel")
    print()

    # Phase 4
    print("[Phase 4: INTEGRATE] Merging branches & verifying contracts...")
    integration = phase4_integrate(tasks, contracts)
    print(f"  -> {integration['branches_merged']} branches merged")
    print(f"  -> Contract checks: {'ALL PASS' if integration['all_checks_pass'] else 'FAILURES'}\n")

    plan = ProjectPlan(
        name=project_name,
        description=description,
        tech_stack=tech_stack,
        modules=modules,
        contracts=contracts,
        tasks=tasks,
        conventions=conventions,
    )

    # Write artifacts
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "contracts"), exist_ok=True)

        artifacts = {
            "ARCHITECTURE.md": generate_architecture_md(plan),
            "CONVENTIONS.md": generate_conventions_md(plan),
            "CLAUDE.md": generate_claude_md(plan),
            "TASK_BOARD.md": generate_task_board(tasks, rounds),
            "INTEGRATION_REPORT.md": generate_integration_report(integration),
            "contracts/contracts.json": generate_contracts_json(contracts),
        }

        for filename, content in artifacts.items():
            path = os.path.join(output_dir, filename)
            with open(path, "w") as f:
                f.write(content)
            print(f"  [wrote] {path}")

    print(f"\n{'='*60}")
    print(f"  Workflow complete. {len(tasks)} tasks across {len(rounds)} rounds.")
    print(f"{'='*60}\n")

    return plan, integration
