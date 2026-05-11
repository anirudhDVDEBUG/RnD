# How to Use — CCGX Multi-Model Workflow

## Install (this demo)

```bash
# No dependencies beyond Python 3.10+
cd ccgx_multi_model_workflow
bash run.sh
```

## Install (full ccgx-workflow from source)

```bash
git clone https://github.com/wzyxdwll/ccgx-workflow.git
cd ccgx-workflow
npm install
npm run build
```

## This is a Claude Code Skill

Drop the skill folder so Claude Code auto-detects it:

```bash
mkdir -p ~/.claude/skills/ccgx_multi_model_workflow
cp SKILL.md ~/.claude/skills/ccgx_multi_model_workflow/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code and the skill activates:

- "Set up multi-model routing for my project"
- "Route frontend tasks to Gemini and backend to Codex"
- "Configure a ccgx workflow with quality tiers"
- "Run an autonomous long-running dev workflow across models"

### What happens

Claude reads the SKILL.md, clones ccgx-workflow, configures routing rules for your repo, and starts dispatching tasks to the right model.

## First 60 Seconds

**Input** — run the demo:

```bash
bash run.sh
```

**Output** — you'll see four sections:

1. **Routing decisions** — each task classified with FE/BE signal scores and confidence:
   ```
   [1] Build a responsive React dashboard with Tailwind CSS cards and ch...
       -> Gemini  (frontend)  confidence=[##################..] 90%
          FE signals=5  BE signals=0
   ```

2. **Quality tiers** — the three tier configs (draft/standard/production) and what each enables.

3. **Workflow runs** — all 8 tasks executed at each quality tier, showing model, token count, latency, and output.

4. **JSON output** — a single task routed and returned as JSON, ready for programmatic use:
   ```json
   {
     "task": "Build a GraphQL API with Prisma ORM and Redis caching",
     "routed_to": "codex",
     "confidence": 0.95,
     "quality_tier": "production"
   }
   ```

## Using as a Library

```python
from ccgx.router import route_task
from ccgx.orchestrator import run_workflow

# Route a single task
result = route_task("Add a navbar component with CSS animations")
print(result.model)       # "gemini"
print(result.confidence)  # 0.9

# Run a batch workflow
run = run_workflow(
    tasks=["Build REST API", "Create React form"],
    quality_tier="production",
    autonomous=True,
)
for r in run.results:
    print(f"{r.routing.model}: {r.response.output}")
```

## CLI (full ccgx-workflow)

```bash
# Single task
npx ccgx-workflow run --task "Build the user dashboard"

# Autonomous long-run
npx ccgx-workflow run --autonomous

# With quality tier
npx ccgx-workflow run --task "Deploy to k8s" --tier production
```
