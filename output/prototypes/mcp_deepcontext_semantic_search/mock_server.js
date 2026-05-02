#!/usr/bin/env node
/**
 * Mock mcp-deepcontext server — simulates symbol-aware semantic search.
 *
 * This demonstrates the MCP tool interface that mcp-deepcontext exposes
 * without requiring an actual embedding model or running MCP transport.
 *
 * In production, the real server:
 *   1. Parses source files with tree-sitter to extract symbols
 *   2. Generates embeddings (local or API-based)
 *   3. Stores vectors in an in-memory HNSW index
 *   4. Serves results over MCP stdio transport
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname, relative } from 'path';

// ── Symbol extraction (simplified tree-sitter stand-in) ────────────────

const SYMBOL_PATTERNS = [
  // TypeScript / JavaScript
  { regex: /export\s+(?:async\s+)?function\s+(\w+)/g, kind: 'function' },
  { regex: /export\s+(?:default\s+)?class\s+(\w+)/g,  kind: 'class' },
  { regex: /export\s+interface\s+(\w+)/g,              kind: 'interface' },
  { regex: /export\s+type\s+(\w+)/g,                   kind: 'type' },
  { regex: /export\s+const\s+(\w+)/g,                  kind: 'constant' },
  // Python
  { regex: /^def\s+(\w+)/gm,                           kind: 'function' },
  { regex: /^class\s+(\w+)/gm,                         kind: 'class' },
];

function extractSymbols(filePath, content) {
  const symbols = [];
  const lines = content.split('\n');
  for (const { regex, kind } of SYMBOL_PATTERNS) {
    regex.lastIndex = 0;
    let match;
    while ((match = regex.exec(content)) !== null) {
      const lineNum = content.slice(0, match.index).split('\n').length;
      const contextStart = Math.max(0, lineNum - 2);
      const contextEnd = Math.min(lines.length, lineNum + 8);
      symbols.push({
        name: match[1],
        kind,
        file: filePath,
        line: lineNum,
        context: lines.slice(contextStart, contextEnd).join('\n'),
      });
    }
  }
  return symbols;
}

// ── Keyword-based semantic similarity mock ─────────────────────────────
// Real mcp-deepcontext uses vector embeddings; we approximate with
// keyword overlap + synonym expansion so the demo is self-contained.

const SYNONYM_MAP = {
  auth:       ['authenticate', 'authorization', 'token', 'jwt', 'login', 'session', 'credential'],
  database:   ['pool', 'connection', 'query', 'sql', 'transaction', 'postgres', 'db', 'dsn'],
  rate:       ['limiter', 'throttle', 'sliding', 'window', 'hits'],
  user:       ['account', 'register', 'signup', 'profile', 'deactivate', 'login'],
  error:      ['retry', 'rollback', 'catch', 'throw', 'exception'],
  session:    ['token', 'jwt', 'login', 'logout', 'cookie'],
  password:   ['hash', 'bcrypt', 'credential', 'salt'],
  middleware: ['request', 'response', 'next', 'handler', 'express'],
};

function expandQuery(query) {
  const words = query.toLowerCase().split(/\W+/).filter(Boolean);
  const expanded = new Set(words);
  for (const w of words) {
    for (const [key, synonyms] of Object.entries(SYNONYM_MAP)) {
      if (w === key || synonyms.includes(w)) {
        expanded.add(key);
        synonyms.forEach(s => expanded.add(s));
      }
    }
  }
  return expanded;
}

function scoreSemantic(symbol, queryTerms) {
  const blob = `${symbol.name} ${symbol.kind} ${symbol.context}`.toLowerCase();
  let score = 0;
  for (const term of queryTerms) {
    const count = (blob.match(new RegExp(term, 'g')) || []).length;
    score += count;
  }
  // Boost exact name matches
  for (const term of queryTerms) {
    if (symbol.name.toLowerCase().includes(term)) score += 5;
  }
  return score;
}

// ── Indexer ────────────────────────────────────────────────────────────

function indexDirectory(dir) {
  const allSymbols = [];
  const exts = new Set(['.ts', '.js', '.tsx', '.jsx', '.py']);

  function walk(d) {
    for (const entry of readdirSync(d)) {
      const full = join(d, entry);
      if (statSync(full).isDirectory()) {
        if (!entry.startsWith('.') && entry !== 'node_modules') walk(full);
      } else if (exts.has(extname(entry))) {
        const content = readFileSync(full, 'utf-8');
        const rel = relative(dir, full);
        allSymbols.push(...extractSymbols(rel, content));
      }
    }
  }
  walk(dir);
  return allSymbols;
}

// ── MCP tool handlers (mock) ──────────────────────────────────────────

export function handleSemanticSearch(index, query, topK = 5) {
  const terms = expandQuery(query);
  const scored = index
    .map(sym => ({ ...sym, score: scoreSemantic(sym, terms) }))
    .filter(s => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
  return scored;
}

export function handleSymbolLookup(index, symbolName) {
  const lower = symbolName.toLowerCase();
  return index.filter(s => s.name.toLowerCase().includes(lower));
}

export function handleIndexProject(dir) {
  const symbols = indexDirectory(dir);
  return { symbolCount: symbols.length, symbols };
}

// ── CLI entry point ───────────────────────────────────────────────────

export { indexDirectory, expandQuery };
