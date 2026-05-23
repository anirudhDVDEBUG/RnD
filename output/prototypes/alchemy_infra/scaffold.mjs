#!/usr/bin/env node
/**
 * scaffold.mjs — Simulates what the alchemy-infra skill does when triggered:
 * 1. Creates an infra/ directory with TypeScript IaC definitions
 * 2. Sets up .env template and .gitignore rules for secret hygiene
 * 3. Generates an alchemy.config.ts entry point
 *
 * This is a LOCAL mock — no cloud credentials needed.
 */

import { mkdirSync, writeFileSync, existsSync, readFileSync } from "fs";
import { join } from "path";

const TARGET = process.argv[2] || "./scaffold-output";

console.log(`\n=== Alchemy Infra Scaffolder ===`);
console.log(`Target directory: ${TARGET}\n`);

// 1. Create directory structure
const dirs = [TARGET, join(TARGET, "infra"), join(TARGET, "infra", "resources")];
for (const d of dirs) {
  mkdirSync(d, { recursive: true });
  console.log(`  [dir]  ${d}/`);
}

// 2. alchemy.config.ts
const alchemyConfig = `import { app } from "alchemy";
import { CloudflareWorker } from "alchemy/cloudflare";
import { S3Bucket } from "alchemy/aws";

const myApp = await app("my-app");

// --- Cloudflare Worker ---
const worker = new CloudflareWorker("api-worker", {
  name: "api-worker",
  script: "./src/worker.ts",
  compatibilityDate: "2025-01-01",
  secrets: {
    API_KEY: myApp.secret("API_KEY"),         // pulled from env, never hardcoded
    DATABASE_URL: myApp.secret("DATABASE_URL"),
  },
});

// --- AWS S3 Bucket ---
const bucket = new S3Bucket("assets", {
  bucketName: "my-app-assets",
  versioning: true,
});

export { worker, bucket };
`;
writeFileSync(join(TARGET, "alchemy.config.ts"), alchemyConfig);
console.log(`  [file] alchemy.config.ts`);

// 3. Resource modules
const cfWorkerResource = `import { CloudflareWorker } from "alchemy/cloudflare";

export function createWorker(app: any, name: string, scriptPath: string) {
  return new CloudflareWorker(name, {
    name,
    script: scriptPath,
    compatibilityDate: "2025-01-01",
    secrets: {
      API_KEY: app.secret("API_KEY"),
    },
  });
}
`;
writeFileSync(join(TARGET, "infra", "resources", "worker.ts"), cfWorkerResource);
console.log(`  [file] infra/resources/worker.ts`);

const s3Resource = `import { S3Bucket } from "alchemy/aws";

export function createBucket(name: string, opts: { versioning?: boolean } = {}) {
  return new S3Bucket(name, {
    bucketName: name,
    versioning: opts.versioning ?? true,
  });
}
`;
writeFileSync(join(TARGET, "infra", "resources", "bucket.ts"), s3Resource);
console.log(`  [file] infra/resources/bucket.ts`);

// 4. .env.example (safe template — no real values)
const envExample = `# Alchemy Infra — Secret Template
# Copy to .env and fill in real values. NEVER commit .env itself.
API_KEY=your-api-key-here
DATABASE_URL=postgres://user:pass@host:5432/dbname
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
CLOUDFLARE_API_TOKEN=
`;
writeFileSync(join(TARGET, ".env.example"), envExample);
console.log(`  [file] .env.example`);

// 5. .gitignore additions for secret hygiene
const gitignoreBlock = `# Alchemy Infra — secret hygiene
.env
.env.*
!.env.example
.alchemy/
*.pem
*.key
`;
const giPath = join(TARGET, ".gitignore");
const existing = existsSync(giPath) ? readFileSync(giPath, "utf-8") : "";
if (!existing.includes(".alchemy/")) {
  writeFileSync(giPath, existing + "\n" + gitignoreBlock);
  console.log(`  [file] .gitignore  (secret-hygiene rules added)`);
} else {
  console.log(`  [skip] .gitignore  (already configured)`);
}

// 6. Summary
console.log(`
--- Scaffold complete ---
Files created:
  ${TARGET}/alchemy.config.ts        Main IaC entry point
  ${TARGET}/infra/resources/worker.ts Cloudflare Worker resource
  ${TARGET}/infra/resources/bucket.ts AWS S3 Bucket resource
  ${TARGET}/.env.example              Secret template (safe to commit)
  ${TARGET}/.gitignore                Secret hygiene rules

Next steps (with real Alchemy):
  1. cp ${TARGET}/.env.example ${TARGET}/.env   # fill in real secrets
  2. npm install alchemy
  3. npx alchemy deploy
`);
