/**
 * Mock Capsule CRM API server.
 * Uses only Node.js built-in modules (no npm dependencies).
 * Simulates the Capsule CRM v2 REST API for demo purposes.
 */
const http = require("http");
const url = require("url");

// ---------- seed data ----------
const parties = [
  { id: 1001, type: "person", firstName: "Alice", lastName: "Chen", title: "VP of Engineering",
    organisation: { name: "Acme Corp" }, email: "alice@acme.io", tags: [{ name: "enterprise" }] },
  { id: 1002, type: "person", firstName: "Bob", lastName: "Martinez", title: "Head of Product",
    organisation: { name: "Globex Inc" }, email: "bob@globex.com", tags: [{ name: "mid-market" }] },
  { id: 1003, type: "organisation", name: "Initech LLC",
    email: "info@initech.co", tags: [{ name: "smb" }] },
];

const opportunities = [
  { id: 2001, name: "Acme Enterprise Deal", milestone: { name: "Proposal" },
    value: { amount: 120000, currency: "USD" }, party: { id: 1001, name: "Alice Chen" },
    expectedCloseDate: "2026-06-15", probability: 60 },
  { id: 2002, name: "Globex Expansion", milestone: { name: "Negotiation" },
    value: { amount: 45000, currency: "USD" }, party: { id: 1002, name: "Bob Martinez" },
    expectedCloseDate: "2026-07-01", probability: 40 },
];

const kases = [
  { id: 3001, name: "Acme Onboarding", status: "OPEN",
    party: { id: 1001, name: "Alice Chen" }, description: "Enterprise onboarding in progress" },
  { id: 3002, name: "Initech Support Ticket", status: "OPEN",
    party: { id: 1003, name: "Initech LLC" }, description: "Integration questions" },
];

const tasks = [
  { id: 4001, description: "Follow up on Acme proposal", dueOn: "2026-05-20",
    status: "OPEN", party: { id: 1001 } },
  { id: 4002, description: "Send Globex contract", dueOn: "2026-05-18",
    status: "OPEN", party: { id: 1002 } },
];

// ---------- helpers ----------
function readBody(req) {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", (c) => (data += c));
    req.on("end", () => {
      try { resolve(JSON.parse(data)); }
      catch { resolve({}); }
    });
  });
}

function send(res, statusCode, body) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

// ---------- router ----------
const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);
  const path = parsed.pathname;
  const method = req.method;

  // auth check
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith("Bearer ")) {
    return send(res, 401, { error: "Unauthorized" });
  }

  // GET /api/v2/parties
  if (method === "GET" && path === "/api/v2/parties") {
    const q = (parsed.query.q || "").toLowerCase();
    const filtered = q
      ? parties.filter(p =>
          (p.firstName || "").toLowerCase().includes(q) ||
          (p.lastName || "").toLowerCase().includes(q) ||
          (p.name || "").toLowerCase().includes(q))
      : parties;
    return send(res, 200, { parties: filtered });
  }

  // GET /api/v2/parties/:id
  const partyMatch = path.match(/^\/api\/v2\/parties\/(\d+)$/);
  if (method === "GET" && partyMatch) {
    const p = parties.find(p => p.id === parseInt(partyMatch[1]));
    return p ? send(res, 200, { party: p }) : send(res, 404, { error: "Not found" });
  }

  // POST /api/v2/parties
  if (method === "POST" && path === "/api/v2/parties") {
    const body = await readBody(req);
    const partyData = body.party || {};
    const newParty = { id: 1000 + parties.length + 1, ...partyData };
    parties.push(newParty);
    return send(res, 201, { party: newParty });
  }

  // GET /api/v2/opportunities
  if (method === "GET" && path === "/api/v2/opportunities") {
    return send(res, 200, { opportunities });
  }

  // GET /api/v2/kases
  if (method === "GET" && path === "/api/v2/kases") {
    return send(res, 200, { kases });
  }

  // GET /api/v2/tasks
  if (method === "GET" && path === "/api/v2/tasks") {
    return send(res, 200, { tasks });
  }

  // POST /api/v2/tasks
  if (method === "POST" && path === "/api/v2/tasks") {
    const body = await readBody(req);
    const taskData = body.task || {};
    const newTask = { id: 4000 + tasks.length + 1, status: "OPEN", ...taskData };
    tasks.push(newTask);
    return send(res, 201, { task: newTask });
  }

  send(res, 404, { error: "Not found" });
});

const PORT = process.env.MOCK_PORT || 4100;
server.listen(PORT, () => {
  console.log(`[Mock Capsule CRM API] listening on http://localhost:${PORT}`);
});

module.exports = server;
