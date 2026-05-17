#!/usr/bin/env node
/**
 * taw-computer MCP Server — Capability Demo (no Docker required)
 *
 * Simulates the MCP tool-call flow that an AI agent would use when connected
 * to the taw-computer server, showing the 30+ tools available and typical
 * request/response patterns.
 */

const TOOLS = [
  // Browser automation
  { name: "browser_navigate", category: "Browser", desc: "Navigate to a URL" },
  { name: "browser_click", category: "Browser", desc: "Click an element by selector" },
  { name: "browser_type", category: "Browser", desc: "Type text into an input field" },
  { name: "browser_screenshot", category: "Browser", desc: "Capture page screenshot (PNG)" },
  { name: "browser_get_text", category: "Browser", desc: "Extract visible text content" },
  { name: "browser_get_html", category: "Browser", desc: "Get page HTML source" },
  { name: "browser_evaluate", category: "Browser", desc: "Run JavaScript in page context" },
  { name: "browser_wait", category: "Browser", desc: "Wait for selector or timeout" },
  { name: "browser_scroll", category: "Browser", desc: "Scroll page by pixels or to element" },
  { name: "browser_select", category: "Browser", desc: "Select dropdown option" },
  { name: "browser_back", category: "Browser", desc: "Navigate back" },
  { name: "browser_forward", category: "Browser", desc: "Navigate forward" },
  { name: "browser_tabs", category: "Browser", desc: "List open browser tabs" },
  { name: "browser_new_tab", category: "Browser", desc: "Open a new tab" },
  { name: "browser_close_tab", category: "Browser", desc: "Close current tab" },
  // Desktop control
  { name: "desktop_screenshot", category: "Desktop", desc: "Capture full desktop screenshot" },
  { name: "desktop_mouse_move", category: "Desktop", desc: "Move mouse to coordinates" },
  { name: "desktop_mouse_click", category: "Desktop", desc: "Click at coordinates" },
  { name: "desktop_mouse_double_click", category: "Desktop", desc: "Double-click at coordinates" },
  { name: "desktop_keyboard_type", category: "Desktop", desc: "Type text via keyboard" },
  { name: "desktop_keyboard_key", category: "Desktop", desc: "Press a key combination" },
  { name: "desktop_drag", category: "Desktop", desc: "Drag from point A to B" },
  // File operations
  { name: "file_read", category: "File", desc: "Read file contents" },
  { name: "file_write", category: "File", desc: "Write content to file" },
  { name: "file_list", category: "File", desc: "List directory contents" },
  { name: "file_delete", category: "File", desc: "Delete a file" },
  { name: "file_exists", category: "File", desc: "Check if file exists" },
  // Shell
  { name: "shell_exec", category: "Shell", desc: "Execute shell command" },
  // Window management
  { name: "window_list", category: "Window", desc: "List open windows" },
  { name: "window_focus", category: "Window", desc: "Focus a window by title/id" },
  { name: "window_resize", category: "Window", desc: "Resize a window" },
  { name: "window_close", category: "Window", desc: "Close a window" },
];

// Simulated MCP session showing a realistic multi-step workflow
const WORKFLOW_STEPS = [
  {
    description: "Agent opens browser and navigates to target site",
    tool: "browser_navigate",
    input: { url: "https://news.ycombinator.com" },
    output: { success: true, url: "https://news.ycombinator.com", title: "Hacker News", status: 200 },
  },
  {
    description: "Agent takes a screenshot to understand the page layout",
    tool: "browser_screenshot",
    input: { format: "png", full_page: false },
    output: { success: true, path: "/tmp/screenshots/page_001.png", width: 1280, height: 720, size_bytes: 184320 },
  },
  {
    description: "Agent extracts the top stories text",
    tool: "browser_get_text",
    input: { selector: ".titleline" },
    output: {
      success: true,
      text: [
        "1. Show HN: I built an open-source MCP server for computer control",
        "2. The future of AI agents is sandboxed environments",
        "3. Docker-based development environments are eating the world",
        "4. Why browser automation needs a protocol layer",
        "5. Playwright vs Puppeteer in 2026: benchmark results",
      ].join("\n"),
    },
  },
  {
    description: "Agent clicks on the first story link",
    tool: "browser_click",
    input: { selector: ".titleline a:first-child" },
    output: { success: true, navigated: true, new_url: "https://example.com/show-hn-mcp-server" },
  },
  {
    description: "Agent runs a shell command inside the sandbox",
    tool: "shell_exec",
    input: { command: "uname -a && cat /etc/os-release | head -5" },
    output: {
      success: true,
      stdout: "Linux taw-sandbox 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux\nNAME=\"Ubuntu\"\nVERSION=\"22.04.3 LTS (Jammy Jellyfish)\"\nID=ubuntu\nID_LIKE=debian\nVERSION_ID=\"22.04\"",
      stderr: "",
      exit_code: 0,
    },
  },
  {
    description: "Agent writes extracted data to a file in the sandbox",
    tool: "file_write",
    input: { path: "/home/user/output/top_stories.txt", content: "Top 5 HN stories extracted..." },
    output: { success: true, path: "/home/user/output/top_stories.txt", bytes_written: 142 },
  },
  {
    description: "Agent takes a desktop screenshot to show full environment",
    tool: "desktop_screenshot",
    input: {},
    output: { success: true, path: "/tmp/screenshots/desktop_001.png", width: 1920, height: 1080, size_bytes: 412672 },
  },
];

