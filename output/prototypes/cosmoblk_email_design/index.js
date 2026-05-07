#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { buildEmail } = require("./builder");
const { ARCHETYPES } = require("./archetypes");

// --- Demo brand brief ---
const brand = {
  name: "Vortex Labs",
  logo_url: "https://placehold.co/150x50/2563eb/white?text=Vortex+Labs",
  primary_color: "#2563eb",
  secondary_color: "#1e40af",
  accent_color: "#f59e0b",
  font_family: "Inter, Helvetica, Arial, sans-serif",
  address: "Vortex Labs Inc · 42 Innovation Blvd, San Francisco, CA 94107",
};

const archetype = process.argv[2] || "welcome";
const esp = process.argv[3] || "generic";

if (!ARCHETYPES[archetype]) {
  console.error(`Unknown archetype: "${archetype}"`);
  console.error(`Available: ${Object.keys(ARCHETYPES).join(", ")}`);
  process.exit(1);
}

console.log(`\n=== CosmoBlk Email Design Demo ===`);
console.log(`Archetype : ${ARCHETYPES[archetype].name}`);
console.log(`Brand     : ${brand.name}`);
console.log(`ESP       : ${esp}`);
console.log(`================================\n`);

const { mjml, html, errors } = buildEmail({ archetype, brand, esp });

if (errors.length > 0) {
  console.warn("MJML warnings:", errors);
}

// Write outputs
const outDir = path.join(__dirname, "output");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

const mjmlPath = path.join(outDir, `${archetype}.mjml`);
const htmlPath = path.join(outDir, `${archetype}.html`);

fs.writeFileSync(mjmlPath, mjml);
fs.writeFileSync(htmlPath, html);

console.log(`MJML saved to: output/${archetype}.mjml`);
console.log(`HTML saved to: output/${archetype}.html`);
console.log(`\nHTML size: ${(Buffer.byteLength(html) / 1024).toFixed(1)} KB`);
console.log(`\n--- MJML source (first 40 lines) ---\n`);
console.log(mjml.split("\n").slice(0, 40).join("\n"));
console.log("\n... (truncated)\n");
