#!/usr/bin/env node
/**
 * demo.js — End-to-end demonstration of the Pi Plugin router.
 * No API keys required; uses mock responses to show the full flow.
 */

const { PiPluginRouter } = require("./pi_plugin");

const RESET = "\x1b[0m";
const BOLD = "\x1b[1m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const RED = "\x1b[31m";
const CYAN = "\x1b[36m";
const DIM = "\x1b[2m";

function colorSeverity(sev) {
  if (sev === "error") return RED + sev + RESET;
  if (sev === "warning") return YELLOW + sev + RESET;
  return DIM + sev + RESET;
}

function banner(text) {
  const line = "=".repeat(60);
  console.log(`\n${CYAN}${line}${RESET}`);
  console.log(`${BOLD}  ${text}${RESET}`);
  console.log(`${CYAN}${line}${RESET}\n`);
}

async function main() {
  const router = new PiPluginRouter();

  // Listen for routing events
  router.on("routing", ({ command, model }) => {
    console.log(`${DIM}  -> Routing /pi:${command} to model: ${model}${RESET}`);
  });

  // ---- Show available commands ----
  banner("Pi Plugin for Claude Code — Demo");
  console.log(`${BOLD}Available slash commands:${RESET}`);
  for (const { command, description } of router.listCommands()) {
    console.log(`  ${GREEN}${command}${RESET}  ${description}`);
  }

  // ---- Demo 1: /pi:review ----
  banner("Demo 1: /pi:review");
  console.log(`${DIM}Input:${RESET} /pi:review function getUser(id) { ... }\n`);

  const reviewResult = await router.route("/pi:review function getUser(id) { ... }");
  const r = reviewResult.result;
  console.log(`${BOLD}Review Score: ${r.score}${RESET}`);
  console.log(`${BOLD}Recommendation:${RESET} ${r.recommendation}\n`);
  console.log(`${BOLD}Findings:${RESET}`);
  for (const f of r.findings) {
    console.log(`  [${colorSeverity(f.severity)}] Line ${f.line}: ${f.message}`);
    console.log(`    ${GREEN}Fix:${RESET} ${f.suggestion}`);
  }
  console.log(`\n${DIM}Tokens used: ${reviewResult.usage.total_tokens}${RESET}`);

  // ---- Demo 2: /pi:rescue ----
  banner("Demo 2: /pi:rescue");
  console.log(`${DIM}Input:${RESET} /pi:rescue infinite loop in processItems()\n`);

  const rescueResult = await router.route("/pi:rescue infinite loop in processItems()");
  const d = rescueResult.result;
  console.log(`${BOLD}Diagnosis:${RESET} ${d.diagnosis}\n`);
  console.log(`${BOLD}Suggested fixes:${RESET}`);
  d.suggestedFix.forEach((fix, i) => console.log(`  ${i + 1}. ${fix}`));
  console.log(`  Confidence: ${GREEN}${d.confidence}${RESET}`);

  // ---- Demo 3: /pi:explain ----
  banner("Demo 3: /pi:explain");
  console.log(`${DIM}Input:${RESET} /pi:explain debounced mutation handler\n`);

  const explainResult = await router.route("/pi:explain debounced mutation handler");
  const e = explainResult.result;
  console.log(`${BOLD}Explanation:${RESET} ${e.explanation}`);
  console.log(`${BOLD}Complexity:${RESET} ${e.complexity}`);

  // ---- Demo 4: /pi:refactor ----
  banner("Demo 4: /pi:refactor");
  console.log(`${DIM}Input:${RESET} /pi:refactor validation + formatting block\n`);

  const refactorResult = await router.route("/pi:refactor validation + formatting block");
  const s = refactorResult.result;
  console.log(`${BOLD}Suggestions:${RESET}`);
  s.suggestions.forEach((sug, i) => console.log(`  ${i + 1}. ${sug}`));

  // ---- Summary ----
  banner("Summary");
  console.log(`All 4 /pi:* commands routed successfully through Pi agent (${router.config.model}).`);
  console.log(`In production, replace mock responses with live DeepSeek V4 API calls.`);
  console.log(`${DIM}See HOW_TO_USE.md for setup instructions.${RESET}\n`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
