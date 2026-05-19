#!/usr/bin/env node
/**
 * DemandBird Social Media Management — Interactive Demo
 *
 * Demonstrates the core workflows: platform listing, post management,
 * content repurposing, analytics, and MCP tool discovery.
 * Uses mock data — no API keys required.
 */

const { DemandBirdClient } = require('./lib/mock-client');
const { listMcpTools } = require('./lib/mcp-server-mock');

let chalk, Table;
try {
  chalk = require('chalk');
  Table = require('cli-table3');
} catch {
  // Fallback if deps not installed
  chalk = { bold: s => s, green: s => s, cyan: s => s, yellow: s => s, magenta: s => s, gray: s => s, white: s => s, red: s => s, blue: s => s, dim: s => s };
  chalk.bold.underline = s => s;
  chalk.bold.cyan = s => s;
  chalk.bold.green = s => s;
  chalk.bold.yellow = s => s;
  chalk.bold.magenta = s => s;
  Table = null;
}

function makeTable(head, colWidths) {
  if (Table) {
    return new Table({ head: head.map(h => chalk.bold(h)), colWidths, wordWrap: true });
  }
  return {
    _rows: [head],
    push(row) { this._rows.push(row); },
    toString() {
      return this._rows.map(r => r.join(' | ')).join('\n');
    },
  };
}

function section(title) {
  console.log('\n' + '='.repeat(60));
  console.log(chalk.bold.cyan(`  ${title}`));
  console.log('='.repeat(60));
}

async function main() {
  console.log(chalk.bold.cyan(`
  ╔═══════════════════════════════════════════════════╗
  ║         DemandBird Social Media Manager           ║
  ║         ── Demo & Evaluation Prototype ──         ║
  ╚═══════════════════════════════════════════════════╝
  `));

  const client = new DemandBirdClient('demo-api-key-12345');

  // ── 1. Connected Platforms ──
  section('1. Connected Platforms');
  const platforms = await client.listPlatforms();
  const platTable = makeTable(['Platform', 'Status', 'Handle'], [20, 14, 22]);
  for (const p of platforms) {
    platTable.push([
      p.name.charAt(0).toUpperCase() + p.name.slice(1),
      chalk.green('Connected'),
      chalk.gray(p.handle),
    ]);
  }
  console.log(platTable.toString());

  // ── 2. Content Pipeline ──
  section('2. Content Pipeline — All Posts');
  const allPosts = await client.listPosts();
  const postTable = makeTable(['ID', 'Status', 'Platforms', 'Content'], [12, 12, 20, 40]);
  for (const p of allPosts) {
    const statusColor = p.status === 'published' ? chalk.green : p.status === 'scheduled' ? chalk.yellow : chalk.gray;
    postTable.push([
      p.id,
      statusColor(p.status),
      p.platforms.join(', '),
      p.content.length > 36 ? p.content.slice(0, 36) + '...' : p.content,
    ]);
  }
  console.log(postTable.toString());

  // ── 3. Create a New Post ──
  section('3. Create & Schedule a New Post');
  const newPost = await client.createPost({
    content: 'Just shipped a major update to our AI content engine. Try the new multi-platform scheduler!',
    platforms: ['twitter', 'linkedin', 'bluesky'],
    scheduledAt: '2026-05-22T10:00:00Z',
  });
  console.log(chalk.green('  Post created successfully:'));
  console.log(`    ID:         ${chalk.bold(newPost.id)}`);
  console.log(`    Status:     ${chalk.yellow(newPost.status)}`);
  console.log(`    Platforms:  ${newPost.platforms.join(', ')}`);
  console.log(`    Scheduled:  ${newPost.scheduledAt}`);
  console.log(`    Content:    "${newPost.content}"`);

  // ── 4. Content Repurposing ──
  section('4. Content Repurposing — post_001 → 4 Platforms');
  const repurposed = await client.repurposePost('post_001', ['linkedin', 'bluesky', 'threads', 'substack']);
  console.log(`  Original: ${chalk.cyan(repurposed.originalId)}\n`);
  for (const v of repurposed.variants) {
    console.log(`  ${chalk.bold(v.platform.toUpperCase().padEnd(10))} ${chalk.gray(`[${v.status}]`)}`);
    console.log(`    "${v.content}"\n`);
  }

  // ── 5. Analytics Dashboard ──
  section('5. Analytics Dashboard');
  const analytics = await client.getAnalytics();
  const summaryTable = makeTable(['Metric', 'Value'], [24, 20]);
  summaryTable.push(['Published Posts', String(analytics.totalPosts)]);
  summaryTable.push(['Total Impressions', analytics.impressions.toLocaleString()]);
  summaryTable.push(['Total Likes', String(analytics.likes)]);
  summaryTable.push(['Total Shares', String(analytics.shares)]);
  summaryTable.push(['Total Comments', String(analytics.comments)]);
  summaryTable.push(['Engagement Rate', chalk.green(analytics.engagementRate)]);
  console.log(summaryTable.toString());

  console.log(chalk.bold('\n  Platform Breakdown:'));
  const breakTable = makeTable(['Platform', 'Posts', 'Impressions'], [20, 10, 18]);
  for (const [plat, data] of Object.entries(analytics.platformBreakdown)) {
    breakTable.push([plat.charAt(0).toUpperCase() + plat.slice(1), String(data.posts), data.impressions.toLocaleString()]);
  }
  console.log(breakTable.toString());

  // ── 6. MCP Tools Discovery ──
  section('6. MCP Server — Available Tools');
  const tools = listMcpTools();
  for (const tool of tools) {
    console.log(`  ${chalk.bold.magenta(tool.name)}`);
    console.log(`    ${chalk.gray(tool.description)}`);
    const params = Object.keys(tool.inputSchema.properties || {});
    if (params.length) {
      console.log(`    Params: ${params.join(', ')}`);
    }
    console.log();
  }

  // ── Summary ──
  console.log('='.repeat(60));
  console.log(chalk.bold.green('  Demo complete. All workflows executed with mock data.'));
  console.log(chalk.gray('  See HOW_TO_USE.md for real setup with API keys.'));
  console.log('='.repeat(60) + '\n');
}

main().catch(err => {
  console.error('Demo error:', err.message);
  process.exit(1);
});
