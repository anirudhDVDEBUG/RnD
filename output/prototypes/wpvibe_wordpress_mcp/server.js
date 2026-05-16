/**
 * Mock WPVibe AI MCP Server (zero dependencies — Node.js built-ins only)
 *
 * Simulates the SSE-based MCP endpoint that the real WPVibe WordPress plugin
 * exposes at /wp-json/wpvibe-ai/v1/mcp. Responds to MCP JSON-RPC messages
 * with realistic WordPress data so you can evaluate the tool surface without
 * a live WordPress install.
 */

const http = require("http");
const crypto = require("crypto");
const { URL } = require("url");

const PORT = process.env.PORT || 3100;
const API_KEY = process.env.WPVIBE_API_KEY || "demo-api-key-12345";

// ---------- mock data ----------

const MOCK_POSTS = [
  { id: 1, title: "Welcome to WPVibe", status: "publish", date: "2026-05-10T09:00:00", author: "admin", categories: ["Uncategorized"], excerpt: "Your AI-powered WordPress workflow starts here." },
  { id: 2, title: "Getting Started with MCP", status: "draft", date: "2026-05-12T14:30:00", author: "admin", categories: ["Tutorials"], excerpt: "Learn how to connect Claude Code to your WordPress site." },
  { id: 3, title: "Theme Customization Guide", status: "draft", date: "2026-05-14T11:00:00", author: "editor", categories: ["Tutorials", "Themes"], excerpt: "Edit theme files directly from your AI assistant." },
];

const MOCK_PAGES = [
  { id: 10, title: "Home", status: "publish", template: "front-page.php" },
  { id: 11, title: "About Us", status: "publish", template: "page.php" },
  { id: 12, title: "Contact", status: "publish", template: "page-contact.php" },
];

const MOCK_PLUGINS = [
  { name: "wpvibe-ai-mcp", title: "Vibe AI", status: "active", version: "1.2.0" },
  { name: "akismet", title: "Akismet Anti-spam", status: "active", version: "5.3.4" },
  { name: "woocommerce", title: "WooCommerce", status: "inactive", version: "9.1.0" },
];

const MOCK_THEMES = [
  { name: "developer-starter", title: "Developer Starter", active: true, version: "2.1.0" },
  { name: "developer-starter-child", title: "Developer Starter Child", active: false, version: "1.0.0" },
];

const MOCK_THEME_FILES = {
  "header.php": `<!DOCTYPE html>\n<html <?php language_attributes(); ?>>\n<head>\n  <meta charset="<?php bloginfo('charset'); ?>">\n  <?php wp_head(); ?>\n</head>\n<body <?php body_class(); ?>>\n  <header class="site-header">\n    <h1><?php bloginfo('name'); ?></h1>\n    <nav><?php wp_nav_menu(['theme_location' => 'primary']); ?></nav>\n  </header>`,
  "footer.php": `  <footer class="site-footer">\n    <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?></p>\n  </footer>\n  <?php wp_footer(); ?>\n</body>\n</html>`,
  "style.css": `/*\nTheme Name: Developer Starter\nVersion: 2.1.0\n*/\nbody { font-family: system-ui, sans-serif; margin: 0; }\n.site-header { background: #1e3a5f; color: #fff; padding: 1rem 2rem; }`,
};

// ---------- MCP tool definitions ----------

