#!/usr/bin/env node
// setup_sample_shelf.mjs — Populate a local knowledge shelf with sample items
// Uses the knowledge-shelf MCP server via the MCP SDK client.

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const SAMPLE_ITEMS = [
  {
    name: "api-error-handling",
    title: "API Error Handling Pattern",
    content: `# API Error Handling Pattern

Use a centralized error handler middleware for Express/Koa APIs.

\`\`\`typescript
class AppError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
    this.name = 'AppError';
  }
}

function errorHandler(err, req, res, next) {
  const status = err.statusCode || 500;
  res.status(status).json({
    error: { message: err.message, code: err.name }
  });
}
\`\`\`

## When to use
- REST APIs with multiple route handlers
- Consistent JSON error responses across endpoints
- Logging and monitoring integration

## Tags
express, error-handling, middleware, typescript`,
    tags: ["express", "error-handling", "typescript"],
  },
  {
    name: "docker-compose-postgres",
    title: "Docker Compose PostgreSQL Setup",
    content: `# Docker Compose PostgreSQL Setup

Standard docker-compose snippet for local Postgres development.

\`\`\`yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
\`\`\`

## Notes
- Always use named volumes to persist data across restarts.
- Pin the major Postgres version to avoid surprise migrations.

## Tags
docker, postgres, devops`,
    tags: ["docker", "postgres", "devops"],
  },
  {
    name: "claude-code-prompt-template",
    title: "Claude Code Prompt Template",
    content: `# Claude Code Prompt Template

Reusable prompt structure for Claude Code tasks:

\`\`\`
## Context
[Describe the project, relevant files, and current state]

## Task
[Clear, specific instruction of what to build/fix/change]

## Constraints
- [Constraint 1: e.g., "Do not modify existing tests"]
- [Constraint 2: e.g., "Use existing project patterns"]

## Expected Output
[Describe the deliverable — files changed, tests passing, etc.]
\`\`\`

## When to use
- Kicking off a complex multi-file task with Claude Code
- Ensuring consistent task delegation across team members
- Reducing back-and-forth by front-loading context

## Tags
claude, prompting, workflow`,
    tags: ["claude", "prompting", "workflow"],
  },
  {
    name: "react-custom-hook-data-fetching",
    title: "React Custom Hook for Data Fetching",
    content: `# React Custom Hook — useApi

A minimal data-fetching hook with loading/error state.

\`\`\`typescript
import { useState, useEffect } from 'react';

function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(url)
      .then(r => { if (!r.ok) throw new Error(r.statusText); return r.json(); })
      .then(d => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => { if (!cancelled) { setError(e.message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}
\`\`\`

## Tags
react, hooks, typescript, data-fetching`,
    tags: ["react", "hooks", "typescript"],
  },
  {
    name: "git-rebase-workflow",
    title: "Git Rebase Workflow Checklist",
    content: `# Git Rebase Workflow

Step-by-step checklist for rebasing a feature branch onto main.

1. Ensure working tree is clean: \`git status\`
2. Fetch latest: \`git fetch origin\`
3. Rebase: \`git rebase origin/main\`
4. Resolve conflicts file-by-file, then \`git add <file>\` + \`git rebase --continue\`
5. Force-push (only your branch!): \`git push --force-with-lease\`
6. Verify CI passes on the updated branch.

## Do NOT
- Force-push to main/master
- Rebase shared/public branches
- Use \`--force\` (prefer \`--force-with-lease\`)

## Tags
git, workflow, rebase`,
    tags: ["git", "workflow", "rebase"],
  },
];

async function main() {
  console.log("=== Setting up Knowledge Shelf with sample items ===\n");

  const transport = new StdioClientTransport({
    command: "npx",
    args: ["-y", "knowledge-shelf"],
  });

  const client = new Client(
    { name: "shelf-setup", version: "1.0.0" },
    { capabilities: {} }
  );

  await client.connect(transport);
  console.log("Connected to knowledge-shelf MCP server.\n");

  // Discover available tools
  const { tools } = await client.listTools();
  const toolNames = tools.map((t) => t.name);
  console.log("Available tools:", toolNames.join(", "), "\n");

  // Try to add items — look for a create/add/save tool
  const addTool =
    toolNames.find((n) => /add|create|save|put|write|store|upsert/i.test(n)) ||
    null;

  if (addTool) {
    for (const item of SAMPLE_ITEMS) {
      console.log(`  Adding: "${item.title}" ...`);
      try {
        await client.callTool({
          name: addTool,
          arguments: {
            name: item.name,
            title: item.title,
            content: item.content,
            tags: item.tags,
          },
        });
        console.log(`    -> OK`);
      } catch (e) {
        // Try alternate argument shapes
        try {
          await client.callTool({
            name: addTool,
            arguments: {
              key: item.name,
              value: item.content,
              metadata: { title: item.title, tags: item.tags },
            },
          });
          console.log(`    -> OK (alt args)`);
        } catch (e2) {
          console.log(`    -> Could not add (${e2.message})`);
        }
      }
    }
  } else {
    console.log(
      "No add/create tool found. The server may use filesystem-based storage."
    );
    console.log("Available tools are:", toolNames.join(", "));
  }

  await client.close();
  console.log("\nSetup complete.");
}

main().catch((err) => {
  console.error("Setup error:", err.message);
  process.exit(1);
});
