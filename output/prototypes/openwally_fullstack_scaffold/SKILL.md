---
name: openwally_fullstack_scaffold
description: |
  Use the OpenWally multi-agent AI pipeline to turn a plain-text idea into a complete, scaffolded full-stack project (backend, React UI, tests, git-ready). Powered by CrewAI and Anthropic Claude.
  Triggers: fullstack scaffold, generate full-stack project, openwally, multi-agent code generation, scaffold app from idea
---

# OpenWally Full-Stack Scaffold

Use the OpenWally multi-agent pipeline to generate a complete full-stack project from a plain-text description. OpenWally orchestrates multiple AI agents via CrewAI to produce a backend (FastAPI), React frontend, tests, and a git-ready repository.

## When to use

- "Scaffold a full-stack app from this idea"
- "Generate a complete project with backend and React frontend"
- "Use OpenWally to create a new app"
- "Turn this description into a working full-stack codebase"
- "Multi-agent code generation for a new project"

## How to use

### 1. Install OpenWally

```bash
git clone https://github.com/abhijitmishra87/openwally.git
cd openwally
pip install -r requirements.txt
```

### 2. Configure environment

Set your Anthropic API key (and optionally Ollama for local models):

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 3. Run the pipeline

Provide a plain-text idea and OpenWally's multi-agent crew will:

1. **Architect Agent** — Designs the project structure, API endpoints, and data models
2. **Backend Agent** — Generates FastAPI backend code with routes, models, and logic
3. **Frontend Agent** — Scaffolds a React UI with components and pages
4. **Testing Agent** — Creates test suites for both backend and frontend
5. **Integration Agent** — Wires everything together into a git-ready repository

```bash
python main.py --idea "A task management app with user auth, project boards, and real-time notifications"
```

### 4. Review and iterate

The output is a complete project directory with:
- FastAPI backend with API routes and data models
- React frontend with components and styling
- Test files for backend and frontend
- Git-initialized repository ready to push

### Tips

- Be specific in your idea description for better results
- The pipeline supports both Anthropic Claude and Ollama for local model usage
- Inspect AI integration allows evaluation and quality checks on generated code
- Review generated code before deploying — treat output as a strong starting point

## References

- Source: [abhijitmishra87/openwally](https://github.com/abhijitmishra87/openwally)
- Stack: Python, CrewAI, Anthropic Claude, FastAPI, React, Inspect AI
- Topics: agentic-coding, code-generation, fullstack, multi-agent, crewai
