#!/usr/bin/env node
/**
 * Mock demo of the Claude WhatsApp/Telegram bot.
 * Simulates the full message-handling pipeline without requiring
 * API keys, WhatsApp auth, or Telegram tokens.
 */

const BOLD = "\x1b[1m";
const DIM = "\x1b[2m";
const GREEN = "\x1b[32m";
const CYAN = "\x1b[36m";
const YELLOW = "\x1b[33m";
const MAGENTA = "\x1b[35m";
const RESET = "\x1b[0m";
const CHECK = "\u2713";

function log(msg) {
  console.log(msg);
}

function header(title) {
  const line = "=".repeat(60);
  log(`\n${CYAN}${line}${RESET}`);
  log(`${BOLD}${CYAN}  ${title}${RESET}`);
  log(`${CYAN}${line}${RESET}\n`);
}

function step(label) {
  log(`${DIM}--- ${label} ---${RESET}`);
}

function userMsg(platform, user, msg) {
  const icon = platform === "WhatsApp" ? "WA" : "TG";
  log(`  ${GREEN}[${icon}] ${user}:${RESET} ${msg}`);
}

function botReply(msg, tools) {
  log(`  ${MAGENTA}[Bot]:${RESET} ${msg}`);
  if (tools && tools.length > 0) {
    log(`  ${DIM}  tools used: ${tools.join(", ")}${RESET}`);
  }
}

function status(msg) {
  log(`  ${YELLOW}${CHECK} ${msg}${RESET}`);
}

// --- Mock Anthropic client ---
class MockAnthropicClient {
  constructor() {
    this.messages = { create: this._create.bind(this) };
    this._callCount = 0;
  }

  async _create({ messages, tools }) {
    this._callCount++;
    const lastUser = messages[messages.length - 1];
    const userText = this._extractText(lastUser.content);

    // Simulate tool use on first call for certain queries
    if (userText.includes("weather") && this._callCount % 2 === 1) {
      return {
        stop_reason: "tool_use",
        content: [
          {
            type: "tool_use",
            id: "tool_001",
            name: "web_search",
            input: { query: "weather today" },
          },
        ],
      };
    }

    if (userText.includes("calculate") || userText.includes("math")) {
      return {
        stop_reason: "end_turn",
        content: [
          {
            type: "tool_use",
            id: "tool_002",
            name: "calculate",
            input: { expression: "42 * 17 + 3" },
          },
          {
            type: "text",
            text: "The result of 42 x 17 + 3 = 717.",
          },
        ],
      };
    }

    // Default: just respond with text
    const responses = {
      voice: "I heard your voice message! You asked about project deadlines. The Q3 milestone is set for September 15th based on the documents you shared earlier.",
      image: "I can see a whiteboard with a system architecture diagram. It shows a microservices layout with 3 services: Auth, API Gateway, and Data Pipeline. The arrows indicate REST communication between them.",
      file: "I've analyzed your document. It's a 12-page technical spec covering the migration from PostgreSQL to CockroachDB. Key risks identified: schema compatibility (pg-specific extensions), connection pooling changes, and transaction isolation differences.",
      rag: "Based on your uploaded documents, the budget allocation for Q3 marketing is $45,000, split across digital ads ($20k), content creation ($15k), and events ($10k).",
      default: "Hello! I'm your Claude-powered assistant on this messaging platform. I can handle text, voice messages, images, and file uploads. How can I help?",
    };

    let responseKey = "default";
    if (userText.includes("Voice") || userText.includes("voice"))
      responseKey = "voice";
    else if (userText.includes("image") || userText.includes("Image"))
      responseKey = "image";
    else if (userText.includes("File") || userText.includes("file"))
      responseKey = "file";
    else if (userText.includes("budget") || userText.includes("rag"))
      responseKey = "rag";

    return {
      stop_reason: "end_turn",
      content: [{ type: "text", text: responses[responseKey] }],
    };
  }

  _extractText(content) {
    if (typeof content === "string") return content;
    if (Array.isArray(content)) {
      return content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join(" ");
    }
    return "";
  }
}

// --- Mock RAG store ---
class MockRAGStore {
  constructor() {
    this.docs = new Map();
  }
  async ingest(userId, fileName, text) {
    if (!this.docs.has(userId)) this.docs.set(userId, []);
    this.docs.get(userId).push({ fileName, text });
  }
  async search(query) {
    return [{ text: `[RAG result for "${query}": matching document chunk]` }];
  }
}

