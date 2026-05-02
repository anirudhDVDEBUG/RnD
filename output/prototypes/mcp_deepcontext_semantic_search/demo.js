#!/usr/bin/env node
/**
 * End-to-end demo of mcp-deepcontext semantic search.
 *
 * Indexes the sample_project/ directory, then runs several semantic
 * queries to show how symbol-aware search differs from plain grep.
 */

import { handleIndexProject, handleSemanticSearch, handleSymbolLookup } from './mock_server.js';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_DIR = join(__dirname, 'sample_project');

// ── Helpers ────────────────────────────────────────────────────────────

function banner(text) {
  const line = '='.repeat(64);
  console.log(`\n${line}`);
  console.log(`  ${text}`);
  console.log(line);
}

function printResults(results) {
  if (results.length === 0) {
    console.log('  (no results)');
    return;
  }
  for (const r of results) {
    const score = r.score !== undefined ? ` (relevance: ${r.score})` : '';
    console.log(`\n  [${r.kind}] ${r.name}${score}`);
    console.log(`    File: ${r.file}:${r.line}`);
    console.log('    Context:');
    for (const line of r.context.split('\n').slice(0, 5)) {
      console.log(`      ${line}`);
    }
  }
}

// ── Main ──────────────────────────────────────────────────────────────

console.log('mcp-deepcontext Semantic Search Demo');
console.log('====================================\n');

// Step 1: Index the project
banner('Step 1: Indexing sample_project/');
const { symbolCount, symbols } = handleIndexProject(PROJECT_DIR);
console.log(`  Indexed ${symbolCount} symbols across sample_project/\n`);
console.log('  Symbols found:');
for (const s of symbols) {
  console.log(`    [${s.kind}] ${s.name} — ${s.file}:${s.line}`);
}

// Step 2: Semantic searches
const queries = [
  'authentication middleware',
  'database connection pooling',
  'rate limiting',
  'user session management',
  'password hashing and credentials',
];

banner('Step 2: Semantic Search Queries');
for (const q of queries) {
  console.log(`\n  Query: "${q}"`);
  console.log('  ' + '-'.repeat(50));
  const results = handleSemanticSearch(symbols, q, 3);
  printResults(results);
}

// Step 3: Symbol lookup
banner('Step 3: Symbol Lookup');
const lookups = ['authenticate', 'pool', 'User'];
for (const name of lookups) {
  console.log(`\n  Lookup: "${name}"`);
  console.log('  ' + '-'.repeat(50));
  const results = handleSymbolLookup(symbols, name);
  printResults(results);
}

// Step 4: Comparison with grep
banner('Step 4: Why Semantic Search Beats grep');
console.log(`
  Query: "user session management"

  grep would search for the literal string "user session management"
  and return ZERO results — none of the files contain that exact phrase.

  Semantic search found:
`);
const sessionResults = handleSemanticSearch(symbols, 'user session management', 3);
for (const r of sessionResults) {
  console.log(`    -> ${r.name} (${r.file}:${r.line}) — relevance ${r.score}`);
}
console.log(`
  The semantic engine understands that "loginUser", "registerUser",
  and "deactivateUser" are all related to session management, even
  though they never mention those exact words together.
`);

console.log('Done. See HOW_TO_USE.md to set up the real MCP server.\n');
