#!/usr/bin/env node
/**
 * demo.mjs — End-to-end demonstration of the alchemy-infra skill.
 *
 * 1. Runs the scaffolder on a temp directory
 * 2. Validates generated files exist and pass hygiene checks
 * 3. Shows what a mock "alchemy deploy" plan would look like
 *
 * No API keys or cloud accounts required.
 */

import { execSync } from "child_process";
import { existsSync, readFileSync, readdirSync, rmSync } from "fs";
import { join } from "path";

const DEMO_DIR = "./demo-project";
const SEP = "─".repeat(60);

// ── Step 0: Clean slate ──
if (existsSync(DEMO_DIR)) rmSync(DEMO_DIR, { recursive: true });

console.log(SEP);
console.log("  ALCHEMY-INFRA SKILL — End-to-End Demo");
console.log(SEP);

// ── Step 1: Run scaffolder ──
console.log("\n[1/3] Scaffolding infrastructure...\n");
execSync(`node scaffold.mjs ${DEMO_DIR}`, { stdio: "inherit" });

// ── Step 2: Hygiene validation ──
console.log(`\n${SEP}`);
console.log("[2/3] Secret hygiene validation\n");

const requiredFiles = [
  "alchemy.config.ts",
  ".env.example",
  ".gitignore",
  "infra/resources/worker.ts",
  "infra/resources/bucket.ts",
];

let allOk = true;
for (const f of requiredFiles) {
  const full = join(DEMO_DIR, f);
  const ok = existsSync(full);
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${f}`);
  if (!ok) allOk = false;
}

// Check .gitignore contains secret-hygiene entries
const gi = readFileSync(join(DEMO_DIR, ".gitignore"), "utf-8");
const hygienePatterns = [".env", ".alchemy/", "*.pem", "*.key"];
for (const p of hygienePatterns) {
  const found = gi.includes(p);
  console.log(`  ${found ? "PASS" : "FAIL"}  .gitignore contains "${p}"`);
  if (!found) allOk = false;
}

// Check no real secrets in config
const config = readFileSync(join(DEMO_DIR, "alchemy.config.ts"), "utf-8");
const hasHardcodedSecret = /["']sk[-_]|["']AKIA|password\s*[:=]\s*["'][^"']+/.test(config);
console.log(`  ${!hasHardcodedSecret ? "PASS" : "FAIL"}  No hardcoded secrets in alchemy.config.ts`);
if (hasHardcodedSecret) allOk = false;

// Check secrets use app.secret() pattern
const usesSecretFn = config.includes(".secret(");
console.log(`  ${usesSecretFn ? "PASS" : "FAIL"}  Secrets use app.secret() pattern`);
if (!usesSecretFn) allOk = false;

console.log(`\n  Overall: ${allOk ? "ALL CHECKS PASSED" : "SOME CHECKS FAILED"}`);

// ── Step 3: Mock deploy plan ──
console.log(`\n${SEP}`);
console.log("[3/3] Mock deployment plan (what `npx alchemy deploy` would do)\n");

const plan = [
  { action: "CREATE", resource: "CloudflareWorker", name: "api-worker", provider: "Cloudflare" },
  { action: "CREATE", resource: "S3Bucket", name: "my-app-assets", provider: "AWS" },
];

console.log("  Alchemy Deploy Plan");
console.log("  " + "─".repeat(50));
for (const item of plan) {
  console.log(`  + ${item.action.padEnd(8)} ${item.resource.padEnd(20)} ${item.name.padEnd(20)} (${item.provider})`);
}
console.log(`\n  Resources: ${plan.length} to create, 0 to update, 0 to destroy`);
console.log("  (Dry run — no cloud credentials needed for this demo)\n");

console.log(SEP);
console.log("  Demo complete. See ./demo-project/ for generated files.");
console.log(SEP + "\n");
