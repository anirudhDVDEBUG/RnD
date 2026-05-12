# Technical Details

## What It Actually Does

Goalkeeper implements a **plan-execute-judge loop** for autonomous goal
completion. You define a goal with a list of concrete, verifiable acceptance
criteria (the "Definition of Done"). An executor works toward the goal,
producing artifacts. An independent judge evaluates every criterion against
those artifacts. If any criterion fails, the executor gets the feedback and
iterates. The goal is only marked complete when every criterion passes -- or
a max-iteration cap is reached.

This pattern is especially powerful when the executor is an LLM agent (like
Claude Code subagents): the judge acts as an automated QA gate that prevents
the agent from declaring victory prematurely.

## Architecture

```
User
  |
  v
GoalkeeperEngine.run(goal, executor)
  |
  +---> executor(goal) -----> updates goal.artifacts
  |                                |
  +---> Judge.evaluate(goal) <-----+
  |         |
  |         +-- for each Criterion:
  |         |     verifier(artifacts) -> (pass/fail, feedback)
  |         +-- updates criterion.status & feedback
  |
  +---> if all PASS: done
  |     else: loop (up to max_iterations)
  |
  v
Goal (with final statuses + report)
```

### Key Files

| File | Purpose |
|------|---------|
| `goalkeeper.py` | Core engine: `Goal`, `Criterion`, `Judge`, `GoalkeeperEngine` |
| `demo.py` | End-to-end demo with simulated executor and verifiers |
| `run.sh` | One-command runner |
| `SKILL.md` | Claude Code skill definition (drop into `~/.claude/skills/`) |

### Data Flow

1. **Goal** is created with a title, description, and list of `Criterion` objects
2. Each `Criterion` has a `verifier` function: `(artifacts) -> (bool, str)`
3. **Executor** receives the goal, produces/updates `goal.artifacts` (a dict)
4. **Judge** runs each verifier against artifacts, sets PASS/FAIL + feedback
5. Loop continues until all criteria pass or max iterations reached
6. Final report is emitted as JSON

### Dependencies

- **Python 3.10+** (uses `X | None` union syntax)
- **No external packages** -- stdlib only for the core engine
- In a real Claude Code deployment, the skill triggers Claude's built-in
  subagent spawning; no separate install is needed

### Model Calls

The local demo makes **zero API calls**. It uses rule-based verifiers to
simulate what a Claude subagent judge would do. In production use as a Claude
Code skill, the judge is a spawned Claude subagent -- so each judge evaluation
is one model call containing the DoD + current artifacts.

## Limitations

- **Not a standalone agent framework.** Goalkeeper is a *pattern* (and a Claude
  Code skill), not a full agent runtime. It defines the contract + judge loop;
  you supply the executor.
- **Verifiers must be deterministic.** The judge is only as good as the
  verifier functions. Vague criteria ("code is clean") produce unreliable
  results.
- **No built-in persistence.** The current implementation is in-memory. For
  durable execution across context switches, you'd need to serialize
  `Goal` state to disk/DB (the upstream repo does this via Claude Code's
  TodoWrite and file artifacts).
- **Single-judge model.** There's no consensus mechanism -- one judge,
  one evaluation per iteration.
- **Max iterations cap.** If the executor can't satisfy criteria within the
  cap (default 5), the goal is marked incomplete rather than looping forever.

## Why It Matters for Claude-Driven Products

| Domain | Application |
|--------|-------------|
| **Agent factories** | Every spawned agent gets a DoD contract -- prevents autonomous agents from shipping broken work. Quality gate for multi-agent pipelines. |
| **Lead-gen / marketing** | Define acceptance criteria for generated content (word count, CTA presence, brand voice compliance), auto-reject and iterate until met. |
| **Ad creatives** | Gate ad copy/image generation with verifiable criteria: character limits, required disclaimers, A/B variant count. |
| **Voice AI** | Validate that generated voice scripts meet duration, reading-level, and keyword-inclusion requirements before synthesis. |
| **Code generation** | Attach test-based verifiers: the judge runs unit tests and only passes if all green. Directly applicable to CI-gated PRs. |

The core insight: **autonomous agents need explicit success contracts**, not
just instructions. Goalkeeper provides the pattern.