const MCP_TOOLS = [
  { name: "wp_list_posts", description: "List WordPress posts with optional filters", inputSchema: { type: "object", properties: { status: { type: "string", enum: ["publish", "draft", "pending", "trash", "any"], default: "any" }, per_page: { type: "number", default: 10 }, category: { type: "string" } } } },
  { name: "wp_create_post", description: "Create a new WordPress post", inputSchema: { type: "object", properties: { title: { type: "string" }, content: { type: "string" }, status: { type: "string", enum: ["publish", "draft"], default: "draft" }, categories: { type: "array", items: { type: "string" } } }, required: ["title", "content"] } },
  { name: "wp_update_post", description: "Update an existing WordPress post by ID", inputSchema: { type: "object", properties: { id: { type: "number" }, title: { type: "string" }, content: { type: "string" }, status: { type: "string" } }, required: ["id"] } },
  { name: "wp_delete_post", description: "Delete a WordPress post by ID", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "wp_list_pages", description: "List WordPress pages", inputSchema: { type: "object", properties: {} } },
  { name: "wp_get_theme_file", description: "Read a theme file from the active theme", inputSchema: { type: "object", properties: { file: { type: "string" } }, required: ["file"] } },
  { name: "wp_update_theme_file", description: "Write changes to a theme file in the active theme", inputSchema: { type: "object", properties: { file: { type: "string" }, content: { type: "string" } }, required: ["file", "content"] } },
  { name: "wp_list_plugins", description: "List installed WordPress plugins and their status", inputSchema: { type: "object", properties: {} } },
  { name: "wp_list_themes", description: "List installed WordPress themes", inputSchema: { type: "object", properties: {} } },
  { name: "wp_cli", description: "Execute a WP-CLI command on the server", inputSchema: { type: "object", properties: { command: { type: "string" } }, required: ["command"] } },
  { name: "wp_rest_api", description: "Call any WordPress REST API endpoint", inputSchema: { type: "object", properties: { method: { type: "string", enum: ["GET", "POST", "PUT", "DELETE"], default: "GET" }, endpoint: { type: "string" }, body: { type: "object" } }, required: ["endpoint"] } },
  { name: "wp_site_info", description: "Get general WordPress site information", inputSchema: { type: "object", properties: {} } },
];

// ---------- tool handlers ----------

function handleToolCall(name, args) {
  switch (name) {
    case "wp_list_posts": {
      let posts = MOCK_POSTS;
      if (args.status && args.status !== "any") posts = posts.filter((p) => p.status === args.status);
      if (args.category) posts = posts.filter((p) => p.categories.includes(args.category));
      return { posts, total: posts.length };
    }
    case "wp_create_post": {
      const newPost = { id: 100 + Math.floor(Math.random() * 900), title: args.title, status: args.status || "draft", date: new Date().toISOString(), author: "admin", categories: args.categories || ["Uncategorized"], excerpt: (args.content || "").slice(0, 120) };
      return { success: true, post: newPost, message: `Post "${args.title}" created as ${newPost.status} (ID: ${newPost.id})` };
    }
    case "wp_update_post": {
      const existing = MOCK_POSTS.find((p) => p.id === args.id);
      if (!existing) return { success: false, error: `Post ${args.id} not found` };
      const updated = { ...existing, ...args };
      return { success: true, post: updated, message: `Post ${args.id} updated` };
    }
    case "wp_delete_post": {
      const found = MOCK_POSTS.find((p) => p.id === args.id);
      return found ? { success: true, message: `Post ${args.id} moved to trash` } : { success: false, error: `Post ${args.id} not found` };
    }
    case "wp_list_pages":
      return { pages: MOCK_PAGES, total: MOCK_PAGES.length };
    case "wp_get_theme_file": {
      const content = MOCK_THEME_FILES[args.file];
      return content ? { file: args.file, theme: "developer-starter", content } : { error: `File ${args.file} not found in active theme` };
    }
    case "wp_update_theme_file":
      return { success: true, file: args.file, theme: "developer-starter", message: `Theme file ${args.file} updated (${args.content.length} bytes)` };
    case "wp_list_plugins":
      return { plugins: MOCK_PLUGINS, total: MOCK_PLUGINS.length };
    case "wp_list_themes":
      return { themes: MOCK_THEMES, total: MOCK_THEMES.length };
    case "wp_cli": {
      const cmd = args.command || "";
      if (cmd.startsWith("plugin list")) return { output: MOCK_PLUGINS.map((p) => `${p.name}\t${p.status}\t${p.version}`).join("\n") };
      if (cmd.startsWith("option get siteurl")) return { output: "https://demo.wpvibe.dev" };
      if (cmd.startsWith("user list")) return { output: "ID\tuser_login\trole\n1\tadmin\tadministrator\n2\teditor\teditor" };
      if (cmd.startsWith("cache flush")) return { output: "Success: The cache was flushed." };
      return { output: `[mock] Executed: wp ${cmd}` };
    }
    case "wp_rest_api": {
      if (args.endpoint === "/" || args.endpoint === "/wp-json") return { name: "Demo WordPress Site", url: "https://demo.wpvibe.dev", namespaces: ["wp/v2", "wpvibe-ai/v1", "wc/v3"] };
      if (args.endpoint.startsWith("/wp/v2/posts")) return MOCK_POSTS;
      return { message: `[mock] ${args.method || "GET"} ${args.endpoint}` };
    }
    case "wp_site_info":
      return { name: "Demo WordPress Site", url: "https://demo.wpvibe.dev", version: "6.7.1", php_version: "8.3.6", active_theme: "Developer Starter", timezone: "America/New_York", multisite: false, permalink_structure: "/%postname%/", wpvibe_version: "1.2.0" };
    default:
      return { error: `Unknown tool: ${name}` };
  }
}

