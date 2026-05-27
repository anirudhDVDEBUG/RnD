#!/usr/bin/env node
/**
 * Basic tests for the Pi Plugin router.
 */

const { PiPluginRouter } = require("./pi_plugin");

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log(`  PASS  ${label}`);
    passed++;
  } else {
    console.log(`  FAIL  ${label}`);
    failed++;
  }
}

async function runTests() {
  console.log("Running Pi Plugin tests...\n");

  const router = new PiPluginRouter();

  // Parse tests
  const p1 = router.parse("/pi:review some code");
  assert(p1 && p1.command === "review", "parse /pi:review");
  assert(p1 && p1.payload === "some code", "parse payload");

  const p2 = router.parse("/pi:rescue stuck task");
  assert(p2 && p2.command === "rescue", "parse /pi:rescue");

  const p3 = router.parse("not a command");
  assert(p3 === null, "parse rejects non-/pi: input");

  // Route tests
  const r1 = await router.route("/pi:review code");
  assert(r1.model === "deepseek-v4", "route uses correct model");
  assert(r1.result.findings.length === 3, "review returns 3 findings");

  const r2 = await router.route("/pi:rescue loop bug");
  assert(r2.result.diagnosis.includes("infinite loop"), "rescue diagnoses loop");

  const r3 = await router.route("/pi:explain handler");
  assert(r3.result.explanation.length > 0, "explain returns explanation");

  const r4 = await router.route("/pi:refactor block");
  assert(r4.result.suggestions.length === 3, "refactor returns 3 suggestions");

  // Error test
  try {
    await router.route("/pi:unknown test");
    assert(false, "unknown command throws");
  } catch (e) {
    assert(e.message.includes("Unknown command"), "unknown command throws");
  }

  // List commands
  const cmds = router.listCommands();
  assert(cmds.length === 4, "listCommands returns 4 commands");

  console.log(`\nResults: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

runTests();
