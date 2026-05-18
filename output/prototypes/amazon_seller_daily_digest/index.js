#!/usr/bin/env node
/**
 * Amazon Seller Daily Digest
 * Fetches signals from multiple sources, synthesizes into bilingual digest.
 * In demo mode (no API key), uses mock data to demonstrate the pipeline.
 */

const { fetchAllSources } = require('./src/fetchers');
const { synthesize } = require('./src/synthesizer');
const { formatDigest } = require('./src/formatter');
const { deliver } = require('./src/delivery');

async function main() {
  const today = new Date().toISOString().slice(0, 10);
  console.log(`\n=== AMAZON SELLER DAILY DIGEST (${today}) ===\n`);

  // Step 1: Fetch signals from all sources
  const rawSignals = await fetchAllSources();
  console.log(`[INFO] Collected ${rawSignals.length} signals from sources\n`);

  // Step 2: Synthesize into structured digest
  const digest = await synthesize(rawSignals);

  // Step 3: Format for output
  const formatted = formatDigest(digest);

  // Step 4: Deliver
  await deliver(formatted);
}

main().catch(err => {
  console.error('[ERROR]', err.message);
  process.exit(1);
});
