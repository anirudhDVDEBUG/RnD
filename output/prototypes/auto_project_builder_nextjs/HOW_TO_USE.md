# How to Use: Auto Project Builder

## Install (this demo)

```bash
# No npm install needed — runs with Node.js >= 18 (zero dependencies)
bash run.sh
```

## Install (real tool)

```bash
git clone https://github.com/hongmacho/auto-project-builder.git
cd auto-project-builder
# Requires Claude Code CLI installed and authenticated
./run.sh
```

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install it:

1. Copy the `SKILL.md` file into your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/auto_project_builder_nextjs
   cp SKILL.md ~/.claude/skills/auto_project_builder_nextjs/SKILL.md
   ```

2. **Trigger phrases** that activate the skill:
   - "auto build nextjs project"
   - "autonomous project builder"
   - "generate nextjs app from idea"
   - "scaffold shadcn sqlite app"
   - "auto-project-builder"
   - "Autonomously build a Next.js web app from scratch"
   - "Build me a full Next.js + SQLite app from this concept"

3. Once installed, Claude Code will recognize these phrases and follow the skill's multi-step pipeline.

## First 60 Seconds

```
$ bash run.sh

Auto Project Builder — Next.js + shadcn/ui + SQLite
====================================================

[IDEA]     Generated concept: "BookmarkVault"
[IDEA]       A personal bookmark manager with tags, search, and reading-list tracking
[IDEA]       Entities: Bookmark, Tag

[SCAFFOLD] Creating Next.js project structure...
[SCAFFOLD]   wrote package.json
[SCAFFOLD]   wrote tsconfig.json
[SCAFFOLD]   wrote tailwind.config.ts
[SCAFFOLD]   wrote postcss.config.js
[SCAFFOLD]   wrote next.config.js

[UI]       Setting up shadcn/ui components...
[UI]         Created: Button, Card, Input components
[UI]       shadcn/ui setup complete.

[DB]       Setting up SQLite database layer...
[DB]         Schema: bookmarks, tags
[DB]         Seed data: 3 sample rows
[DB]       Database layer complete.

[FEATURE]  Building pages, API routes, and components...
[FEATURE]    Pages: layout.tsx, page.tsx
[FEATURE]    API: /api/bookmarks (GET, POST)
[FEATURE]    Components: Button, Card, Input
[FEATURE]  Feature implementation complete.

[VERIFY]   Running verification checks...
[VERIFY]     11/11 files present
[VERIFY]   All checks passed.

[DONE]     Project "BookmarkVault" generated successfully!
[DONE]     Output directory: ./generated_project/
```

**What you get:** A complete `generated_project/` directory containing a valid Next.js app. To actually run it:

```bash
cd generated_project
npm install
npm run dev
# Open http://localhost:3000
```

## Preview Without npm install

```bash
node src/preview-server.mjs
# Opens a static HTML preview at http://localhost:3456
```

This renders the generated project's UI as plain HTML — useful for evaluating the output without installing Next.js dependencies.
