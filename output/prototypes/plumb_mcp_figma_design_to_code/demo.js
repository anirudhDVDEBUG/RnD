#!/usr/bin/env node
/**
 * demo.js — Simulates an AI agent calling plumb-mcp tools to:
 *   1. Fetch file structure from Figma
 *   2. Extract design tokens
 *   3. Get component details for HeroSection
 *   4. Generate React/HTML code from the design
 *   5. Run the verification loop against the generated code
 *
 * No Figma account, API key, or network access required.
 */

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const FIGMA_DATA = JSON.parse(
  readFileSync(join(__dirname, "mock-figma-data.json"), "utf-8")
);

// ── Inline the tool handlers (same as mock-mcp-server.js) ───────────
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
    })),
  }),

  get_component_details: ({ componentName }) => {
    return FIGMA_DATA.components.find(
      (c) => c.name.toLowerCase() === componentName.toLowerCase()
    );
  },

  extract_design_tokens: () => FIGMA_DATA.designTokens,

  verify_implementation: ({ html }) => {
    const tokens = FIGMA_DATA.designTokens;
    const checks = [];
    let pass = 0, total = 0;
    for (const [name, value] of Object.entries(tokens.colors)) {
      total++;
      const found = html.includes(value);
      checks.push({ check: `color/${name}`, value, found });
      if (found) pass++;
    }
    for (const [name, spec] of Object.entries(tokens.typography)) {
      total++;
      const found = html.includes(`${spec.fontSize}px`);
      checks.push({ check: `typography/${name}`, fontSize: `${spec.fontSize}px`, found });
      if (found) pass++;
    }
    return {
      score: Math.round((pass / total) * 100),
      passed: pass,
      total,
      checks,
      verdict: pass === total
        ? "PASS — all design tokens present"
        : `PARTIAL — ${total - pass} token(s) missing`,
    };
  },
};

// ── Helpers ──────────────────────────────────────────────────────────
const sep = (title) =>
  console.log(`\n${"=".repeat(64)}\n  ${title}\n${"=".repeat(64)}`);

function rgbaToHex(r, g, b) {
  const hex = (v) =>
    Math.round(v * 255)
      .toString(16)
      .padStart(2, "0")
      .toUpperCase();
  return `#${hex(r)}${hex(g)}${hex(b)}`;
}

// ── Step 1: Fetch file structure ─────────────────────────────────────
sep("STEP 1 — get_file_structure");
const structure = tools.get_file_structure();
console.log(`File: ${structure.fileName} (${structure.fileKey})`);
console.log(`Components found: ${structure.componentCount}`);
structure.components.forEach((c) =>
  console.log(`  - ${c.name}  [${c.type}]  ${c.size}`)
);

// ── Step 2: Extract design tokens ────────────────────────────────────
sep("STEP 2 — extract_design_tokens");
const tokens = tools.extract_design_tokens();
console.log("Colors:");
for (const [k, v] of Object.entries(tokens.colors))
  console.log(`  --${k}: ${v}`);
console.log("\nTypography:");
for (const [k, v] of Object.entries(tokens.typography))
  console.log(`  ${k}: ${v.fontFamily} ${v.fontWeight} ${v.fontSize}px/${v.lineHeight}px`);
console.log("\nSpacing:");
for (const [k, v] of Object.entries(tokens.spacing))
  console.log(`  --spacing-${k}: ${v}px`);

// ── Step 3: Get HeroSection details ──────────────────────────────────
sep("STEP 3 — get_component_details('HeroSection')");
const hero = tools.get_component_details({ componentName: "HeroSection" });
console.log(`Component: ${hero.name}  ${hero.width}x${hero.height}`);
console.log(`Layout: ${hero.layoutMode}, gap ${hero.itemSpacing}px`);
console.log(`Children:`);
hero.children.forEach((child) => {
  if (child.type === "TEXT") {
    console.log(`  [TEXT] "${child.characters}"  ${child.style.fontSize}px ${child.style.fontWeight}`);
  } else if (child.type === "FRAME") {
    console.log(`  [FRAME] ${child.name}  ${child.width}x${child.height}  radius=${child.cornerRadius}px`);
    if (child.children) {
      child.children.forEach((gc) =>
        console.log(`    [${gc.type}] "${gc.characters || gc.name}"`)
      );
    }
  }
});

