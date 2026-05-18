# How to Use

## Install

```bash
cd orkestrai_multi_agent_orchestrator
pip install -r requirements.txt
```

No API keys required for the demo — it runs in mock mode by default.

To use real LLMs, copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY and/or OPENAI_API_KEY
```

## As a Claude Code Skill

Drop the skill folder into your skills directory:

```bash
cp -r skill/ ~/.claude/skills/orkestrai_multi_agent_orchestrator/
```

### Trigger phrases

- "Build a multi-agent orchestration system with FastAPI and Next.js"
- "Create an autonomous agent pipeline that coordinates multiple LLMs"
- "Set up a hackathon platform where AI agents collaborate on tasks"
- "Orchestrate multiple AI agents to break down and solve complex problems"
- "Scaffold a full-stack app with a FastAPI agent backend and React frontend"

## First 60 Seconds

```bash
$ bash run.sh

=== Orkestrai Multi-Agent Orchestrator Demo ===

Task: "Build a landing page for an AI writing assistant SaaS product"

[Orchestrator] Decomposing task...
[Planner] Breaking into subtasks:
  1. Research competitor landing pages
  2. Define page structure and copy
  3. Generate HTML/CSS code
  4. Review for quality and completeness

[Researcher] Gathering context...
  -> Found 3 competitor patterns, key themes: social proof, demo CTA, feature grid

[Coder] Generating implementation...
  -> Produced 47-line HTML landing page with hero, features, CTA sections

[Reviewer] Quality check...
  -> Score: 8.5/10 | Suggestions: Add testimonials section, improve mobile nav

=== Final Output ===
Status: COMPLETE
Agents used: 4
Total steps: 6
```

## Running the FastAPI server (with real LLMs)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
cd backend
uvicorn main:app --reload --port 8000
```

Then POST to `/orchestrate`:

```bash
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a landing page for a SaaS product", "provider": "anthropic"}'
```
