---
name: alchemy-infra
description: |
  Scaffolds Alchemy (Infrastructure-as-TypeScript) into any codebase with strict secret hygiene.
  Triggers: "set up alchemy", "add infrastructure as code", "scaffold IaC with TypeScript", "deploy to AWS or Cloudflare", "add alchemy infra to this project"
---

# Alchemy Infrastructure Scaffolding

Agent skill that scaffolds [Alchemy](https://github.com/sam-goodwin/alchemy) (Infrastructure-as-TypeScript) into any codebase with strict secret hygiene. Compatible with skills.sh and npx.

## When to use

- "Set up Alchemy infrastructure in this project"
- "Add Infrastructure-as-Code with TypeScript"
- "Scaffold AWS or Cloudflare infrastructure"
- "Deploy Cloudflare Workers with Alchemy"
- "Add IaC to this codebase with secret hygiene"

## How to use

1. **Install Alchemy**: Add the `alchemy` package to the project.
   ```bash
   npx skills.sh install aashirjaved/alchemy-infra
   # or manually:
   npm install alchemy
   ```

2. **Scaffold infrastructure files**: Create an `alchemy.config.ts` or `infra/` directory with TypeScript-based infrastructure definitions targeting AWS and/or Cloudflare.

3. **Configure secrets safely**: Alchemy enforces strict secret hygiene — never commit plaintext secrets. Use environment variables or Alchemy's built-in secret management:
   - Store secrets in `.env` files (git-ignored)
   - Reference secrets via `alchemy.secret()` in infrastructure code
   - Ensure `.gitignore` includes `.env`, `.alchemy/`, and any secret files

4. **Define resources in TypeScript**:
   ```typescript
   import { CloudflareWorker } from "alchemy/cloudflare";
   import { S3Bucket } from "alchemy/aws";

   const worker = new CloudflareWorker("my-worker", {
     script: "./src/worker.ts",
   });

   const bucket = new S3Bucket("my-bucket", {
     bucketName: "my-app-assets",
   });
   ```

5. **Deploy infrastructure**:
   ```bash
   npx alchemy deploy
   ```

## Key features

- **TypeScript-native IaC**: Define AWS, Cloudflare, and other cloud resources in TypeScript
- **Strict secret hygiene**: Built-in guardrails prevent accidental secret exposure
- **Cloudflare Workers support**: First-class support for deploying Workers
- **AWS integration**: Provision S3, Lambda, and other AWS resources
- **skills.sh compatible**: Install via the skills.sh ecosystem

## References

- Source: [aashirjaved/alchemy-infra](https://github.com/aashirjaved/alchemy-infra)
- Alchemy framework: [sam-goodwin/alchemy](https://github.com/sam-goodwin/alchemy)