// ── Step 4: Generate code from design data ───────────────────────────
sep("STEP 4 — Generate React + CSS from design");

const generatedCSS = `:root {
  /* Colors from design tokens */
  --bg-primary: ${tokens.colors["background-primary"]};
  --bg-card: ${tokens.colors["background-card"]};
  --border-card: ${tokens.colors["border-card"]};
  --text-primary: ${tokens.colors["text-primary"]};
  --text-secondary: ${tokens.colors["text-secondary"]};
  --text-muted: ${tokens.colors["text-muted"]};
  --accent: ${tokens.colors["accent-primary"]};
  --accent-muted: ${tokens.colors["accent-primary-muted"]};
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${hero.paddingTop}px ${hero.paddingTop}px;
  gap: ${hero.itemSpacing}px;
  background: var(--bg-primary);
  min-height: ${hero.height}px;
}

.hero__headline {
  font-family: '${tokens.typography["heading-xl"].fontFamily}', sans-serif;
  font-weight: ${tokens.typography["heading-xl"].fontWeight};
  font-size: ${tokens.typography["heading-xl"].fontSize}px;
  line-height: ${tokens.typography["heading-xl"].lineHeight}px;
  letter-spacing: ${tokens.typography["heading-xl"].letterSpacing}px;
  color: var(--text-primary);
  text-align: center;
}

.hero__sub {
  font-family: '${tokens.typography["body-lg"].fontFamily}', sans-serif;
  font-weight: ${tokens.typography["body-lg"].fontWeight};
  font-size: ${tokens.typography["body-lg"].fontSize}px;
  line-height: ${tokens.typography["body-lg"].lineHeight}px;
  color: var(--text-secondary);
  text-align: center;
}

.hero__cta {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  background: var(--accent);
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-family: '${tokens.typography["button"].fontFamily}', sans-serif;
  font-weight: ${tokens.typography["button"].fontWeight};
  font-size: ${tokens.typography["button"].fontSize}px;
  line-height: ${tokens.typography["button"].lineHeight}px;
  color: var(--text-primary);
}`;

const generatedJSX = `export function HeroSection() {
  return (
    <section className="hero">
      <h1 className="hero__headline">
        ${hero.children[0].characters}
      </h1>
      <p className="hero__sub">
        ${hero.children[1].characters}
      </p>
      <button className="hero__cta">
        ${hero.children[2].children[0].characters}
      </button>
    </section>
  );
}`;

console.log("--- Generated CSS (hero.css) ---");
console.log(generatedCSS);
console.log("\n--- Generated JSX (HeroSection.jsx) ---");
console.log(generatedJSX);

// ── Step 5: Verification loop ────────────────────────────────────────
sep("STEP 5 — verify_implementation (verification loop)");

// Build a flat HTML-like string containing all token values for checking
const implString = generatedCSS + " " + generatedJSX;
const result = tools.verify_implementation({ html: implString });

console.log(`Score: ${result.score}%  (${result.passed}/${result.total} checks passed)`);
console.log(`Verdict: ${result.verdict}\n`);
console.log("Detail:");
result.checks.forEach((c) => {
  const icon = c.found ? "[PASS]" : "[MISS]";
  const val = c.value || c.fontSize;
  console.log(`  ${icon} ${c.check}  (${val})`);
});

// ── Summary ──────────────────────────────────────────────────────────
sep("DONE");
console.log(`
plumb-mcp demo complete.

What happened:
  1. Retrieved Figma file structure (2 components)
  2. Extracted 8 color tokens, 5 typography scales, 6 spacing values
  3. Read HeroSection layout details (auto-layout, children, text styles)
  4. Generated React component + CSS custom properties from design data
  5. Ran verification loop — ${result.score}% token coverage

In production, plumb-mcp does this against your REAL Figma file via a
local plugin (no REST API, no rate limits, works on Figma Free).
`);
