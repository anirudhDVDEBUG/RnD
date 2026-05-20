#!/usr/bin/env node
/**
 * Tokenless Context Compression — Interactive Demo
 *
 * Compresses the included sample_project/ and prints a detailed
 * before/after report showing token savings per file and overall.
 */

const path = require("path");
const { compressProject, compressFile, estimateTokens } = require("./compressor");

// ── Helpers ──────────────────────────────────────────────────────────
function bar(pct, width = 30) {
  const filled = Math.round((pct / 100) * width);
  return "[" + "#".repeat(filled) + "-".repeat(width - filled) + "]";
}

function pad(str, len) {
  str = String(str);
  return str.length >= len ? str : str + " ".repeat(len - str.length);
}

function rpad(str, len) {
  str = String(str);
  return str.length >= len ? str : " ".repeat(len - str.length) + str;
}

// ── Main ─────────────────────────────────────────────────────────────
const sampleDir = path.join(__dirname, "sample_project");

console.log("=".repeat(70));
console.log("  TOKENLESS CONTEXT COMPRESSION — DEMO");
console.log("=".repeat(70));
console.log();
console.log(`Scanning: ${sampleDir}`);
console.log();

const result = compressProject(sampleDir);

// Per-file table
console.log("-".repeat(70));
console.log(
  pad("File", 30) +
    rpad("Original", 10) +
    rpad("Compressed", 12) +
    rpad("Saved", 8) +
    rpad("  %", 7)
);
console.log("-".repeat(70));

for (const f of result.files) {
  const name = path.relative(sampleDir, f.filePath);
  console.log(
    pad(name, 30) +
      rpad(String(f.originalTokens), 10) +
      rpad(String(f.compressedTokens), 12) +
      rpad(String(f.savedTokens), 8) +
      rpad(f.savingsPercent + "%", 7)
  );
}

console.log("-".repeat(70));
console.log();

// Summary
const pct = parseFloat(result.totalSavingsPercent);
console.log("SUMMARY");
console.log(`  Files scanned:     ${result.fileCount}`);
console.log(`  Original tokens:   ${result.totalOriginal.toLocaleString()}`);
console.log(`  Compressed tokens: ${result.totalCompressed.toLocaleString()}`);
console.log(`  Tokens saved:      ${result.totalSaved.toLocaleString()}`);
console.log(`  Savings:           ${result.totalSavingsPercent}%  ${bar(pct)}`);
console.log();

// Show a before/after snippet for the first file
if (result.files.length > 0) {
  const first = result.files[0];
  const fileName = path.relative(sampleDir, first.filePath);
  console.log("=".repeat(70));
  console.log(`  BEFORE / AFTER — ${fileName}`);
  console.log("=".repeat(70));

  const originalLines = first.original.split("\n");
  const compressedLines = first.compressed.split("\n");

  console.log();
  console.log("--- BEFORE (first 20 lines) ---");
  originalLines.slice(0, 20).forEach((l, i) =>
    console.log(`  ${String(i + 1).padStart(3)}| ${l}`)
  );
  if (originalLines.length > 20) console.log(`  ... (${originalLines.length - 20} more lines)`);

  console.log();
  console.log("--- AFTER (first 20 lines) ---");
  compressedLines.slice(0, 20).forEach((l, i) =>
    console.log(`  ${String(i + 1).padStart(3)}| ${l}`)
  );
  if (compressedLines.length > 20)
    console.log(`  ... (${compressedLines.length - 20} more lines)`);

  console.log();
}

// Compression techniques summary
console.log("=".repeat(70));
console.log("  COMPRESSION TECHNIQUES APPLIED");
console.log("=".repeat(70));
console.log();
console.log("  1. Comment stripping        — block & inline comments removed");
console.log("  2. Whitespace normalization  — collapsed blank lines & indentation");
console.log("  3. Boilerplate removal       — license headers, 'use strict', etc.");
console.log("  4. Import deduplication      — duplicate imports merged");
console.log("  5. Identifier abbreviation   — long repeated names shortened");
console.log();
console.log("These techniques preserve the semantic structure that LLMs need");
console.log("while eliminating tokens that add no informational value.");
console.log();
console.log("=".repeat(70));
console.log("  In a real workflow: npx tokenless");
console.log("  Docs: https://github.com/MaxForAI/Tokenless");
console.log("=".repeat(70));
