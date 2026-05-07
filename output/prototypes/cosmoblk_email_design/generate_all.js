#!/usr/bin/env node
// Generate all six archetypes at once for quick comparison.

const fs = require("fs");
const path = require("path");
const { buildEmail } = require("./builder");
const { ARCHETYPES } = require("./archetypes");

const brand = {
  name: "Vortex Labs",
  logo_url: "https://placehold.co/150x50/2563eb/white?text=Vortex+Labs",
  primary_color: "#2563eb",
  secondary_color: "#1e40af",
  font_family: "Inter, Helvetica, Arial, sans-serif",
  address: "Vortex Labs Inc · 42 Innovation Blvd, San Francisco, CA 94107",
};

const outDir = path.join(__dirname, "output");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

console.log("\n=== Generating all 6 email archetypes ===\n");

for (const [key, arch] of Object.entries(ARCHETYPES)) {
  const { mjml, html, errors } = buildEmail({ archetype: key, brand, esp: "generic" });

  fs.writeFileSync(path.join(outDir, `${key}.mjml`), mjml);
  fs.writeFileSync(path.join(outDir, `${key}.html`), html);

  const sizeKb = (Buffer.byteLength(html) / 1024).toFixed(1);
  const warn = errors.length > 0 ? ` (${errors.length} warnings)` : "";
  console.log(`  [OK] ${arch.name.padEnd(15)} → output/${key}.html  (${sizeKb} KB)${warn}`);
}

console.log(`\nDone. Open any .html file in a browser to preview.\n`);
