#!/usr/bin/env node
/**
 * Standalone demo — exercises Qobrix CRM MCP tools using mock data directly.
 * No API keys or live CRM instance required.
 */

import { contacts, properties, leads, opportunities, tasks, users } from "./mock-data.js";

const DIVIDER = "─".repeat(60);

function heading(title) {
  console.log(`\n${DIVIDER}`);
  console.log(`  ${title}`);
  console.log(DIVIDER);
}

function table(rows, columns) {
  // Simple ASCII table
  const widths = columns.map(col =>
    Math.max(col.label.length, ...rows.map(r => String(col.get(r)).length))
  );
  const header = columns.map((c, i) => c.label.padEnd(widths[i])).join(" | ");
  const sep = widths.map(w => "─".repeat(w)).join("─┼─");
  console.log(`  ${header}`);
  console.log(`  ${sep}`);
  rows.forEach(r => {
    const line = columns.map((c, i) => String(c.get(r)).padEnd(widths[i])).join(" | ");
    console.log(`  ${line}`);
  });
}

// ── Scenario 1: Property search ──────────────────────────────
heading("1. PROPERTY SEARCH — Dubai Marina, under $2M");

const marineProps = properties.filter(
  p => p.SubdivisionName.toLowerCase().includes("marina") && p.ListPrice <= 2000000
);

table(marineProps, [
  { label: "ListingId", get: r => r.ListingId },
  { label: "Type", get: r => r.PropertyType },
  { label: "Beds", get: r => r.BedroomsTotal },
  { label: "Price (USD)", get: r => `$${r.ListPrice.toLocaleString()}` },
  { label: "Status", get: r => r.StandardStatus },
  { label: "Location", get: r => r.SubdivisionName },
]);

console.log(`\n  → Found ${marineProps.length} matching property(ies)`);

// ── Scenario 2: Lead pipeline ────────────────────────────────
heading("2. LEAD PIPELINE — All leads assigned to John");

const johnLeads = leads.filter(l => l.AssignedAgent.includes("John"));

table(johnLeads, [
  { label: "LeadId", get: r => r.LeadId },
  { label: "Contact", get: r => r.ContactName },
  { label: "Status", get: r => r.Status },
  { label: "Source", get: r => r.Source },
  { label: "Created", get: r => r.CreatedAt.slice(0, 10) },
]);

console.log(`\n  → ${johnLeads.length} lead(s) assigned to John Mitchell`);

// ── Scenario 3: Active opportunities ─────────────────────────
heading("3. DEAL PIPELINE — Opportunities in Negotiation stage");

const negotiating = opportunities.filter(o => o.Stage === "Negotiation");

table(negotiating, [
  { label: "OppId", get: r => r.OpportunityId },
  { label: "Contact", get: r => r.ContactName },
  { label: "Value", get: r => `$${r.Value.toLocaleString()}` },
  { label: "Probability", get: r => `${r.Probability}%` },
  { label: "Expected Close", get: r => r.ExpectedCloseDate },
]);

console.log(`\n  → Total pipeline value: $${negotiating.reduce((s, o) => s + o.Value, 0).toLocaleString()}`);

// ── Scenario 4: Upcoming tasks ───────────────────────────────
heading("4. CRM TASKS — High-priority pending tasks");

const highPrio = tasks.filter(t => t.Priority === "High");

table(highPrio, [
  { label: "TaskId", get: r => r.TaskId },
  { label: "Title", get: r => r.Title },
  { label: "Assigned To", get: r => r.AssignedTo },
  { label: "Due", get: r => r.DueDate },
  { label: "Status", get: r => r.Status },
]);

// ── Scenario 5: Contact lookup ───────────────────────────────
heading("5. CONTACT DETAILS — Get record cnt-001");

const contact = contacts.find(c => c.ContactId === "cnt-001");
console.log(`  Name:     ${contact.FirstName} ${contact.LastName}`);
console.log(`  Email:    ${contact.Email}`);
console.log(`  Phone:    ${contact.Phone}`);
console.log(`  Type:     ${contact.ContactType}`);
console.log(`  Location: ${contact.PreferredLocation}`);
console.log(`  Budget:   $${contact.Budget.toLocaleString()}`);

// ── Scenario 6: Active listings with 3+ bedrooms ────────────
heading("6. LISTINGS — Active properties with 3+ bedrooms");

const bigActive = properties.filter(p => p.StandardStatus === "Active" && p.BedroomsTotal >= 3);

table(bigActive, [
  { label: "ListingId", get: r => r.ListingId },
  { label: "Type", get: r => r.PropertyType },
  { label: "Beds", get: r => r.BedroomsTotal },
  { label: "Baths", get: r => r.BathroomsTotalInteger },
  { label: "Area (sqft)", get: r => r.LivingArea.toLocaleString() },
  { label: "Price", get: r => `$${r.ListPrice.toLocaleString()}` },
  { label: "Agent", get: r => r.ListAgentFullName },
]);

// ── Scenario 7: Agent summary ────────────────────────────────
heading("7. AGENT ROSTER — All agents");

table(users, [
  { label: "Name", get: r => r.FullName },
  { label: "Role", get: r => r.Role },
  { label: "Team", get: r => r.Team },
  { label: "Active Listings", get: r => r.ActiveListings },
  { label: "Closed Deals", get: r => r.ClosedDeals },
]);

// ── RESO DD 2.0 field mapping demo ──────────────────────────
heading("8. RESO DD 2.0 FIELD MAPPING");

const resoFields = [
  { qobrix: "listing_price", reso: "ListPrice", sample: "$1,500,000" },
  { qobrix: "property_category", reso: "PropertyType", sample: "Apartment" },
  { qobrix: "listing_status", reso: "StandardStatus", sample: "Active" },
  { qobrix: "listing_id", reso: "ListingId", sample: "prop-101" },
  { qobrix: "bedrooms", reso: "BedroomsTotal", sample: "2" },
  { qobrix: "bathrooms", reso: "BathroomsTotalInteger", sample: "2" },
  { qobrix: "area_sqft", reso: "LivingArea", sample: "1200" },
  { qobrix: "subdivision", reso: "SubdivisionName", sample: "Dubai Marina" },
];

table(resoFields, [
  { label: "Qobrix Field", get: r => r.qobrix },
  { label: "RESO DD 2.0", get: r => r.reso },
  { label: "Sample Value", get: r => r.sample },
]);

// ── Summary ──────────────────────────────────────────────────
heading("SUMMARY");
console.log(`  Contacts:      ${contacts.length}`);
console.log(`  Properties:    ${properties.length}`);
console.log(`  Leads:         ${leads.length}`);
console.log(`  Opportunities: ${opportunities.length}`);
console.log(`  Tasks:         ${tasks.length}`);
console.log(`  Users/Agents:  ${users.length}`);
console.log(`\n  All data uses RESO DD 2.0 canonical field names.`);
console.log(`  The real server exposes 42 tools across 13 entity groups.`);
console.log(`  This demo covered 7 representative query patterns.\n`);
