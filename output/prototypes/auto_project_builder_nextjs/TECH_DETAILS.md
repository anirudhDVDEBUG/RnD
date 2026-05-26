# Technical Details: Auto Project Builder

## What It Does

The [auto-project-builder](https://github.com/hongmacho/auto-project-builder) is a shell-orchestrated Claude Code skill that turns a single idea (or generates one) into a complete, runnable Next.js web application. It uses Claude Code as an autonomous agent that writes every file — from `package.json` and TypeScript config to database schemas, API routes, and React components. The output is a self-contained project directory you can `npm install && npm run dev` immediately.

This demo (`src/builder.mjs`) replicates the exact 6-stage pipeline the real tool follows, producing real files on disk, but without requiring Claude Code or any API keys. It serves as a reference implementation showing the structure and output format.

## Architecture

### Pipeline Stages

```
[Idea Generation] → [Project Scaffolding] → [UI Setup] → [Database Layer] → [Feature Build] → [Verification]
```

1. **Idea Generation** — Picks or generates a project concept with named entities (e.g., `Bookmark`, `Tag`).
2. **Project Scaffolding** — Creates `package.json`, `tsconfig.json`, `next.config.js`, `tailwind.config.ts`, `postcss.config.js`.
3. **UI Setup** — Writes shadcn/ui-style components (Button, Card, Input) with the `cn()` utility and CSS variables.
4. **Database Layer** — Generates `src/lib/db.ts` with `better-sqlite3` init, schema creation, and seed data.
5. **Feature Build** — Writes App Router layout, pages, and API routes (`GET`, `POST`) tied to the entities.
6. **Verification** — Checks all expected files exist and reports pass/fail.

### Key Files

| File | Purpose |
|------|---------|
| `src/builder.mjs` | Main pipeline — generates the project |
| `src/preview-server.mjs` | Static HTML preview server (no deps) |
| `run.sh` | Entry point — runs the builder |
| `SKILL.md` | Claude Code skill definition |
| `generated_project/` | Output directory (created at runtime) |

### Data Flow

```
run.sh
  └─ node src/builder.mjs
       ├─ pickIdea()        → selects from 5 built-in concepts
       ├─ scaffold(idea)    → writes config files to generated_project/
       ├─ setupUI(idea)     → writes component files
       ├─ setupDatabase()   → writes db.ts with schema
       ├─ buildFeatures()   → writes pages + API routes
       └─ verify()          → checks file existence
```

### Dependencies

- **Runtime:** Node.js >= 18 (uses ES modules, `fs`, `path`, `http`)
- **Generated project deps:** Next.js 14, React 18, better-sqlite3, Tailwind CSS, lucide-react, class-variance-authority, clsx, tailwind-merge
- **Demo itself:** Zero npm dependencies (pure Node.js)

### Model Calls

The demo makes **zero** API/model calls. The real `auto-project-builder` delegates all code generation to Claude Code CLI, which calls Anthropic's API. The shell scripts in the source repo orchestrate Claude Code with specific prompts for each pipeline stage.

## Limitations

- **Demo is deterministic** — picks from 5 hardcoded ideas rather than generating novel concepts via Claude.
- **No actual Claude Code integration** — the real tool requires Claude Code CLI installed and authenticated with an Anthropic API key.
- **Generated projects are templates** — the demo writes valid TypeScript but doesn't run `npm install` or `next build`, so type-checking and compilation aren't verified at demo time.
- **No iterative refinement** — the real builder can loop and fix errors; this demo is single-pass.
- **Single stack only** — locked to Next.js + shadcn/ui + SQLite. No support for other frameworks, ORMs, or databases.
- **No tests generated** — the output projects don't include test files.

## Why This Matters

For teams building Claude-driven products:

- **Agent factories:** Demonstrates the pattern of using Claude Code as an autonomous agent orchestrated by shell scripts — a lightweight alternative to complex agent frameworks. The 6-stage pipeline is a reusable template for any "generate entire project" workflow.
- **Lead-gen / marketing:** Rapidly prototype landing pages or micro-SaaS demos. Feed in a concept, get a deployable app in minutes instead of hours.
- **Internal tooling:** Spin up admin dashboards, CRUD apps, or data viewers on demand — useful for ops teams that need quick internal tools.
- **Skill composition:** This skill can be combined with other Claude Code skills (design systems, deployment, testing) to build more complete autonomous pipelines.
