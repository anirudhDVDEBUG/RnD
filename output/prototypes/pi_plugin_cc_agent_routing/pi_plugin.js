#!/usr/bin/env node
/**
 * Pi Plugin for Claude Code — routes /pi:* slash commands
 * through the Pi coding agent (default: DeepSeek V4).
 *
 * This is a standalone simulator that demonstrates the routing
 * logic without requiring a live DeepSeek API key.
 */

const { EventEmitter } = require("events");

// --------------- Configuration ---------------

const DEFAULT_CONFIG = {
  model: process.env.PI_MODEL || "deepseek-v4",
  endpoint: process.env.PI_ENDPOINT || "https://api.deepseek.com/v1/chat/completions",
  timeout: parseInt(process.env.PI_TIMEOUT || "30000", 10),
};

// --------------- Mock Pi Agent ---------------

/**
 * Simulates a call to the Pi coding agent backend.
 * In production this would POST to DEFAULT_CONFIG.endpoint.
 */
async function callPiAgent(command, payload, config) {
  // Simulate network latency
  await new Promise((r) => setTimeout(r, 120));

  const responses = {
    review: generateReviewResponse(payload),
    rescue: generateRescueResponse(payload),
    explain: generateExplainResponse(payload),
    refactor: generateRefactorResponse(payload),
  };

  return {
    model: config.model,
    command,
    result: responses[command] || `Unknown command: /pi:${command}`,
    usage: { prompt_tokens: 340, completion_tokens: 210, total_tokens: 550 },
  };
}

function generateReviewResponse(payload) {
  return {
    summary: "Code review completed by Pi agent (DeepSeek V4)",
    findings: [
      {
        severity: "warning",
        line: 12,
        message: "Potential null dereference — `user.profile` may be undefined when account is newly created.",
        suggestion: "Add optional chaining: `user.profile?.avatar`",
      },
      {
        severity: "info",
        line: 27,
        message: "Magic number 86400 could be replaced with a named constant for readability.",
        suggestion: "const SECONDS_PER_DAY = 86400;",
      },
      {
        severity: "error",
        line: 41,
        message: "SQL query uses string concatenation — SQL injection risk.",
        suggestion: "Use parameterized queries: db.query('SELECT * FROM users WHERE id = ?', [userId])",
      },
    ],
    score: "6.5/10",
    recommendation: "Address the SQL injection issue before merging. Other items are advisory.",
  };
}

function generateRescueResponse(payload) {
  return {
    summary: "Rescue analysis completed by Pi agent (DeepSeek V4)",
    diagnosis: "The function enters an infinite loop when `items` is an empty array because the while-loop condition never becomes false.",
    suggestedFix: [
      "Add an early return: if (items.length === 0) return [];",
      "Change while(true) to while(index < items.length)",
    ],
    confidence: "high",
  };
}

function generateExplainResponse(payload) {
  return {
    summary: "Code explanation by Pi agent (DeepSeek V4)",
    explanation:
      "This function implements a debounced event handler that batches DOM mutations " +
      "using requestAnimationFrame. It collects mutations during a frame, then flushes " +
      "them in a single synchronous pass to minimise layout thrashing.",
    complexity: "O(n) per frame where n = queued mutations",
  };
}

function generateRefactorResponse(payload) {
  return {
    summary: "Refactor suggestions by Pi agent (DeepSeek V4)",
    suggestions: [
      "Extract the validation block (lines 15-38) into a dedicated `validateInput()` function.",
      "Replace the nested callbacks with async/await for readability.",
      "The three format branches share identical error handling — consolidate into a wrapper.",
    ],
  };
}

// --------------- Plugin Router ---------------

class PiPluginRouter extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.commands = new Map([
      ["review", "Route a code review through Pi agent"],
      ["rescue", "Send a stuck task to Pi for alternative fix"],
      ["explain", "Ask Pi to explain a code snippet"],
      ["refactor", "Get refactoring suggestions from Pi"],
    ]);
  }

  /** Parse a raw slash-command string like "/pi:review <code>" */
  parse(input) {
    const match = input.match(/^\/pi:(\w+)\s*([\s\S]*)$/);
    if (!match) return null;
    return { command: match[1], payload: match[2].trim() };
  }

  /** Route a parsed command to the Pi agent */
  async route(input) {
    const parsed = this.parse(input);
    if (!parsed) {
      throw new Error(`Invalid /pi: command format. Available: ${[...this.commands.keys()].map((c) => `/pi:${c}`).join(", ")}`);
    }

    const { command, payload } = parsed;
    if (!this.commands.has(command)) {
      throw new Error(`Unknown command /pi:${command}. Available: ${[...this.commands.keys()].map((c) => `/pi:${c}`).join(", ")}`);
    }

    this.emit("routing", { command, model: this.config.model });
    const result = await callPiAgent(command, payload, this.config);
    this.emit("complete", result);
    return result;
  }

  listCommands() {
    return [...this.commands.entries()].map(([cmd, desc]) => ({
      command: `/pi:${cmd}`,
      description: desc,
    }));
  }
}

// --------------- Exports ---------------

module.exports = { PiPluginRouter, callPiAgent, DEFAULT_CONFIG };
