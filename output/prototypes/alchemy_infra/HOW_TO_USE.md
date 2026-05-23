# How to Use: alchemy-infra

## What it is

A **Claude Code skill** (SKILL.md format). When installed, Claude Code automatically scaffolds Alchemy infrastructure files into your project when you use certain trigger phrases.

## Install the skill

### Option A: via skills.sh (one command)

```bash
npx skills.sh install aashirjaved/alchemy-infra
```

This drops the SKILL.md into your Claude Code skills directory automatically.

### Option B: manual install

```bash
# Clone the repo
git clone https://github.com/aashirjaved/alchemy-infra.git

# Copy the skill file into Claude Code's skills directory
mkdir -p ~/.claude/skills/alchemy-infra
cp alchemy-infra/SKILL.md ~/.claude/skills/alchemy-infra/SKILL.md
```

### Option C: project-local skill

```bash
mkdir -p .claude/skills/alchemy-infra
# Place the SKILL.md inside that directory
```

## Trigger phrases

Once installed, say any of these in Claude Code:

- "Set up Alchemy infrastructure in this project"
- "Add Infrastructure-as-Code with TypeScript"
- "Scaffold AWS or Cloudflare infrastructure"
- "Deploy Cloudflare Workers with Alchemy"
- "Add IaC to this codebase with secret hygiene"

Claude will then scaffold the infra files directly into your working project.

## First 60 seconds

```
You: "Set up alchemy in this project"

Claude Code:
  1. npm install alchemy
  2. Creates alchemy.config.ts with your app name
  3. Creates infra/resources/worker.ts (Cloudflare Worker)
  4. Creates infra/resources/bucket.ts (AWS S3)
  5. Creates .env.example with secret placeholders
  6. Updates .gitignore with .env, .alchemy/, *.pem, *.key

You see:
  alchemy.config.ts        ← main IaC entry point
  infra/resources/worker.ts
  infra/resources/bucket.ts
  .env.example             ← safe template, fill in real values
  .gitignore               ← secret hygiene rules added

Next: cp .env.example .env && fill in secrets && npx alchemy deploy
```

## Running this demo locally

No cloud credentials needed:

```bash
bash run.sh
```

This scaffolds a `demo-project/` directory, validates secret hygiene, and shows a mock deploy plan.

## Prerequisites for real deployment

- Node.js 18+
- `npm install alchemy` in your project
- For AWS resources: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env`
- For Cloudflare resources: `CLOUDFLARE_API_TOKEN` in `.env`
