# Technical Details - Cybrix Deploy

## What It Does

Cybrix Deploy is a shell-based Claude Code skill that bridges the gap between local development and hosted deployment. When triggered, it inspects the local project structure to auto-detect the framework and build system, generates a deployment configuration, and communicates with the Cybrix hosted backend API to provision, build, and deploy the application. The skill wraps Cybrix's CLI/API operations into natural language commands that Claude can execute on behalf of the developer.

The Cybrix platform itself is a managed hosting service (similar in concept to Railway or Render) that handles container orchestration, SSL, and auto-deployment from Git webhooks. The skill acts as the glue layer that lets Claude Code orchestrate this without the user needing to learn Cybrix's CLI syntax.

## Architecture

### Key Files (in `cybrixcc/cybrix-skills` repo)

```
skills/
  cybrix_deploy/
    SKILL.md          - Trigger config and usage instructions for Claude
    deploy.sh         - Main deployment shell script
    detect.sh         - Framework/build-system detection logic
    config.sh         - cybrix.yaml generation
    status.sh         - Query deployment status
```

### Data Flow

```
User prompt -> Claude Code (skill trigger)
  -> detect.sh (scan project files)
  -> config.sh (generate cybrix.yaml)
  -> deploy.sh (call Cybrix API: build + deploy)
  -> Cybrix Backend (container build, provision, route)
  -> Return live URL to user
```

### Dependencies

- **Claude Code** with skills/plugin support
- **Cybrix account** (free tier available) with API token
- **Git** for auto-deploy webhook setup
- **curl/jq** used internally by shell scripts for API calls
- No Python/Node runtime required for the skill itself

### Model Calls

The skill itself makes zero LLM calls. It's purely shell scripts that Claude Code invokes. Claude interprets the output and presents it to the user.

## Limitations

- **Cybrix-only**: Does not deploy to other platforms. If you need Vercel/Netlify/AWS, this skill won't help.
- **Framework support**: Limited to what Cybrix's detection supports (Node.js, Python, Go, Rust, static sites, Docker). Exotic build systems may require manual `cybrix.yaml`.
- **No local preview**: This skill deploys to remote infrastructure. It doesn't run anything locally.
- **Account required**: You need a Cybrix account and API token configured (`CYBRIX_API_TOKEN` env var).
- **Closed backend**: While the skills are open-source, the Cybrix hosting backend is proprietary. You cannot self-host the deployment target.
- **Early stage**: The GitHub repo is new with limited community validation. API stability is not guaranteed.

## Why It Might Matter

### For Claude-driven product builders

1. **Agent factories**: If you're building agents that generate and ship code, Cybrix Deploy gives those agents a "deploy" action — closing the loop from code generation to live URL without human intervention.

2. **Lead-gen / marketing**: Rapid deployment of landing pages, microsites, or campaign-specific apps directly from Claude conversations. "Build me a waitlist page and deploy it" becomes a single interaction.

3. **Ad creatives**: Deploy interactive ad experiences or dynamic landing pages that A/B test variants, all orchestrated by Claude.

4. **Voice AI**: Deploy voice agent backends that need hosting — the skill lets Claude handle both the code and the infrastructure in one session.

### Competitive context

Similar to how Vercel's `v0` generates and deploys UI, Cybrix positions itself as the deployment layer for Claude Code workflows. The differentiator is the open-source skill interface that any Claude Code user can install, versus proprietary integrations.