// ---------- HTTP server ----------

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

function sendJson(res, statusCode, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(statusCode, { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) });
  res.end(body);
}

function checkAuth(req) {
  const authHeader = req.headers.authorization || "";
  return authHeader === `Bearer ${API_KEY}`;
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  // Health check
  if (path === "/health" && req.method === "GET") {
    return sendJson(res, 200, { status: "ok", server: "wpvibe-ai-mock", tools: MCP_TOOLS.length });
  }

  // MCP endpoint
  if (path === "/wp-json/wpvibe-ai/v1/mcp") {
    if (!checkAuth(req)) {
      return sendJson(res, 401, { error: "Unauthorized — invalid or missing API key" });
    }

    // SSE (GET)
    if (req.method === "GET") {
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      });
      const sessionId = crypto.randomUUID();
      res.write(`data: ${JSON.stringify({ jsonrpc: "2.0", method: "session/started", params: { sessionId } })}\n\n`);
      const keepAlive = setInterval(() => res.write(": keepalive\n\n"), 15000);
      req.on("close", () => clearInterval(keepAlive));
      return;
    }

    // JSON-RPC (POST)
    if (req.method === "POST") {
      let body;
      try {
        const raw = await readBody(req);
        body = JSON.parse(raw);
      } catch {
        return sendJson(res, 400, { error: "Invalid JSON" });
      }

      const { jsonrpc, id, method, params } = body;
      if (jsonrpc !== "2.0") return sendJson(res, 400, { error: "Invalid JSON-RPC version" });

      let result;
      switch (method) {
        case "initialize":
          result = {
            protocolVersion: "2024-11-05",
            serverInfo: { name: "wpvibe-ai", version: "1.2.0" },
            capabilities: { tools: { listChanged: false } },
          };
          break;
        case "tools/list":
          result = { tools: MCP_TOOLS };
          break;
        case "tools/call": {
          const toolResult = handleToolCall(params.name, params.arguments || {});
          result = { content: [{ type: "text", text: JSON.stringify(toolResult, null, 2) }] };
          break;
        }
        case "ping":
          result = {};
          break;
        default:
          return sendJson(res, 200, { jsonrpc: "2.0", id, error: { code: -32601, message: `Method not found: ${method}` } });
      }

      return sendJson(res, 200, { jsonrpc: "2.0", id, result });
    }
  }

  sendJson(res, 404, { error: "Not found" });
});

server.listen(PORT, () => {
  console.log(`\n  WPVibe AI Mock MCP Server`);
  console.log(`  ========================`);
  console.log(`  SSE endpoint : http://localhost:${PORT}/wp-json/wpvibe-ai/v1/mcp`);
  console.log(`  API key      : ${API_KEY}`);
  console.log(`  Tools        : ${MCP_TOOLS.length} WordPress tools registered`);
  console.log(`  Health check : http://localhost:${PORT}/health\n`);
});
