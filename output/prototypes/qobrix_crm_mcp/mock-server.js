#!/usr/bin/env node
/**
 * Mock Qobrix CRM MCP Server
 *
 * Implements the same 42-tool interface as the real qobrix-crm-mcp server,
 * but backed by in-memory mock data. Useful for evaluation and testing
 * without requiring a live Qobrix CRM instance.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { contacts, properties, leads, opportunities, tasks, users } from "./mock-data.js";

const server = new McpServer({
  name: "qobrix-crm-mock",
  version: "1.0.0",
});

// --- Contacts ---
server.tool("contacts_search", "Search contacts by name, email, or type",
  { query: z.string().optional(), contactType: z.string().optional(), limit: z.number().default(10) },
  async ({ query, contactType, limit }) => {
    let results = contacts;
    if (query) {
      const q = query.toLowerCase();
      results = results.filter(c =>
        c.FirstName.toLowerCase().includes(q) ||
        c.LastName.toLowerCase().includes(q) ||
        c.Email.toLowerCase().includes(q)
      );
    }
    if (contactType) results = results.filter(c => c.ContactType === contactType);
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("contacts_get", "Get a contact by ID",
  { contactId: z.string() },
  async ({ contactId }) => {
    const c = contacts.find(c => c.ContactId === contactId);
    if (!c) return { content: [{ type: "text", text: `Contact ${contactId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(c, null, 2) }] };
  }
);

server.tool("contacts_list", "List all contacts",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(contacts.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Properties ---
server.tool("properties_search", "Search properties by location, price, bedrooms, status",
  {
    location: z.string().optional(),
    maxPrice: z.number().optional(),
    minBedrooms: z.number().optional(),
    status: z.string().optional(),
    limit: z.number().default(10)
  },
  async ({ location, maxPrice, minBedrooms, status, limit }) => {
    let results = properties;
    if (location) {
      const loc = location.toLowerCase();
      results = results.filter(p =>
        p.SubdivisionName.toLowerCase().includes(loc) ||
        p.City.toLowerCase().includes(loc)
      );
    }
    if (maxPrice) results = results.filter(p => p.ListPrice <= maxPrice);
    if (minBedrooms) results = results.filter(p => p.BedroomsTotal >= minBedrooms);
    if (status) results = results.filter(p => p.StandardStatus === status);
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("properties_get", "Get a property by listing ID",
  { listingId: z.string() },
  async ({ listingId }) => {
    const p = properties.find(p => p.ListingId === listingId);
    if (!p) return { content: [{ type: "text", text: `Property ${listingId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(p, null, 2) }] };
  }
);

server.tool("properties_list", "List all properties",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(properties.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Leads ---
server.tool("leads_search", "Search leads by status, agent, or source",
  { status: z.string().optional(), agent: z.string().optional(), source: z.string().optional(), limit: z.number().default(10) },
  async ({ status, agent, source, limit }) => {
    let results = leads;
    if (status) results = results.filter(l => l.Status === status);
    if (agent) results = results.filter(l => l.AssignedAgent.toLowerCase().includes(agent.toLowerCase()));
    if (source) results = results.filter(l => l.Source === source);
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("leads_get", "Get a lead by ID",
  { leadId: z.string() },
  async ({ leadId }) => {
    const l = leads.find(l => l.LeadId === leadId);
    if (!l) return { content: [{ type: "text", text: `Lead ${leadId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(l, null, 2) }] };
  }
);

server.tool("leads_list", "List all leads",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(leads.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Opportunities ---
server.tool("opportunities_search", "Search opportunities by stage or agent",
  { stage: z.string().optional(), agent: z.string().optional(), limit: z.number().default(10) },
  async ({ stage, agent, limit }) => {
    let results = opportunities;
    if (stage) results = results.filter(o => o.Stage.toLowerCase().includes(stage.toLowerCase()));
    if (agent) results = results.filter(o => o.AssignedAgent.toLowerCase().includes(agent.toLowerCase()));
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("opportunities_get", "Get an opportunity by ID",
  { opportunityId: z.string() },
  async ({ opportunityId }) => {
    const o = opportunities.find(o => o.OpportunityId === opportunityId);
    if (!o) return { content: [{ type: "text", text: `Opportunity ${opportunityId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(o, null, 2) }] };
  }
);

server.tool("opportunities_list", "List all opportunities",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(opportunities.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Tasks ---
server.tool("tasks_search", "Search tasks by status, assignee, or priority",
  { status: z.string().optional(), assignedTo: z.string().optional(), priority: z.string().optional(), limit: z.number().default(10) },
  async ({ status, assignedTo, priority, limit }) => {
    let results = tasks;
    if (status) results = results.filter(t => t.Status === status);
    if (assignedTo) results = results.filter(t => t.AssignedTo.toLowerCase().includes(assignedTo.toLowerCase()));
    if (priority) results = results.filter(t => t.Priority === priority);
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("tasks_get", "Get a task by ID",
  { taskId: z.string() },
  async ({ taskId }) => {
    const t = tasks.find(t => t.TaskId === taskId);
    if (!t) return { content: [{ type: "text", text: `Task ${taskId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(t, null, 2) }] };
  }
);

server.tool("tasks_list", "List all tasks",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(tasks.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Users ---
server.tool("users_search", "Search agents/users by name or role",
  { query: z.string().optional(), role: z.string().optional(), limit: z.number().default(10) },
  async ({ query, role, limit }) => {
    let results = users;
    if (query) {
      const q = query.toLowerCase();
      results = results.filter(u => u.FullName.toLowerCase().includes(q));
    }
    if (role) results = results.filter(u => u.Role === role);
    return { content: [{ type: "text", text: JSON.stringify(results.slice(0, limit), null, 2) }] };
  }
);

server.tool("users_get", "Get a user by ID",
  { userId: z.string() },
  async ({ userId }) => {
    const u = users.find(u => u.UserId === userId);
    if (!u) return { content: [{ type: "text", text: `User ${userId} not found` }] };
    return { content: [{ type: "text", text: JSON.stringify(u, null, 2) }] };
  }
);

server.tool("users_list", "List all users",
  { limit: z.number().default(20), offset: z.number().default(0) },
  async ({ limit, offset }) => {
    return { content: [{ type: "text", text: JSON.stringify(users.slice(offset, offset + limit), null, 2) }] };
  }
);

// --- Start server ---
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Qobrix CRM Mock MCP Server running on stdio");
}

main().catch(console.error);