// ─── Main output ──────────────────────────────────────────────────────────────

function printHeader() {
  console.log("╔══════════════════════════════════════════════════════════════════╗");
  console.log("║   taw-computer MCP Server — Capability & Workflow Demo          ║");
  console.log("║   Give any AI a real Ubuntu computer with 30+ MCP tools         ║");
  console.log("╚══════════════════════════════════════════════════════════════════╝");
  console.log();
}

function printToolCatalog() {
  console.log("┌─────────────────────────────────────────────────────────────────┐");
  console.log("│  AVAILABLE TOOLS (grouped by category)                          │");
  console.log("└─────────────────────────────────────────────────────────────────┘");

  const categories = {};
  for (const tool of TOOLS) {
    if (!categories[tool.category]) categories[tool.category] = [];
    categories[tool.category].push(tool);
  }

  for (const [cat, tools] of Object.entries(categories)) {
    console.log(`\n  ▸ ${cat} (${tools.length} tools)`);
    for (const t of tools) {
      console.log(`      ${t.name.padEnd(30)} ${t.desc}`);
    }
  }
  console.log(`\n  Total: ${TOOLS.length} tools across ${Object.keys(categories).length} categories\n`);
}

function printWorkflow() {
  console.log("┌─────────────────────────────────────────────────────────────────┐");
  console.log("│  SIMULATED WORKFLOW: Scrape Hacker News top stories             │");
  console.log("└─────────────────────────────────────────────────────────────────┘\n");

  for (let i = 0; i < WORKFLOW_STEPS.length; i++) {
    const step = WORKFLOW_STEPS[i];
    console.log(`  Step ${i + 1}: ${step.description}`);
    console.log(`  ┌── Tool: ${step.tool}`);
    console.log(`  │   Input:  ${JSON.stringify(step.input)}`);
    console.log(`  │   Output: ${JSON.stringify(step.output)}`);
    console.log(`  └──`);
    console.log();
  }
}

function printMcpConfig() {
  console.log("┌─────────────────────────────────────────────────────────────────┐");
  console.log("│  MCP SERVER CONFIG (paste into ~/.claude.json mcpServers)       │");
  console.log("└─────────────────────────────────────────────────────────────────┘\n");

  const config = {
    "taw-computer": {
      command: "npx",
      args: ["-y", "@the-agents-work/taw-computer"],
      env: {},
    },
  };
  console.log(JSON.stringify(config, null, 2));
  console.log();
}

function printSummary() {
  console.log("┌─────────────────────────────────────────────────────────────────┐");
  console.log("│  WHY THIS MATTERS                                               │");
  console.log("└─────────────────────────────────────────────────────────────────┘\n");
  console.log("  • Gives Claude (or any MCP client) a full Ubuntu desktop + browser");
  console.log("  • All execution is sandboxed in Docker — safe for automation");
  console.log("  • 30+ tools cover browser, desktop, file, shell, and window ops");
  console.log("  • Enables: web scraping, form filling, GUI testing, data extraction");
  console.log("  • Comparable to Anthropic's computer-use, but open-source & extensible");
  console.log();
  console.log("  To run for real: docker compose up -d && add MCP config above.");
  console.log();
}

// ─── Run ──────────────────────────────────────────────────────────────────────
printHeader();
printToolCatalog();
printWorkflow();
printMcpConfig();
printSummary();
