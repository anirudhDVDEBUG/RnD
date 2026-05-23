# Tech Details: alchemy-infra

## What it does

alchemy-infra is a Claude Code skill (SKILL.md format) that instructs Claude to scaffold [Alchemy](https://github.com/sam-goodwin/alchemy) infrastructure files into any TypeScript/JavaScript project. Alchemy is an Infrastructure-as-Code framework that lets you define AWS, Cloudflare, and other cloud resources in pure TypeScript — no YAML, no HCL, no separate DSL. The skill adds a strict secret hygiene layer: all secrets are referenced via `app.secret()` (pulled from environment variables at deploy time), `.env` files are git-ignored by default, and the generated `.gitignore` blocks `.alchemy/`, `*.pem`, and `*.key` patterns.

The skill itself is a prompt document — it doesn't run code. When Claude Code loads the SKILL.md, it gains the knowledge and instructions to: install the `alchemy` npm package, create config files, wire up resource definitions, and enforce the secret-hygiene invariants. The actual infrastructure provisioning happens through Alchemy's CLI (`npx alchemy deploy`), which is a separate runtime concern.

## Architecture

```
SKILL.md (prompt)
  └── Claude Code reads this on trigger phrases
        └── Generates files in user's project:
              alchemy.config.ts         ← app entry point, imports resources
              infra/resources/worker.ts ← Cloudflare Worker definition
              infra/resources/bucket.ts ← AWS S3 Bucket definition
              .env.example              ← secret template (safe to commit)
              .gitignore                ← secret hygiene rules
```

**Key files in this demo:**
- `scaffold.mjs` — Simulates the file-generation step (what Claude would do)
- `demo.mjs` — Runs scaffold + validates hygiene + shows mock deploy plan
- `run.sh` — Entry point for `bash run.sh`

**Dependencies:** None beyond Node.js (no npm install needed for the demo). Real usage requires the `alchemy` npm package.

**Data flow:** Trigger phrase → Claude reads SKILL.md → Claude generates files → User fills `.env` → `npx alchemy deploy` provisions cloud resources.

## Limitations

- **Skill is prompt-only.** It doesn't enforce hygiene at runtime — it instructs Claude to generate compliant files. A user could manually break the pattern after scaffolding.
- **No drift detection.** If someone edits the generated files to hardcode secrets, there's no automated check. You'd need a pre-commit hook or CI check for that.
- **Alchemy scope.** Supports AWS and Cloudflare primarily. GCP, Azure, and other providers depend on Alchemy's own plugin ecosystem.
- **No state management demo.** Alchemy stores deploy state in `.alchemy/` — this demo doesn't simulate that.
- **Skill.md format only.** This is not an MCP server. It extends Claude Code's behavior through prompt injection, not tool registration.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Agents that spin up infrastructure on demand need safe IaC scaffolding — this skill provides that pattern for Alchemy-based stacks. |
| **Lead-gen / marketing SaaS** | Quick deployment of Cloudflare Workers for landing pages, API endpoints, or edge functions — scaffolded in seconds via Claude. |
| **Ad creatives pipeline** | S3 buckets for asset storage + Workers for serving — the two resources this skill scaffolds out of the box. |
| **Voice AI** | Backend infra (Lambda, Workers) for voice processing pipelines can be defined in the same TypeScript codebase as the app logic. |

The core value proposition: developers using Claude Code can go from "I need infrastructure" to "deploy-ready TypeScript IaC" in one conversational turn, with secrets handled correctly by default.
