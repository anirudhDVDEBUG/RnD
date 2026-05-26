/**
 * Mock plumb-mcp server — simulates the MCP tool interface that the real
 * plumb-mcp exposes to AI coding agents.  Uses the same JSON-RPC style
 * messages so you can see what the agent↔server conversation looks like.
 *
 * This does NOT require Figma Desktop; it reads mock-figma-data.json instead.
 */

import { readFileSync } from "fs";
import { createServer } from "http";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const FIGMA_DATA = JSON.parse(
  readFileSync(join(__dirname, "mock-figma-data.json"), "utf-8")
);

// ── MCP Tool handlers ────────────────────────────────────────────────
const tools = {
  get_file_structure: () => ({
    fileName: FIGMA_DATA.fileName,
    fileKey: FIGMA_DATA.fileKey,
    lastModified: FIGMA_DATA.lastModified,
    componentCount: FIGMA_DATA.components.length,
    components: FIGMA_DATA.components.map((c) => ({
      id: c.id,
      name: c.name,
      type: c.type,
      size: `${c.width}x${c.height}`,
      childCount: c.children?.length ?? 0,
    })),
  }),

  get_component_details: ({ componentName }) => {
    const comp = FIGMA_DATA.components.find(
      (c) => c.name.toLowerCase() === (componentName || "").toLowerCase()
    );
    if (!comp) return { error: `Component "${componentName}" not found` };
    return comp;
  },

  extract_design_tokens: () => FIGMA_DATA.designTokens,

  verify_implementation: ({ html }) => {
    // Simulated verification — checks for token usage in supplied HTML
    const tokens = FIGMA_DATA.designTokens;
    const checks = [];
    let pass = 0;
    let total = 0;

    // Check colors
    for (const [name, value] of Object.entries(tokens.colors)) {
      total++;
      const found = html && html.includes(value);
      checks.push({ check: `color/${name}`, value, found: !!found });
      if (found) pass++;
    }

    // Check font sizes
    for (const [name, spec] of Object.entries(tokens.typography)) {
      total++;
      const found = html && html.includes(`${spec.fontSize}px`);
      checks.push({
        check: `typography/${name}`,
        fontSize: `${spec.fontSize}px`,
        found: !!found,
      });
      if (found) pass++;
    }

    return {
      score: total > 0 ? Math.round((pass / total * 100)) : 0,
      passed: pass,
      total,
      checks,
      verdict:
        pass === total
          ? "PASS — implementation matches design tokens"
          : `PARTIAL — ${total - pass} token(s) missing from implementation`,
    };
  },
};

// ── HTTP server (for demo / inspection) ──────────────────────────────
const PORT = process.env.PORT || 9333;

const server = createServer((req, res) => {
  if (req.method === "POST") {
    let body = "";
    req.on("data", (d) => (body += d));
    req.on("end", () => {
      try {
        const { method, params } = JSON.parse(body);
        const handler = tools[method];
        if (!handler) {
          res.writeHead(404);
          res.end(JSON.stringify({ error: `Unknown tool: ${method}` }));
          return;
        }
        const result = handler(params || {});
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(result, null, 2));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(
      JSON.stringify({
        name: "plumb-mcp (mock)",
        tools: Object.keys(tools),
        status: "ready",
      })
    );
  }
});

server.listen(PORT, () => {
  console.log(`Mock plumb-mcp server listening on http://localhost:${PORT}`);
  console.log(`Available tools: ${Object.keys(tools).join(", ")}`);
});

export { tools };
