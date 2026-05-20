/**
 * server.js — Local Express server for the Draftspect Office Add-in demo.
 * Serves the taskpane UI and handles API routes for document operations
 * and Claude Code chat.
 */

const express = require("express");
const path = require("path");
const { OfficeBridge } = require("./office-bridge");
const { ClaudeRunner } = require("./claude-runner");

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const bridge = new OfficeBridge();
const claude = new ClaudeRunner({
  demo: true,
  contextPaths: [process.cwd()],
});

// --- Word document endpoints ---

app.get("/api/word/text", async (req, res) => {
  const text = await bridge.getDocumentText();
  res.json({ text });
});

app.post("/api/word/insert", async (req, res) => {
  const { text, location } = req.body;
  const result = await bridge.insertText(text, location);
  res.json(result);
});

app.post("/api/word/replace", async (req, res) => {
  const { search, replace } = req.body;
  const result = await bridge.searchAndReplace(search, replace);
  res.json(result);
});

// --- Excel workbook endpoints ---

app.get("/api/excel/sheets", async (req, res) => {
  const names = await bridge.getSheetNames();
  res.json({ sheets: names });
});

app.get("/api/excel/data/:sheet?", async (req, res) => {
  const data = await bridge.getSheetData(req.params.sheet);
  res.json({ data });
});

app.post("/api/excel/write", async (req, res) => {
  const { sheet, startCell, values } = req.body;
  const result = await bridge.writeToRange(sheet, startCell, values);
  res.json(result);
});

// --- Claude chat endpoint ---

app.post("/api/chat", async (req, res) => {
  const { message } = req.body;
  const docText = await bridge.getDocumentText();
  const sheetData = await bridge.getSheetData();

  const context = {
    wordDocument: docText.substring(0, 2000),
    excelActiveSheet: sheetData,
  };

  const response = await claude.sendMessage(message, context);

  // If there's a pending action, apply it
  if (response.action && !response.action.pending) {
    if (response.action.type === "word.replace") {
      await bridge.searchAndReplace(response.action.search, response.action.replace);
    } else if (response.action.type === "word.insert") {
      await bridge.insertText(response.action.text, response.action.location);
    }
  }

  res.json({
    reply: response.text,
    action: response.action || null,
  });
});

app.get("/api/chat/history", (req, res) => {
  res.json({ history: claude.history });
});

// --- Status / health ---

app.get("/api/status", (req, res) => {
  res.json({
    status: "running",
    mode: "demo",
    documentLoaded: true,
    sheetsAvailable: Object.keys(bridge.excelWorkbook.sheets),
    contextPaths: claude.contextPaths,
  });
});

// --- Start server ---

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(PORT, () => {
    console.log("");
    console.log("=".repeat(60));
    console.log("  Draftspect Office Add-in Demo");
    console.log("=".repeat(60));
    console.log("");
    console.log(`  Server running at http://localhost:${PORT}`);
    console.log("");
    console.log("  Mock document loaded:");
    console.log("    Word: Quarterly Business Review — Q1 2026");
    console.log("    Excel: Revenue + Expenses sheets");
    console.log("");
    console.log("  Try these in the chat:");
    console.log('    "Summarize this document"');
    console.log('    "Analyze the revenue data"');
    console.log('    "Rewrite the executive summary"');
    console.log('    "Add a risk factors section"');
    console.log("");
    console.log("  In production, this runs inside Office as a sideloaded");
    console.log("  taskpane add-in with real Office.js document access.");
    console.log("=".repeat(60));
    console.log("");
  });
}

module.exports = app;
