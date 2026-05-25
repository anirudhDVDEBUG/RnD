# Technical Details

## What it does

Cue is a lightweight CLI (TypeScript, published as `cue-ai` on npm) that manages per-directory agent profiles for Claude Code and Codex CLI. Each profile is a JSON file inside a `.cue/` directory at your project root. The profile declares which skills (SKILL.md packages), MCP servers, and plugins should be active when an AI agent operates in that directory. Cue reads the active profile and configures the agent environment before launch, so you never manually toggle tools between projects.

The core value proposition is context-switching: a backend repo loads database MCPs and API-review skills; a marketing site loads SEO skills and analytics MCPs. Profiles are version-controllable (commit `.cue/` to git) so the whole team shares the same agent configuration.

## Architecture

```
.cue/
  active.json          # { "active": "default" } — pointer to current profile
  default.json         # profile definition (skills, mcpServers, plugins, env)
  staging.json         # alternate profile
```

**Key data flow:**

1. User runs `cue init` — creates `.cue/` and a `default.json` profile.
2. `cue add skill/mcp <name>` — appends to the profile's arrays.
3. `cue use <name>` — writes `active.json` to point at the chosen profile.
4. On agent launch (shell hook or pre-launch integration), Cue reads `active.json`, loads the profile, and injects the declared skills/MCPs/plugins into the agent's configuration.

**Dependencies:** Node.js 18+. Zero runtime npm dependencies — the CLI is self-contained TypeScript compiled to JS.

**Source structure (upstream):**

| Path | Purpose |
|------|---------|
| `src/cli.ts` | CLI entry point, command parsing |
| `src/profile.ts` | Profile CRUD (init, load, save, list) |
| `src/activate.ts` | Reads active profile, generates agent config |
| `src/shell.ts` | Shell integration hooks (bash/zsh/fish) |

## Limitations

- **No remote profile sync** — profiles are local files. Sharing requires committing `.cue/` to version control.
- **Skill/MCP resolution is by name only** — Cue doesn't install or verify that a skill package or MCP server actually exists. It trusts the names you provide and passes them to the agent.
- **Shell hook required for auto-activation** — without the shell integration (`eval "$(cue hook bash)"`), you must run `cue use` manually before launching the agent.
- **No profile inheritance or composition** — you can't extend one profile from another. Each profile is a standalone definition.
- **Claude Code / Codex only** — profiles target Anthropic's agent tools. Other AI coding agents are not supported.

## Why it matters for Claude-driven products

- **Agent factories:** If you're building multi-tenant agent deployments, Cue's profile model shows how to scope agent capabilities per-workspace. Each customer's directory gets a profile with only the MCPs and skills they need.
- **Lead-gen / marketing teams:** Different campaigns can have different agent toolsets (SEO optimizer for content repos, ad-creative skills for design repos) without cross-contamination.
- **Voice AI / plugin ecosystems:** As MCP server counts grow, per-project profiles prevent tool overload — agents only see relevant servers, reducing latency and confusion.
- **Team standardization:** Committing `.cue/` profiles to git ensures every developer on the team gets the same agent configuration, reducing "works on my machine" issues with AI tooling.
