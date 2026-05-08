#!/usr/bin/env node
/**
 * Thunderbit Web Scraper – Local Demo (mock mode)
 *
 * Simulates the two core MCP tools provided by thunderbit-mcp-server:
 *   1. scrape_url  – scrape a webpage to markdown
 *   2. extract_data – extract structured fields from a URL via AI
 *
 * No API key required: uses built-in mock responses so you can see
 * the exact shape of the data Thunderbit returns.
 */

// ── Mock data representing real Thunderbit API responses ──────────────

const MOCK_PAGES = {
  "https://example.com/products": {
    markdown: `# Acme Widget Store\n\nWelcome to our product catalog.\n\n## Products\n\n### Ultra Widget Pro\n- **Price:** $49.99\n- **Rating:** 4.8/5 (2,341 reviews)\n- **Description:** The ultimate widget for professionals. Titanium-grade build quality with AI-assisted calibration.\n- **In Stock:** Yes\n\n### Mini Widget Lite\n- **Price:** $19.99\n- **Rating:** 4.5/5 (987 reviews)\n- **Description:** Compact and affordable widget for everyday tasks. Perfect starter widget.\n- **In Stock:** Yes\n\n### Widget Enterprise X\n- **Price:** $199.99\n- **Rating:** 4.9/5 (412 reviews)\n- **Description:** Enterprise-grade widget with team collaboration features and 99.9% uptime SLA.\n- **In Stock:** Limited\n\n---\n\n*Last updated: 2026-05-08*`,
    structured: [
      {
        name: "Ultra Widget Pro",
        price: "$49.99",
        rating: "4.8/5",
        reviews: 2341,
        in_stock: true,
        description: "The ultimate widget for professionals. Titanium-grade build quality with AI-assisted calibration."
      },
      {
        name: "Mini Widget Lite",
        price: "$19.99",
        rating: "4.5/5",
        reviews: 987,
        in_stock: true,
        description: "Compact and affordable widget for everyday tasks. Perfect starter widget."
      },
      {
        name: "Widget Enterprise X",
        price: "$199.99",
        rating: "4.9/5",
        reviews: 412,
        in_stock: false,
        description: "Enterprise-grade widget with team collaboration features and 99.9% uptime SLA."
      }
    ]
  },
  "https://example.com/blog": {
    markdown: `# Acme Blog\n\n## Latest Posts\n\n### How AI is Transforming Web Scraping in 2026\n*Published: May 5, 2026 | Author: Jane Smith*\n\nTraditional scraping relied on brittle CSS selectors. Modern AI-powered scrapers like Thunderbit understand page semantics...\n\n### 5 Tips for Structured Data Extraction\n*Published: April 28, 2026 | Author: John Doe*\n\nWhen extracting product data at scale, defining clear field schemas upfront saves hours of post-processing...`,
    structured: [
      {
        title: "How AI is Transforming Web Scraping in 2026",
        date: "2026-05-05",
        author: "Jane Smith"
      },
      {
        title: "5 Tips for Structured Data Extraction",
        date: "2026-04-28",
        author: "John Doe"
      }
    ]
  }
};

// ── Tool implementations ─────────────────────────────────────────────

function scrapeUrl(url) {
  const page = MOCK_PAGES[url];
  if (!page) {
    return { success: false, error: `No mock data for URL: ${url}` };
  }
  return { success: true, url, format: "markdown", content: page.markdown };
}

function extractData(url, fields) {
  const page = MOCK_PAGES[url];
  if (!page) {
    return { success: false, error: `No mock data for URL: ${url}` };
  }
  const rows = page.structured.map(row => {
    if (fields && fields.length > 0) {
      const filtered = {};
      for (const f of fields) {
        if (f in row) filtered[f] = row[f];
      }
      return filtered;
    }
    return row;
  });
  return { success: true, url, fields_requested: fields || "all", row_count: rows.length, data: rows };
}

// ── CLI entrypoint ───────────────────────────────────────────────────

function main() {
  const divider = "═".repeat(60);

  console.log(divider);
  console.log("  Thunderbit Web Scraper – Demo (mock mode)");
  console.log(divider);
  console.log();

  // Demo 1: scrape_url
  const scrapeTarget = "https://example.com/products";
  console.log(`[1] scrape_url("${scrapeTarget}")`);
  console.log("─".repeat(60));
  const scrapeResult = scrapeUrl(scrapeTarget);
  console.log(scrapeResult.content);
  console.log();

  // Demo 2: extract_data with specific fields
  const fields = ["name", "price", "rating", "in_stock"];
  console.log(`[2] extract_data("${scrapeTarget}", fields=${JSON.stringify(fields)})`);
  console.log("─".repeat(60));
  const extractResult = extractData(scrapeTarget, fields);
  console.log(JSON.stringify(extractResult, null, 2));
  console.log();

  // Demo 3: extract_data on a different page (all fields)
  const blogUrl = "https://example.com/blog";
  console.log(`[3] extract_data("${blogUrl}", fields=all)`);
  console.log("─".repeat(60));
  const blogResult = extractData(blogUrl, null);
  console.log(JSON.stringify(blogResult, null, 2));
  console.log();

  console.log(divider);
  console.log("  All demos complete. See HOW_TO_USE.md for real API setup.");
  console.log(divider);
}

main();
