# alchemy-infra

**Claude Code skill that scaffolds [Alchemy](https://github.com/sam-goodwin/alchemy) (Infrastructure-as-TypeScript) into any codebase with built-in secret hygiene.** One trigger phrase — "set up alchemy" — generates a deploy-ready `infra/` directory, `.env` template, and `.gitignore` rules so secrets never leak into version control.

**Headline result:** Say "scaffold IaC with TypeScript" in Claude Code and get a complete Alchemy project skeleton — Cloudflare Workers + AWS S3 resources defined in TypeScript, secret references via `app.secret()`, and gitignore rules — in under 10 seconds.

| Doc | What's inside |
|-----|--------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, trigger phrases, first 60 seconds |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations |

```bash
bash run.sh   # runs the full demo locally, no API keys needed
```
