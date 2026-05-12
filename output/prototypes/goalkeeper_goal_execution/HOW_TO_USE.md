# How to Use Goalkeeper

## What Is It?

Goalkeeper is a **Claude Code skill** -- a markdown-based instruction set that
teaches Claude a new workflow pattern. In this case: define a goal with
explicit acceptance criteria, work toward it, then use a subagent judge to
gate completion.

---

## Install (Claude Code Skill)

### 1. Drop the SKILL.md folder

```bash
mkdir -p ~/.claude/skills/goalkeeper_goal_execution
cp SKILL.md ~/.claude/skills/goalkeeper_goal_execution/SKILL.md
```

Or clone the upstream repo:

```bash
git clone https://github.com/itsuzef/goalkeeper.git
cp -r goalkeeper/skill ~/.claude/skills/goalkeeper_goal_execution
```

### 2. Trigger Phrases

Once installed, any of these phrases in a Claude Code session will activate the
goalkeeper workflow:

- "Execute this goal with a definition of done"
- "Use goalkeeper to track and verify task completion"
- "Set up a contract-driven goal with acceptance criteria"
- "Run a goal with a subagent judge to verify completion"
- "Break down this task with a definition of done and verify each criterion"

Claude will then:
1. Ask you to define (or help you draft) the goal and DoD criteria
2. Plan subtasks aligned to the criteria
3. Execute each subtask
4. Spawn a judge subagent that evaluates every criterion as PASS/FAIL
5. Loop back if anything failed, up to a configurable max

---

## Run the Local Demo (no API keys needed)

```bash
# No dependencies required -- stdlib Python only
bash run.sh
```

### First 60 Seconds

**Input:** `bash run.sh`

**Output:**
```
============================================================
GOALKEEPER: Starting goal 'User Registration Endpoint'
============================================================
Goal: User Registration Endpoint
  Implement a secure POST /register endpoint with full validation.

Definition of Done:
  [    ] 1. POST /register endpoint exists
  [    ] 2. Passwords are hashed before storage
  [    ] 3. Email addresses are validated
  [    ] 4. Duplicate users are rejected
  [    ] 5. Unit tests cover success and failure paths

>>> Executor: working on 5 pending/failed criteria...
  [executor] Producing initial (incomplete) implementation...

--- Judge Evaluation (iteration 1) ---
Goal: User Registration Endpoint
  ...
  [PASS] 1. POST /register endpoint exists
         -> POST /register endpoint found
  [FAIL] 2. Passwords are hashed before storage
         -> Passwords stored in plaintext -- must hash
  [FAIL] 3. Email addresses are validated
         -> No email validation found
  [FAIL] 4. Duplicate users are rejected
         -> No duplicate-user guard
  [FAIL] 5. Unit tests cover success and failure paths
         -> Missing test cases: failure path

>>> Executor: working on 4 pending/failed criteria...
  [executor] Fixing issues identified by judge...

--- Judge Evaluation (iteration 2) ---
  [PASS] 1. POST /register endpoint exists
  [PASS] 2. Passwords are hashed before storage
  [PASS] 3. Email addresses are validated
  [PASS] 4. Duplicate users are rejected
  [PASS] 5. Unit tests cover success and failure paths

*** ALL CRITERIA PASSED -- Goal complete! ***

Status: SUCCESS
Completed in 2 iteration(s)
Report written to goal_report.json
```

A JSON report (`goal_report.json`) is also written with structured results.

---

## Using in Your Own Code

```python
from goalkeeper import Goal, Criterion, GoalkeeperEngine

goal = Goal(
    title="My Feature",
    description="What it should do",
    criteria=[
        Criterion("Criterion 1", verifier=my_check_fn),
        Criterion("Criterion 2", verifier=another_check_fn),
    ],
)

engine = GoalkeeperEngine()
result = engine.run(goal, my_executor_fn)
print("Complete!" if result.is_complete else "Failed")
```

Each verifier is a `Callable[[dict], tuple[bool, str]]` that receives the
goal's `artifacts` dict and returns `(passed, feedback)`.
