#!/usr/bin/env node
/**
 * Tokenless-style context compressor.
 *
 * Scans source files, applies multiple compression passes, and outputs
 * a compact context representation that preserves semantic meaning while
 * dramatically reducing token count.
 *
 * Techniques applied:
 *  1. Comment stripping (block + inline)
 *  2. Whitespace normalization (collapse runs, trim blank lines)
 *  3. Import/require deduplication
 *  4. Boilerplate removal (license headers, auto-generated markers)
 *  5. Symbol summarization (functions → signatures only when body is trivial)
 *  6. Identifier abbreviation mapping for repeated long names
 */

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Token estimation (cl100k_base-ish heuristic: ~4 chars per token on avg)
// ---------------------------------------------------------------------------
function estimateTokens(text) {
  if (!text) return 0;
  // Rough approximation matching cl100k_base behaviour
  const byChars = Math.ceil(text.length / 3.7);
  const byWords = text.split(/\s+/).filter(Boolean).length * 1.3;
  return Math.round((byChars + byWords) / 2);
}

// ---------------------------------------------------------------------------
// Pass 1 – Strip comments
// ---------------------------------------------------------------------------
function stripComments(src, ext) {
  if ([".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".go", ".rs"].includes(ext)) {
    // Remove block comments
    src = src.replace(/\/\*[\s\S]*?\*\//g, "");
    // Remove line comments (but not URLs like https://)
    src = src.replace(/(?<!:)\/\/.*$/gm, "");
  } else if ([".py", ".rb", ".sh", ".yml", ".yaml"].includes(ext)) {
    // Remove # comments (preserve shebangs)
    src = src.replace(/^(\s*)#(?!!).*$/gm, "");
    // Remove Python docstrings
    src = src.replace(/"""[\s\S]*?"""/g, '""');
    src = src.replace(/'''[\s\S]*?'''/g, "''");
  }
  return src;
}

// ---------------------------------------------------------------------------
// Pass 2 – Whitespace normalization
// ---------------------------------------------------------------------------
function normalizeWhitespace(src) {
  // Collapse multiple blank lines into one
  src = src.replace(/\n{3,}/g, "\n\n");
  // Trim trailing whitespace on each line
  src = src.replace(/[ \t]+$/gm, "");
  // Collapse leading indentation beyond 2 levels to 2 levels
  src = src.replace(/^( {8,}|\t{3,})/gm, (m) => "  ".repeat(2));
  return src.trim();
}

// ---------------------------------------------------------------------------
// Pass 3 – Boilerplate removal
// ---------------------------------------------------------------------------
function removeBoilerplate(src) {
  // Strip license/copyright headers (first block comment or consecutive # lines at top)
  src = src.replace(/^(?:\s*(?:\/\*[\s\S]*?\*\/|(?:#[^\n]*\n){3,}))\s*/m, (match) => {
    if (/license|copyright|generated|auto-gen/i.test(match)) return "";
    return match;
  });
  // Strip "use strict"
  src = src.replace(/^['"]use strict['"];?\s*\n/gm, "");
  return src;
}

// ---------------------------------------------------------------------------
// Pass 4 – Import deduplication
// ---------------------------------------------------------------------------
function deduplicateImports(src) {
  const importLines = [];
  const seen = new Set();

  const lines = src.split("\n");
  const result = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (/^(?:import |const .+ = require\(|from |require\()/.test(trimmed)) {
      const key = trimmed.replace(/['"]/g, "").replace(/\s+/g, " ");
      if (seen.has(key)) continue;
      seen.add(key);
      importLines.push(line);
    } else {
      result.push(line);
    }
  }

  if (importLines.length > 0) {
    return importLines.join("\n") + "\n" + result.join("\n");
  }
  return src;
}

// ---------------------------------------------------------------------------
// Pass 5 – Identifier abbreviation map
// ---------------------------------------------------------------------------
function abbreviateIdentifiers(src) {
  // Find long identifiers (>20 chars) that appear 3+ times
  const identRegex = /\b([a-zA-Z_$][a-zA-Z0-9_$]{20,})\b/g;
  const freq = {};
  let m;
  while ((m = identRegex.exec(src)) !== null) {
    freq[m[1]] = (freq[m[1]] || 0) + 1;
  }

  const abbrevMap = {};
  let counter = 0;
  for (const [ident, count] of Object.entries(freq)) {
    if (count >= 3) {
      const abbr = `_${counter++}`;
      abbrevMap[ident] = abbr;
    }
  }

  if (Object.keys(abbrevMap).length === 0) return { src, abbrevMap: {} };

  let compressed = src;
  for (const [full, short] of Object.entries(abbrevMap)) {
    compressed = compressed.replace(new RegExp(`\\b${full}\\b`, "g"), short);
  }

  // Prepend abbreviation legend
  const legend = Object.entries(abbrevMap)
    .map(([full, short]) => `${short}=${full}`)
    .join("; ");
  compressed = `/* ABBREV: ${legend} */\n` + compressed;

  return { src: compressed, abbrevMap };
}

// ---------------------------------------------------------------------------
// Main compressor pipeline
// ---------------------------------------------------------------------------
function compressFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf-8");
  const ext = path.extname(filePath).toLowerCase();

  let compressed = raw;
  compressed = stripComments(compressed, ext);
  compressed = normalizeWhitespace(compressed);
  compressed = removeBoilerplate(compressed);
  compressed = deduplicateImports(compressed);
  const { src: final } = abbreviateIdentifiers(compressed);

  const originalTokens = estimateTokens(raw);
  const compressedTokens = estimateTokens(final);

  return {
    filePath,
    original: raw,
    compressed: final,
    originalTokens,
    compressedTokens,
    savedTokens: originalTokens - compressedTokens,
    savingsPercent:
      originalTokens > 0
        ? ((1 - compressedTokens / originalTokens) * 100).toFixed(1)
        : "0.0",
  };
}

// ---------------------------------------------------------------------------
// Directory scanner
// ---------------------------------------------------------------------------
const DEFAULT_EXTENSIONS = new Set([
  ".js", ".ts", ".jsx", ".tsx", ".py", ".rb", ".go", ".rs",
  ".java", ".c", ".cpp", ".h", ".sh", ".yml", ".yaml", ".md",
  ".json", ".toml", ".cfg", ".ini",
]);

const IGNORE_DIRS = new Set([
  "node_modules", ".git", "__pycache__", ".next", "dist", "build",
  ".tokenless", "coverage", ".venv", "venv",
]);

function scanDirectory(dir, extensions = DEFAULT_EXTENSIONS, maxFiles = 50) {
  const results = [];

  function walk(d) {
    if (results.length >= maxFiles) return;
    let entries;
    try {
      entries = fs.readdirSync(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (results.length >= maxFiles) return;
      if (IGNORE_DIRS.has(entry.name)) continue;
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (extensions.has(path.extname(entry.name).toLowerCase())) {
        try {
          const stat = fs.statSync(full);
          if (stat.size > 0 && stat.size < 200_000) {
            results.push(full);
          }
        } catch {}
      }
    }
  }

  walk(dir);
  return results;
}

// ---------------------------------------------------------------------------
// Compress a whole project
// ---------------------------------------------------------------------------
function compressProject(dir) {
  const files = scanDirectory(dir);
  const fileResults = files.map((f) => compressFile(f));

  const totalOriginal = fileResults.reduce((s, r) => s + r.originalTokens, 0);
  const totalCompressed = fileResults.reduce((s, r) => s + r.compressedTokens, 0);

  return {
    dir,
    fileCount: fileResults.length,
    files: fileResults,
    totalOriginal,
    totalCompressed,
    totalSaved: totalOriginal - totalCompressed,
    totalSavingsPercent:
      totalOriginal > 0
        ? ((1 - totalCompressed / totalOriginal) * 100).toFixed(1)
        : "0.0",
  };
}

module.exports = {
  estimateTokens,
  compressFile,
  compressProject,
  scanDirectory,
  stripComments,
  normalizeWhitespace,
  removeBoilerplate,
  deduplicateImports,
  abbreviateIdentifiers,
};
