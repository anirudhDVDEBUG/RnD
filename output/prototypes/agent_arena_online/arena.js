#!/usr/bin/env node
/**
 * Agent Arena Online — Local Simulator (zero dependencies)
 *
 * Simulates a competitive agent arena session where multiple AI coding agents
 * compete head-to-head on timed coding challenges. Runs entirely locally
 * with mock agents — no network or API keys needed.
 */

// ANSI color helpers
const c = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  magenta: "\x1b[35m",
  red: "\x1b[31m",
  white: "\x1b[37m",
  gray: "\x1b[90m",
};

function color(code, text) { return `${code}${text}${c.reset}`; }
function bold(text) { return color(c.bold, text); }
function gray(text) { return color(c.gray, text); }
function cyan(text) { return color(c.cyan, text); }
function green(text) { return color(c.green, text); }
function yellow(text) { return color(c.yellow, text); }
function magenta(text) { return color(c.magenta, text); }
function red(text) { return color(c.red, text); }

// Table drawing
function drawTable(headers, rows, colWidths) {
  const top    = "┌" + colWidths.map(w => "─".repeat(w)).join("┬") + "┐";
  const mid    = "├" + colWidths.map(w => "─".repeat(w)).join("┼") + "┤";
  const bottom = "└" + colWidths.map(w => "─".repeat(w)).join("┴") + "┘";

  function pad(str, width) {
    // Strip ANSI for length calculation
    const plain = str.replace(/\x1b\[[0-9;]*m/g, "");
    const padding = Math.max(0, width - plain.length - 2);
    return " " + str + " ".repeat(padding + 1);
  }

  function row(cells) {
    return "│" + cells.map((cell, i) => pad(String(cell), colWidths[i])).join("│") + "│";
  }

  const lines = [top, row(headers), mid];
  for (const r of rows) { lines.push(row(r)); }
  lines.push(bottom);
  return lines.map(l => "  " + l).join("\n");
}

// Challenge bank
const CHALLENGES = [
  { id: "CH-001", title: "FizzBuzz Variant", difficulty: "Easy",
    description: "Print 1-100, replacing multiples of 3/5/both with Fizz/Buzz/FizzBuzz.",
    testCases: 12, timeLimit: 30 },
  { id: "CH-002", title: "Balanced Parentheses", difficulty: "Medium",
    description: "Determine if a string of brackets ()[]{} is balanced.",
    testCases: 18, timeLimit: 60 },
  { id: "CH-003", title: "Shortest Path in Grid", difficulty: "Hard",
    description: "Find shortest path in a weighted NxN grid (top-left to bottom-right).",
    testCases: 25, timeLimit: 120 },
];

// Mock agents
const AGENTS = [
  { name: "Claude Code",  icon: "C", colorFn: cyan,    skill: 0.92 },
  { name: "Codex CLI",    icon: "X", colorFn: green,   skill: 0.85 },
  { name: "Open Code",    icon: "O", colorFn: yellow,  skill: 0.80 },
  { name: "Gemini Agent", icon: "G", colorFn: magenta, skill: 0.78 },
];

// Simulation
function rand(min, max) { return Math.random() * (max - min) + min; }

function simulate(agent, ch) {
  const penalty = ch.difficulty === "Easy" ? 0 : ch.difficulty === "Medium" ? 0.08 : 0.18;
  const passRate = Math.min(1, agent.skill - penalty + rand(-0.05, 0.05));
  const passed = Math.round(ch.testCases * Math.max(0, passRate));
  const timeTaken = Math.round(ch.timeLimit * rand(0.3, 0.95) * (1 - agent.skill + 0.5));
  const quality = Math.round(Math.max(40, Math.min(100, agent.skill * 100 + rand(-15, 10))));
  return { passed, total: ch.testCases, timeTaken, quality };
}

function score(result, ch) {
  const correctness = (result.passed / result.total) * 50;
  const speed = Math.max(0, (1 - result.timeTaken / ch.timeLimit)) * 30;
  const qual = (result.quality / 100) * 20;
  return Math.round(correctness + speed + qual);
}

// Display
function banner() {
  console.log();
  console.log(bold(cyan("  ╔═══════════════════════════════════════════════════╗")));
  console.log(bold(cyan("  ║")) + bold("       AGENT ARENA ONLINE — Local Simulator        ") + bold(cyan("║")));
  console.log(bold(cyan("  ║")) + gray("    Competitive agent gaming with your local CLI    ") + bold(cyan("║")));
  console.log(bold(cyan("  ╚═══════════════════════════════════════════════════╝")));
  console.log();
}

function divider(label) {
  console.log(gray("\n  " + "─".repeat(55)));
  if (label) console.log(bold(label));
  console.log(gray("  " + "─".repeat(55)));
}

// Main
function runArena() {
  banner();

  console.log("  Lobby: 4 agents connected\n");
  for (const a of AGENTS) {
    console.log("    " + a.colorFn(`[${a.icon}] ${a.name}`));
  }

  const totals = {};
  AGENTS.forEach(a => totals[a.name] = 0);

  for (let round = 0; round < CHALLENGES.length; round++) {
    const ch = CHALLENGES[round];
    divider(`  ROUND ${round + 1} / ${CHALLENGES.length}  —  ${ch.title} (${ch.difficulty})`);
    console.log(gray("  " + ch.description));
    console.log(gray(`  Time limit: ${ch.timeLimit}s  |  Test cases: ${ch.testCases}\n`));

    const results = AGENTS.map(agent => {
      const r = simulate(agent, ch);
      const s = score(r, ch);
      totals[agent.name] += s;
      return { agent, result: r, score: s };
    }).sort((a, b) => b.score - a.score);

    const headers = [bold("Agent"), bold("Tests Passed"), bold("Time"), bold("Quality"), bold("Score")];
    const rows = results.map(({ agent, result, score }) => {
      const passClr = result.passed === result.total ? green : result.passed > result.total * 0.7 ? yellow : red;
      return [
        agent.colorFn(`[${agent.icon}] ${agent.name}`),
        passClr(`${result.passed} / ${result.total}`),
        `${result.timeTaken}s`,
        `${result.quality}%`,
        bold(`${score}`),
      ];
    });

    console.log(drawTable(headers, rows, [18, 14, 8, 10, 8]));

    const w = results[0];
    console.log(`\n  Round winner: ${w.agent.colorFn(w.agent.name)} ${gray(`(${w.score} pts)`)}`);
  }

  // Final leaderboard
  divider("  FINAL LEADERBOARD");
  console.log();

  const sorted = AGENTS.map(a => ({ agent: a, total: totals[a.name] }))
    .sort((a, b) => b.total - a.total);

  const medals = ["1st", "2nd", "3rd", "4th"];
  const ratings = ["S", "A", "B", "C"];
  const rColors = [cyan, green, yellow, gray];

  const lHeaders = [bold("Rank"), bold("Agent"), bold("Total Score"), bold("Rating")];
  const lRows = sorted.map((e, i) => [
    bold(medals[i]),
    e.agent.colorFn(`[${e.agent.icon}] ${e.agent.name}`),
    bold(`${e.total}`),
    rColors[i](ratings[i]),
  ]);

  console.log(drawTable(lHeaders, lRows, [8, 20, 14, 10]));

  const champ = sorted[0];
  console.log(`\n  ${bold(cyan("Champion: " + champ.agent.name))} with ${bold(`${champ.total}`)} points!\n`);

  divider();
  console.log(gray("  This was a local simulation. To compete online:"));
  console.log("  $ npx agent-arena-online start\n");
  console.log(gray("  See HOW_TO_USE.md for full setup instructions.\n"));
}

runArena();
