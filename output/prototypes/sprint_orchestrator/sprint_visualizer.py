"""
Sprint Visualizer — renders ASCII timeline and dependency graphs
for sprint plans, showing how agents work in parallel.
"""

from sprint_orchestrator import SprintPlan, Task, Phase


def render_dependency_graph(plan: SprintPlan) -> str:
    """Render an ASCII dependency graph of the sprint plan."""
    lines = []
    lines.append("DEPENDENCY GRAPH")
    lines.append("")

    all_tasks: dict[str, Task] = {}
    for phase in plan.phases:
        for task in phase.tasks:
            all_tasks[task.id] = task

    for phase in plan.phases:
        lines.append(f"  Phase {phase.number}: {phase.name}")
        for task in phase.tasks:
            deps_str = ""
            if task.depends_on:
                arrows = " + ".join(task.depends_on)
                deps_str = f"  <-- [{arrows}]"
            agent_tag = f"[{task.agent}]"
            lines.append(f"    {task.id}: {task.title:<35} {agent_tag:<12}{deps_str}")
        lines.append("")

    return "\n".join(lines)


def render_gantt_chart(plan: SprintPlan) -> str:
    """Render a simple ASCII Gantt-style chart showing parallel execution."""
    lines = []
    lines.append("GANTT CHART (simulated parallel execution)")
    lines.append("")

    agents = sorted(set(t.agent for ph in plan.phases for t in ph.tasks))
    agent_width = max(len(a) for a in agents)

    col_width = 16
    header = " " * (agent_width + 2)
    for phase in plan.phases:
        label = f"Phase {phase.number}"
        header += f"| {label:<{col_width - 2}} "
    lines.append(header + "|")
    lines.append("-" * len(header) + "-")

    # Build a map: agent -> phase -> task title
    agent_phase_map: dict[str, dict[int, str]] = {a: {} for a in agents}
    for phase in plan.phases:
        for task in phase.tasks:
            agent_phase_map[task.agent][phase.number] = task.id + ": " + task.title[:col_width - 6]

    for agent in agents:
        row = f"{agent:<{agent_width}}  "
        for phase in plan.phases:
            task_label = agent_phase_map[agent].get(phase.number, "")
            if task_label:
                bar = f"[{'#' * min(len(task_label), col_width - 4)}]"
                cell = f"{bar:<{col_width - 2}}"
            else:
                cell = f"{'.' * (col_width - 2)}"
            row += f"| {cell} "
        lines.append(row + "|")

    lines.append("")
    lines.append("Legend: [###] = active work, .... = idle")
    lines.append("")
    return "\n".join(lines)


def render_file_isolation_matrix(plan: SprintPlan) -> str:
    """Show which agents touch which files — confirms no conflicts."""
    lines = []
    lines.append("FILE ISOLATION MATRIX")
    lines.append("")

    file_owners: dict[str, list[str]] = {}
    for phase in plan.phases:
        for task in phase.tasks:
            for f in task.files:
                file_owners.setdefault(f, []).append(f"{task.agent} ({task.id})")

    conflicts = 0
    for filepath, owners in sorted(file_owners.items()):
        # Check unique agents
        unique_agents = set(o.split(" ")[0] for o in owners)
        marker = "  " if len(unique_agents) == 1 else "!!"
        if len(unique_agents) > 1:
            conflicts += 1
        lines.append(f"  {marker} {filepath:<45} -> {', '.join(owners)}")

    lines.append("")
    if conflicts:
        lines.append(f"  WARNING: {conflicts} file(s) touched by multiple agents — review for merge conflicts")
    else:
        lines.append("  OK: No file conflicts detected — all files have single-agent ownership")
    lines.append("")
    return "\n".join(lines)


def render_full_visualization(plan: SprintPlan) -> str:
    """Render all visualizations for a sprint plan."""
    sep = "=" * 64
    parts = [
        sep,
        f"  SPRINT VISUALIZATION: {plan.name}",
        sep,
        "",
        render_dependency_graph(plan),
        render_gantt_chart(plan),
        render_file_isolation_matrix(plan),
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    from sprint_orchestrator import plan_sprint
    plan = plan_sprint("saas_landing_page")
    print(render_full_visualization(plan))
