---
name: auto_project_builder_nextjs
description: |
  Autonomously build complete Next.js + shadcn/ui + SQLite web projects from generated ideas using Claude Code. Generates project concepts, scaffolds the full stack, and produces runnable applications.
  Triggers: auto build nextjs project, autonomous project builder, generate nextjs app from idea, scaffold shadcn sqlite app, auto-project-builder
---

# Auto Project Builder (Next.js + shadcn/ui + SQLite)

Autonomously generate and build complete web applications using Next.js, shadcn/ui, and SQLite from a single idea or prompt. This skill lets Claude Code act as an autonomous agent that conceives project ideas and builds them end-to-end.

## When to use

- "Autonomously build a Next.js web app from scratch"
- "Generate a project idea and scaffold it with shadcn/ui and SQLite"
- "Use auto-project-builder to create a complete web application"
- "Build me a full Next.js + SQLite app from this concept"
- "Auto-generate a web project with a UI and database"

## How to use

### 1. Clone and set up the builder

```bash
git clone https://github.com/hongmacho/auto-project-builder.git
cd auto-project-builder
```

### 2. Run the autonomous build process

The builder autonomously:

1. **Idea Generation** — Generates or accepts a project concept
2. **Project Scaffolding** — Creates a Next.js project with TypeScript
3. **UI Setup** — Installs and configures shadcn/ui components
4. **Database Layer** — Sets up SQLite with schema and data access
5. **Feature Implementation** — Builds out pages, API routes, and components
6. **Verification** — Ensures the project builds and runs correctly

```bash
# Run the builder (uses Claude Code as the autonomous agent)
./run.sh
```

### 3. Output structure

The generated project includes:
- Next.js app with TypeScript and App Router
- shadcn/ui components for polished UI
- SQLite database with schema and seed data
- API routes for data operations
- Fully functional, runnable application

### Tips

- Provide a specific idea for more targeted output, or let it generate one autonomously
- The builder uses shell scripts to orchestrate the Claude Code agent
- Review generated code before deploying to production
- Each run produces an independent, self-contained Next.js project
- Works best with Claude Code configured with appropriate permissions for file creation and command execution

## References

- Source: [hongmacho/auto-project-builder](https://github.com/hongmacho/auto-project-builder)
- Stack: Next.js, TypeScript, shadcn/ui, SQLite, Shell
- Topics: ai-agent, autonomous, claude-code, claude-skill, nextjs, shadcn-ui, sqlite
