/**
 * claude-runner.js — Manages Claude Code CLI sessions.
 * In production, spawns the real `claude` CLI process.
 * In demo mode, returns mock responses that show what the integration does.
 */

const { EventEmitter } = require("events");

class ClaudeRunner extends EventEmitter {
  constructor(options = {}) {
    super();
    this.demo = options.demo !== false;
    this.contextPaths = options.contextPaths || [];
    this.history = [];
  }

  /**
   * In production: spawn("claude", ["--print", "--verbose"], { cwd, stdio: ["pipe","pipe","pipe"] })
   * In demo: return mock responses based on the prompt.
   */
  async sendMessage(prompt, documentContext) {
    this.history.push({ role: "user", content: prompt });

    if (this.demo) {
      const response = await this._mockResponse(prompt, documentContext);
      this.history.push({ role: "assistant", content: response.text });
      return response;
    }

    // Production path (not executed in demo)
    return this._spawnClaude(prompt, documentContext);
  }

  async _mockResponse(prompt, docCtx) {
    // Simulate processing delay
    await new Promise(r => setTimeout(r, 300));

    const lower = prompt.toLowerCase();

    // Summarize document
    if (lower.includes("summar")) {
      return {
        text: "Here's a summary of your document:\n\n" +
          "**Q1 2026 Business Review Highlights:**\n" +
          "- Revenue grew 12% YoY to $4.2M ARR\n" +
          "- Net Revenue Retention at 118%, CAC payback improved to 14 months\n" +
          "- 3 major features shipped (analytics dashboard, API v2, mobile redesign)\n" +
          "- Key challenge: enterprise deal cycles lengthened ~2 weeks\n" +
          "- Next quarter focus: self-serve onboarding, EMEA expansion, API latency improvements",
        action: null,
      };
    }

    // Edit / rewrite request
    if (lower.includes("rewrite") || lower.includes("edit") || lower.includes("improve")) {
      return {
        text: "I've drafted an improved version of the Executive Summary:\n\n" +
          "> Q1 2026 delivered strong results: ARR reached $4.2M (+12% YoY) with net revenue retention " +
          "of 118%. We reduced customer acquisition costs by 8% while growing lifetime value 15%. " +
          "Three major product launches — the analytics dashboard, API v2, and mobile redesign — " +
          "strengthened our platform. Next quarter, we're prioritizing self-serve onboarding and EMEA expansion.\n\n" +
          "Shall I apply this change to the document?",
        action: {
          type: "word.replace",
          search: "Revenue grew 12% year-over-year",
          replace: "Q1 2026 delivered strong results: ARR reached $4.2M (+12% YoY)",
          pending: true,
        },
      };
    }

    // Analyze Excel data
    if (lower.includes("analyz") || lower.includes("data") || lower.includes("numbers") || lower.includes("revenue")) {
      return {
        text: "**Revenue Analysis (Q1 2026):**\n\n" +
          "| Metric | Value | Trend |\n" +
          "|--------|-------|-------|\n" +
          "| ARR Growth (Jan→Mar) | +9.1% | Accelerating |\n" +
          "| Avg New Customers/mo | 52.7 | Growing |\n" +
          "| Churn Rate Trend | 1.8% → 1.2% | Improving |\n" +
          "| MRR (March) | $350K | +9.1% from Jan |\n\n" +
          "The churn rate improvement is particularly notable — dropping from 1.8% to 1.2% " +
          "in one quarter suggests strong product-market fit in the new cohorts.\n\n" +
          "Budget variance is net positive at +$18,500, primarily from Sales & Marketing underspend.",
        action: null,
      };
    }

    // Add content
    if (lower.includes("add") || lower.includes("append") || lower.includes("insert")) {
      return {
        text: "I can add a new section to the document. Here's what I'd insert:\n\n" +
          "**Risk Factors**\n" +
          "- Macro headwinds may slow enterprise expansion in H2\n" +
          "- Key engineering hires needed for EMEA infrastructure\n" +
          "- Mobile support load may require dedicated team allocation\n\n" +
          "Want me to insert this after the Challenges section?",
        action: {
          type: "word.insert",
          text: "\nRisk Factors\n- Macro headwinds may slow enterprise expansion in H2\n- Key engineering hires needed for EMEA infrastructure\n- Mobile support load may require dedicated team allocation\n",
          location: "end",
          pending: true,
        },
      };
    }

    // Default
    return {
      text: "I can see your document content and any context folders you've pointed me at. " +
        "Try asking me to:\n" +
        "- **Summarize** the document\n" +
        "- **Rewrite** or improve a section\n" +
        "- **Analyze** the data in your spreadsheet\n" +
        "- **Add** new content based on context\n\n" +
        "I have full read/write access to the active document and can reference " +
        `${this.contextPaths.length || "any"} local context folders.`,
      action: null,
    };
  }

  _spawnClaude(prompt, docCtx) {
    // Production implementation would use child_process.spawn
    // const { spawn } = require("child_process");
    // const proc = spawn("claude", ["--print", "--verbose"], { ... });
    throw new Error("Production Claude runner requires claude CLI installed");
  }
}

module.exports = { ClaudeRunner };
