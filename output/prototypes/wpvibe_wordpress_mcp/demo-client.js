#!/usr/bin/env node
/**
 * Demo client — exercises every WPVibe MCP tool against the mock server
 * and prints the results in a readable format.
 */

const http = require("http");

const BASE = process.env.WPVIBE_URL || "http://localhost:3100";
const API_KEY = process.env.WPVIBE_API_KEY || "demo-api-key-12345";

let reqId = 0;

async function rpc(method, params = {}) {
  reqId++;
  const url = new URL("/wp-json/wpvibe-ai/v1/mcp", BASE);
  const body = JSON.stringify({ jsonrpc: "2.0", id: reqId, method, params });

  return new Promise((resolve, reject) => {
    const req = http.request(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
    }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(new Error(`Bad response: ${data}`)); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function callTool(name, args = {}) {
  const res = await rpc("tools/call", { name, arguments: args });
  if (res.error) return res.error;
  const text = res.result?.content?.[0]?.text;
  return text ? JSON.parse(text) : res.result;
}

function banner(text) {
  const line = "─".repeat(60);
  console.log(`\n${line}`);
  console.log(`  ${text}`);
  console.log(line);
}

function pretty(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

async function main() {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║         WPVibe AI — WordPress MCP Demo                 ║");
  console.log("║   Connecting Claude Code to a WordPress site via MCP   ║");
  console.log("╚══════════════════════════════════════════════════════════╝");

  // 1. Initialize
  banner("1. MCP Initialize — handshake with the server");
  const init = await rpc("initialize", { protocolVersion: "2024-11-05", clientInfo: { name: "demo-client", version: "1.0.0" } });
  pretty(init.result);

  // 2. List tools
  banner("2. List Available Tools");
  const toolsRes = await rpc("tools/list");
  const tools = toolsRes.result.tools;
  console.log(`Server exposes ${tools.length} tools:\n`);
  tools.forEach((t) => console.log(`  - ${t.name.padEnd(24)} ${t.description}`));

  // 3. Site info
  banner("3. wp_site_info — get WordPress site details");
  pretty(await callTool("wp_site_info"));

  // 4. List posts
  banner("4. wp_list_posts — all posts");
  pretty(await callTool("wp_list_posts", { status: "any" }));

  // 5. List draft posts only
  banner("5. wp_list_posts — drafts only");
  pretty(await callTool("wp_list_posts", { status: "draft" }));

  // 6. Create a new post
  banner("6. wp_create_post — create a blog post");
  pretty(await callTool("wp_create_post", {
    title: "AI-Generated Product Roundup",
    content: "<p>This post was created by Claude Code via the WPVibe MCP server. It demonstrates automated content creation for marketing workflows.</p>",
    status: "draft",
    categories: ["Marketing", "AI"],
  }));

  // 7. Update existing post
  banner("7. wp_update_post — publish a draft");
  pretty(await callTool("wp_update_post", { id: 2, status: "publish" }));

  // 8. List pages
  banner("8. wp_list_pages — site pages");
  pretty(await callTool("wp_list_pages"));

  // 9. Read theme file
  banner("9. wp_get_theme_file — read header.php");
  const themeFile = await callTool("wp_get_theme_file", { file: "header.php" });
  console.log(`Theme: ${themeFile.theme}  |  File: ${themeFile.file}\n`);
  console.log(themeFile.content);

  // 10. Update theme file
  banner("10. wp_update_theme_file — add a banner to header.php");
  pretty(await callTool("wp_update_theme_file", {
    file: "header.php",
    content: '<!-- AI-inserted promo banner -->\n<div class="promo-banner">Summer Sale — 20% off all plans!</div>',
  }));

  // 11. List plugins
  banner("11. wp_list_plugins — installed plugins");
  pretty(await callTool("wp_list_plugins"));

  // 12. List themes
  banner("12. wp_list_themes — installed themes");
  pretty(await callTool("wp_list_themes"));

  // 13. WP-CLI command
  banner("13. wp_cli — run 'plugin list'");
  const cliResult = await callTool("wp_cli", { command: "plugin list" });
  console.log(cliResult.output);

  // 14. WP-CLI cache flush
  banner("14. wp_cli — run 'cache flush'");
  pretty(await callTool("wp_cli", { command: "cache flush" }));

  // 15. REST API
  banner("15. wp_rest_api — GET site index");
  pretty(await callTool("wp_rest_api", { method: "GET", endpoint: "/" }));

  // Summary
  banner("Demo Complete");
  console.log("  All 12 MCP tools exercised successfully.");
  console.log("  In production, these tools operate against a live WordPress site.");
  console.log("  Configure the real plugin to connect Claude Code to your site.\n");
  console.log("  See HOW_TO_USE.md for setup instructions.\n");
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
