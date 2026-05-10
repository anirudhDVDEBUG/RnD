# How to Use OpenWally Full-Stack Scaffold

## Option A: Run the Mock Demo (no API key)

```bash
cd openwally_fullstack_scaffold
bash run.sh
```

This runs `openwally_mock.py`, which simulates all 5 agents and writes a real file tree to `generated_project/`. Useful for evaluating the pipeline concept before committing to API costs.

## Option B: Run Real OpenWally

### 1. Install

```bash
git clone https://github.com/abhijitmishra87/openwally.git
cd openwally
pip install -r requirements.txt
```

Key dependencies: `crewai`, `anthropic`, `inspect-ai`, `fastapi`.

### 2. Configure

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Optional: use local models via Ollama instead
# export OLLAMA_BASE_URL="http://localhost:11434"
```

### 3. Run

```bash
python main.py --idea "A task management app with user auth, project boards, and real-time notifications"
```

Output lands in a new directory with backend, frontend, tests, and config files.

## Option C: Use as a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/openwally_fullstack_scaffold
cp SKILL.md ~/.claude/skills/openwally_fullstack_scaffold/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code:

- "Scaffold a full-stack app from this idea"
- "Generate a complete project with backend and React frontend"
- "Use OpenWally to create a new app"
- "Turn this description into a working full-stack codebase"
- "Multi-agent code generation for a new project"

Claude will clone OpenWally, install deps, and run the pipeline for you.

## First 60 Seconds

```
# 1. Run the demo
$ bash run.sh

# 2. You see each agent fire in sequence:
[1/5] Architect Agent (System Architect)
    Designs project structure, API endpoints, and data models
    -> Designed 8 endpoints, 4 models
    -> Stack: FastAPI + React + Vite

[2/5] Backend Agent (Backend Developer)
    -> Generated 7 backend files

[3/5] Frontend Agent (Frontend Developer)
    -> Generated 12 frontend files

[4/5] Testing Agent (QA Engineer)
    -> Generated 6 test files

[5/5] Integration Agent (DevOps Engineer)
    -> Total files in scaffold: 29

# 3. Inspect the output
$ ls generated_project/
backend/  frontend/  docker-compose.yml  Makefile  README.md  .gitignore  openwally_manifest.json

$ cat generated_project/backend/main.py
# Full FastAPI app with routers, CORS, etc.

$ cat generated_project/openwally_manifest.json
# JSON manifest listing all agents, endpoints, and files
```

**Total time:** ~2 seconds (mock) or ~30-60 seconds (real, with Claude API calls).