// --- Import handler ---
const { MessageHandler } = require("./message-handler");

async function runDemo() {
  header("Claude Code WhatsApp & Telegram Bot - Demo");

  log(`${BOLD}Initializing bot components...${RESET}\n`);

  const mockClient = new MockAnthropicClient();
  const ragStore = new MockRAGStore();
  const handler = new MessageHandler(mockClient, { ragStore });

  status("Anthropic client initialized (mock mode)");
  status("RAG document store ready");
  status("Message handler configured with 3 tools");
  log("");

  // ── Scenario 1: Text message on WhatsApp ──
  step("Scenario 1: Text Message (WhatsApp)");
  userMsg("WhatsApp", "Alice", "Hi! What can you do?");
  const r1 = await handler.handleMessage("alice-wa", {
    type: "text",
    content: "Hi! What can you do?",
  });
  botReply(r1.text, r1.toolsUsed);
  log("");

  // ── Scenario 2: Voice message on Telegram ──
  step("Scenario 2: Voice Message (Telegram)");
  userMsg("Telegram", "Bob", "[Voice note: 8 seconds]");
  const r2 = await handler.handleMessage("bob-tg", {
    type: "voice",
    content: Buffer.from("fake-audio-data"),
  });
  botReply(r2.text, r2.toolsUsed);
  log("");

  // ── Scenario 3: Image analysis on WhatsApp ──
  step("Scenario 3: Image/Vision Analysis (WhatsApp)");
  userMsg("WhatsApp", "Carol", "[Photo: whiteboard.jpg]");
  const r3 = await handler.handleMessage("carol-wa", {
    type: "image",
    content: Buffer.from("fake-image-data").toString("base64"),
    mimeType: "image/jpeg",
  });
  botReply(r3.text, r3.toolsUsed);
  log("");

  // ── Scenario 4: File upload + RAG ──
  step("Scenario 4: File Upload + RAG Ingestion (Telegram)");
  userMsg("Telegram", "Dave", "[File: q3-budget.pdf]");
  const r4a = await handler.handleMessage("dave-tg", {
    type: "file",
    content: "Budget document text content here...",
    mimeType: "application/pdf",
    fileName: "q3-budget.pdf",
  });
  botReply(r4a.text, r4a.toolsUsed);
  log("");

  userMsg("Telegram", "Dave", "What's the marketing budget for Q3?");
  const r4b = await handler.handleMessage("dave-tg", {
    type: "text",
    content: "What's the marketing budget for Q3? Use rag lookup.",
  });
  botReply(r4b.text, r4b.toolsUsed);
  log("");

  // ── Scenario 5: Multi-tool reasoning ──
  step("Scenario 5: Multi-Tool Reasoning (WhatsApp)");
  userMsg("WhatsApp", "Eve", "Can you calculate 42 * 17 + 3 for me?");
  const r5 = await handler.handleMessage("eve-wa", {
    type: "text",
    content: "Can you calculate 42 * 17 + 3? Use the math tool.",
  });
  botReply(r5.text, r5.toolsUsed);
  log("");

  // ── Summary ──
  header("Demo Summary");
  log(`  ${BOLD}Messages processed:${RESET}  5 conversations across 2 platforms`);
  log(`  ${BOLD}Message types:${RESET}       text, voice, image, file, RAG query`);
  log(`  ${BOLD}Tools available:${RESET}     web_search, calculate, rag_lookup`);
  log(`  ${BOLD}Conversations:${RESET}       ${handler.conversations.size} active user sessions`);
  log(`  ${BOLD}RAG documents:${RESET}       ${ragStore.docs.size} user(s) with ingested files`);
  log(`  ${BOLD}API calls (mock):${RESET}    ${mockClient._callCount}`);
  log("");
  log(`  ${GREEN}${CHECK} All scenarios completed successfully.${RESET}`);
  log(`  ${DIM}To run with real APIs, set ANTHROPIC_API_KEY in .env${RESET}`);
  log(`  ${DIM}and TELEGRAM_BOT_TOKEN for Telegram support.${RESET}\n`);
}

runDemo().catch((err) => {
  console.error("Demo failed:", err);
  process.exit(1);
});
