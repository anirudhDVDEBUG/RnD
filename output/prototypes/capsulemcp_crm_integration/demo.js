#!/usr/bin/env node
/**
 * demo.js — Exercises the mock Capsule CRM API the same way
 * capsulemcp would, showing every major CRM operation Claude can
 * perform through the MCP server.
 *
 * Runs against the local mock server so no real API key is needed.
 */

const http = require("http");

const BASE = `http://localhost:${process.env.MOCK_PORT || 4100}`;
const TOKEN = "demo-token-for-testing";

// ── helpers ──────────────────────────────────────────────────────
function api(method, path, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE);
    const opts = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: {
        Authorization: `Bearer ${TOKEN}`,
        "Content-Type": "application/json",
      },
    };
    const req = http.request(opts, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(data); }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function heading(text) {
  const line = "═".repeat(text.length + 4);
  console.log(`\n${line}`);
  console.log(`║ ${text} ║`);
  console.log(`${line}`);
}

function table(rows, cols) {
  // simple column printer
  const widths = cols.map((c) =>
    Math.max(c.label.length, ...rows.map((r) => String(c.fn(r)).length))
  );
  const header = cols.map((c, i) => c.label.padEnd(widths[i])).join(" │ ");
  const sep = widths.map((w) => "─".repeat(w)).join("─┼─");
  console.log(`  ${header}`);
  console.log(`  ${sep}`);
  rows.forEach((r) => {
    const line = cols.map((c, i) => String(c.fn(r)).padEnd(widths[i])).join(" │ ");
    console.log(`  ${line}`);
  });
}

// ── main ─────────────────────────────────────────────────────────
async function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║   capsulemcp — Capsule CRM ↔ Claude MCP Demo       ║");
  console.log("║   (running against local mock API)                  ║");
  console.log("╚══════════════════════════════════════════════════════╝");

  // 1. List contacts
  heading("1. List all CRM contacts (parties)");
  const { parties } = await api("GET", "/api/v2/parties");
  table(parties, [
    { label: "ID",   fn: (p) => p.id },
    { label: "Type", fn: (p) => p.type },
    { label: "Name", fn: (p) => p.type === "person" ? `${p.firstName} ${p.lastName}` : p.name },
    { label: "Org",  fn: (p) => p.organisation?.name || "—" },
    { label: "Tags", fn: (p) => (p.tags || []).map(t => t.name).join(", ") },
  ]);

  // 2. Search contacts
  heading("2. Search contacts (query: 'alice')");
  const search = await api("GET", "/api/v2/parties?q=alice");
  search.parties.forEach((p) => {
    console.log(`  → Found: ${p.firstName} ${p.lastName} (${p.title}) at ${p.organisation?.name}`);
    console.log(`    Email: ${p.email}`);
  });

  // 3. Opportunities / pipeline
  heading("3. Sales pipeline (opportunities)");
  const { opportunities } = await api("GET", "/api/v2/opportunities");
  table(opportunities, [
    { label: "Deal",       fn: (o) => o.name },
    { label: "Stage",      fn: (o) => o.milestone.name },
    { label: "Value",      fn: (o) => `$${(o.value.amount).toLocaleString()}` },
    { label: "Close Date", fn: (o) => o.expectedCloseDate },
    { label: "Prob",       fn: (o) => `${o.probability}%` },
  ]);

  const totalPipeline = opportunities.reduce((s, o) => s + o.value.amount, 0);
  const weightedPipeline = opportunities.reduce((s, o) => s + o.value.amount * o.probability / 100, 0);
  console.log(`\n  Total pipeline:    $${totalPipeline.toLocaleString()}`);
  console.log(`  Weighted pipeline: $${weightedPipeline.toLocaleString()}`);

  // 4. Cases
  heading("4. Open cases");
  const { kases } = await api("GET", "/api/v2/kases");
  table(kases, [
    { label: "Case",    fn: (k) => k.name },
    { label: "Status",  fn: (k) => k.status },
    { label: "Contact", fn: (k) => k.party.name },
    { label: "Desc",    fn: (k) => k.description },
  ]);

  // 5. Tasks
  heading("5. Upcoming tasks");
  const { tasks } = await api("GET", "/api/v2/tasks");
  table(tasks, [
    { label: "Task",   fn: (t) => t.description },
    { label: "Due",    fn: (t) => t.dueOn },
    { label: "Status", fn: (t) => t.status },
  ]);

  // 6. Create a new contact
  heading("6. Create new contact (write operation)");
  const newContact = await api("POST", "/api/v2/parties", {
    party: { type: "person", firstName: "Dana", lastName: "Reeves",
             title: "CTO", organisation: { name: "NewCo" } }
  });
  console.log(`  ✓ Created: ${newContact.party.firstName} ${newContact.party.lastName}`);
  console.log(`    ID: ${newContact.party.id}, Title: ${newContact.party.title}`);

  // 7. Create a task
  heading("7. Create follow-up task");
  const newTask = await api("POST", "/api/v2/tasks", {
    task: { description: "Schedule intro call with Dana Reeves",
            dueOn: "2026-05-25", party: { id: newContact.party.id } }
  });
  console.log(`  ✓ Task created: "${newTask.task.description}"`);
  console.log(`    Due: ${newTask.task.dueOn}  Status: ${newTask.task.status}`);

  // 8. Summary
  heading("Summary");
  console.log(`  Contacts:      ${parties.length + 1} (1 new)`);
  console.log(`  Opportunities: ${opportunities.length}`);
  console.log(`  Open cases:    ${kases.length}`);
  console.log(`  Tasks:         ${tasks.length + 1} (1 new)`);
  console.log(`\n  All operations succeeded against the mock Capsule CRM API.`);
  console.log(`  In production, capsulemcp exposes these as MCP tools that`);
  console.log(`  Claude calls directly during conversation.\n`);
}

main().catch((err) => {
  console.error("Demo failed:", err.message);
  process.exit(1);
});
