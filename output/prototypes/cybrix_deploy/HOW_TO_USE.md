# How to Use Cybrix Deploy

## This is a Claude Code Skill

Cybrix Deploy is a **Claude Code skill** (not a standalone CLI or MCP server). It extends Claude Code's capabilities to deploy apps to the Cybrix hosted platform.

## Install Steps

### 1. Install via Claude Plugin Marketplace

```bash
claude plugin marketplace add cybrixcc/cybrix-skills
```

### 2. Manual Installation (alternative)

Clone the skill into your Claude skills directory:

```bash
git clone https://github.com/cybrixcc/cybrix-skills.git
cp -r cybrix-skills/skills/cybrix_deploy ~/.claude/skills/cybrix_deploy/
```

Ensure `~/.claude/skills/cybrix_deploy/SKILL.md` exists with the trigger configuration.

### 3. Skill Location

The skill file lives at:
```
~/.claude/skills/cybrix_deploy/SKILL.md
```

## Trigger Phrases

The skill activates when you say things like:

- "Deploy this app to Cybrix"
- "Set up auto-deployment for this repo"
- "Host this project with Cybrix"
- "Check my Cybrix deployment status"
- "Configure Cybrix hosting for this service"

It does **NOT** trigger for:
- Local-only development
- Explicit use of other providers (Vercel, Netlify, AWS)
- General devops unrelated to deployment

## First 60 Seconds

### Input

Open Claude Code in your project directory and type:

```
Deploy this app to Cybrix
```

### What Happens

1. Cybrix skill activates and scans your project root
2. Detects framework (Dockerfile, package.json, requirements.txt, etc.)
3. Generates a deployment config (`cybrix.yaml`)
4. Pushes config and triggers deployment via Cybrix backend
5. Returns a live URL and deployment status

### Output

```
Detected: Node.js (Next.js) project
Build system: npm run build
Deploy target: cybrix.app

Deploying to Cybrix...
  - Building image... done (42s)
  - Provisioning... done (8s)
  - Health check... passed

Live at: https://my-nextjs-app.cybrix.app
Auto-deploy: enabled (branch: main)
Dashboard: https://dashboard.cybrix.app/projects/my-nextjs-app
```

## Configuration

After first deploy, a `cybrix.yaml` is created in your project root:

```yaml
name: my-nextjs-app
framework: nextjs
build_command: npm run build
start_command: npm start
port: 3000
auto_deploy:
  branch: main
  enabled: true
env:
  NODE_ENV: production
```

## Managing Deployments

```
"Check my Cybrix deployment status"    -> shows status, uptime, last deploy
"Show Cybrix logs for this app"        -> tails recent logs
"Restart my Cybrix deployment"         -> triggers restart
"Set env var DATABASE_URL=... on Cybrix" -> updates environment
```
