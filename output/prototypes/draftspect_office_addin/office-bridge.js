/**
 * office-bridge.js — Mock Office.js bridge for demo purposes.
 * In production, these calls go through the real Office.js API
 * inside the taskpane iframe. Here we simulate document state.
 */

class OfficeBridge {
  constructor() {
    // Simulated Word document content
    this.wordDocument = {
      body: [
        "Quarterly Business Review — Q1 2026",
        "",
        "Executive Summary",
        "Revenue grew 12% year-over-year, driven primarily by expansion in the",
        "enterprise segment. Customer acquisition cost decreased by 8% while",
        "lifetime value increased by 15%. The product team shipped 3 major features",
        "including the new analytics dashboard, API v2, and mobile redesign.",
        "",
        "Key Metrics",
        "- ARR: $4.2M (up from $3.75M)",
        "- Net Revenue Retention: 118%",
        "- CAC Payback: 14 months (improved from 16)",
        "- NPS: 62 (up from 58)",
        "",
        "Challenges",
        "- Enterprise deal cycles lengthened by ~2 weeks on average",
        "- Engineering velocity dipped in February due to infrastructure migration",
        "- Support ticket volume increased 20% following the mobile launch",
        "",
        "Next Quarter Priorities",
        "- Launch self-serve onboarding flow",
        "- Expand into EMEA market with localized pricing",
        "- Reduce P95 API latency below 200ms",
      ].join("\n"),
      selectedText: "",
    };

    // Simulated Excel workbook
    this.excelWorkbook = {
      sheets: {
        "Revenue": [
          ["Month", "ARR", "MRR", "New Customers", "Churn Rate"],
          ["Jan 2026", 3850000, 320833, 45, 0.018],
          ["Feb 2026", 3950000, 329167, 52, 0.015],
          ["Mar 2026", 4200000, 350000, 61, 0.012],
        ],
        "Expenses": [
          ["Category", "Q1 Budget", "Q1 Actual", "Variance"],
          ["Engineering", 450000, 462000, -12000],
          ["Sales & Marketing", 380000, 355000, 25000],
          ["Operations", 120000, 118500, 1500],
          ["G&A", 95000, 91000, 4000],
        ],
      },
      activeSheet: "Revenue",
      selectedRange: null,
    };
  }

  // --- Word operations ---

  async getDocumentText() {
    return this.wordDocument.body;
  }

  async getSelectedText() {
    return this.wordDocument.selectedText || "(no selection)";
  }

  async insertText(text, location = "end") {
    if (location === "replace") {
      this.wordDocument.body = text;
    } else if (location === "end") {
      this.wordDocument.body += "\n" + text;
    } else if (location === "start") {
      this.wordDocument.body = text + "\n" + this.wordDocument.body;
    }
    return { success: true, location, length: text.length };
  }

  async searchAndReplace(search, replace) {
    const original = this.wordDocument.body;
    this.wordDocument.body = original.replaceAll(search, replace);
    const count = (original.split(search).length - 1);
    return { replacements: count };
  }

  // --- Excel operations ---

  async getSheetData(sheetName) {
    const name = sheetName || this.excelWorkbook.activeSheet;
    return this.excelWorkbook.sheets[name] || [];
  }

  async getSheetNames() {
    return Object.keys(this.excelWorkbook.sheets);
  }

  async writeToRange(sheetName, startCell, values) {
    const name = sheetName || this.excelWorkbook.activeSheet;
    if (!this.excelWorkbook.sheets[name]) {
      this.excelWorkbook.sheets[name] = [];
    }
    this.excelWorkbook.sheets[name] = values;
    return { success: true, sheet: name, rows: values.length };
  }

  async addRow(sheetName, row) {
    const name = sheetName || this.excelWorkbook.activeSheet;
    if (this.excelWorkbook.sheets[name]) {
      this.excelWorkbook.sheets[name].push(row);
      return { success: true, rowIndex: this.excelWorkbook.sheets[name].length - 1 };
    }
    return { success: false, error: "Sheet not found" };
  }

  // --- Context gathering (local files) ---

  getContextSummary(paths) {
    return paths.map(p => ({
      path: p,
      type: p.endsWith("/") ? "directory" : "file",
      note: "(mock — in production, reads actual file content)",
    }));
  }
}

module.exports = { OfficeBridge };
