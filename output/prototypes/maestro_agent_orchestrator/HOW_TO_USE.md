# How to Use

## Install

```bash
git clone <this-repo> && cd maestro_agent_orchestrator
pip install -r requirements.txt   # just pyyaml
```

## This is a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
cp -r . ~/.claude/skills/maestro_agent_orchestrator/
```

**Trigger phrases** that activate it:
- "Set up multi-agent orchestration for my project"
- "Route this task to the best AI agent"
- "Coordinate Claude, Codex, and Cursor on this codebase"
- "Create agent profiles and routing rules"
- "Manage hooks and handoffs between AI coding tools"

## First 60 Seconds

**1. Run the demo (no API keys needed):**

```bash
bash run.sh
```

**2. You'll see output like:**

```
======================================================================
  DEMO 1: SINGLE-TASK ROUTING
======================================================================
  Routing 6 different tasks to the best-suited agent...

  --- Task 1 ---
  Agent:      claude
  Task:       Refactor the auth module for better testability
  Routed by:  Matched patterns: refactor (priority: high)
  Confidence: 50%
  Output:     Analyzed the task thoroughly. Proposed a modular architecture...

  --- Task 2 ---
  Agent:      codex
  Task:       Generate CRUD boilerplate for the user management API
  Routed by:  Matched patterns: generate, boilerplate, crud (priority: medium)
  Confidence: 100%
  Output:     Generated scaffolding with 4 files...
```

**3. Try routing your own task programmatically:**

```python
from maestro.loader import load_profiles, load_routing, load_hooks
from maestro.router import Router

profiles = load_profiles(".maestro/profiles")
rules, fallback = load_routing(".maestro/routing.yaml")
router = Router(rules, profiles, fallback)

agent, reason, confidence = router.route("Debug the memory leak in the worker pool")
print(f"Route to: {agent} ({reason}, {confidence:.0%})")
# -> Route to: claude (Matched patterns: debug, priority: high, 50%)
```

## Configuration

All config lives in `.maestro/`:

```
.maestro/
├── profiles/          # One YAML per agent (claude.yaml, codex.yaml, ...)
│   ├── claude.yaml
│   ├── codex.yaml
│   ├── cursor.yaml
│   ├── gemini.yaml
│   └── windsurf.yaml
├── routing.yaml       # Pattern -> agent mapping with priorities
├── hooks.yaml         # Pre/post/handoff shell commands
└── workflows/         # Multi-step agent pipelines
    └── feature_implementation.yaml
```

### Add a new agent

Create `.maestro/profiles/myagent.yaml`:

```yaml
agent: myagent
strengths:
  - testing
  - CI/CD
context_window: medium
preferred_tasks:
  - test generation
  - pipeline configuration
```

Add a routing rule in `.maestro/routing.yaml`:

```yaml
- pattern: "test|ci|pipeline|coverage"
  route_to: myagent
  priority: medium
```

### Custom workflow

Create `.maestro/workflows/my_pipeline.yaml`:

```yaml
name: my_pipeline
steps:
  - agent: claude
    task: "Analyze requirements"
    output: ".maestro/artifacts/analysis.md"
  - agent: codex
    task: "Generate implementation"
    input: ".maestro/artifacts/analysis.md"
    output: "src/"
```
