# Technical Details: Sprint Orchestrator

## What It Actually Does

Sprint Orchestrator is a **prompt-based skill** for Claude Code — a structured SKILL.md file that teaches Claude a multi-phase workflow for coordinating parallel development across multiple chat sessions. It is not a standalone program; it augments Claude Code's behavior so that when a user asks for "sprint orchestration," Claude follows a repeatable decomposition-and-coordination protocol.

The skill encodes a 4-step process: (1) decompose a project goal into parallelizable tasks with dependency tracking, (2) assign tasks to agents with file-level isolation to prevent merge conflicts, (3) execute in phases where all tasks in a phase run in parallel and phase boundaries enforce dependency gates, and (4) validate acceptance criteria before declaring the sprint complete.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The actual skill definition — drop this into `~/.claude/skills/sprint-orchestrator/` |
| `sprint_orchestrator.py` | Demo engine: planning, execution simulation, report generation |
| `sprint_visualizer.py` | ASCII dependency graphs, Gantt charts, file isolation matrix |
| `run.sh` | End-to-end demo runner |

### Data Flow (in the skill)

```
User goal
  -> Task decomposition (identify independent work units)
  -> Dependency analysis (build DAG of task prerequisites)
  -> Phase grouping (batch parallelizable tasks)
  -> Agent assignment (map tasks to chat sessions with file isolation)
  -> Phase-gated execution (run phase N, verify, then phase N+1)
  -> Acceptance criteria check
  -> Sprint report
```

### Data Flow (in the demo)

```
DEMO_PROJECTS dict (mock project definitions)
  -> plan_sprint() builds SprintPlan dataclass
  -> execute_sprint() runs tasks phase-by-phase with simulated timing
  -> generate_markdown_report() produces .md output
  -> sprint_visualizer renders ASCII graphs
```

### Dependencies

- **Skill itself**: Zero dependencies. It's a markdown file that Claude Code reads.
- **Demo code**: Python 3.10+ standard library only. No pip packages.

### Model Calls

The skill itself makes no API calls — it structures Claude Code's existing capabilities. The demo uses no model calls either; it simulates agent work with `time.sleep()` and random durations.

## Limitations

- **No actual multi-process orchestration.** The skill is a prompt protocol — it tells Claude *how* to coordinate, but the user still manually opens multiple Claude Code sessions. There is no daemon, no message bus, no IPC.
- **No real-time sync.** Agents don't communicate during execution. The orchestrator (the primary Claude session) checks progress at phase boundaries by reading files or asking the user.
- **File isolation is advisory.** The skill recommends assigning disjoint file sets to agents, but nothing enforces it. If two agents edit the same file, you get merge conflicts.
- **No persistent state.** Sprint plans live in the conversation context or in markdown files the user saves. There's no database, no sprint history.
- **Scales to ~3-5 agents.** Beyond that, the human overhead of managing chat sessions outweighs the parallelism gains.

## Why It Might Matter

For teams building **Claude-driven products** (agent factories, marketing automation, lead-gen pipelines, ad creative workflows):

- **Agent factories**: This is a lightweight orchestration pattern for multi-agent systems. If you're building a product where multiple Claude instances collaborate, this skill's decomposition + dependency gating + file isolation approach is a proven starting point — battle-tested across 17+ sprints.
- **Development velocity**: For internal teams using Claude Code, adopting this skill means faster feature delivery through structured parallelism instead of ad-hoc "go build this" prompts.
- **Reproducibility**: The phased sprint format produces auditable sprint reports, making it easier to track what AI agents actually did — useful for compliance-sensitive industries.
- **Template for custom skills**: The SKILL.md structure itself is a good reference for how to write effective Claude Code skills — clear trigger phrases, step-by-step workflow, concrete examples.
