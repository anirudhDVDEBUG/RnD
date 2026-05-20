#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "  Draftspect Office Add-in — Demo Runner"
echo "============================================================"
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
  echo "ERROR: Node.js is required. Install from https://nodejs.org"
  exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --no-audit --no-fund 2>&1 | tail -1
  echo ""
fi

echo "Starting demo server..."
echo ""

# Run the server, but also exercise the API to show output in terminal
node -e "
const app = require('./server');
const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, async () => {
  console.log('');
  console.log('='.repeat(60));
  console.log('  Draftspect Office Add-in Demo');
  console.log('='.repeat(60));
  console.log('');
  console.log('  Server: http://localhost:' + PORT);
  console.log('  Taskpane UI: http://localhost:' + PORT + '/taskpane.html');
  console.log('');

  // Run automated demo sequence
  const http = require('http');

  function apiCall(method, path, body) {
    return new Promise((resolve, reject) => {
      const opts = {
        hostname: 'localhost', port: PORT,
        path, method,
        headers: { 'Content-Type': 'application/json' }
      };
      const req = http.request(opts, res => {
        let data = '';
        res.on('data', c => data += c);
        res.on('end', () => resolve(JSON.parse(data)));
      });
      req.on('error', reject);
      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }

  console.log('─'.repeat(60));
  console.log('  DEMO: Automated API walkthrough');
  console.log('─'.repeat(60));
  console.log('');

  // 1. Show document content
  console.log('1. Reading Word document...');
  const doc = await apiCall('GET', '/api/word/text');
  const lines = doc.text.split('\\\n').slice(0, 5);
  lines.forEach(l => console.log('   │ ' + l));
  console.log('   │ ...');
  console.log('');

  // 2. Show Excel data
  console.log('2. Reading Excel sheet (Revenue)...');
  const sheet = await apiCall('GET', '/api/excel/data/Revenue');
  sheet.data.forEach(row => {
    const formatted = row.map(c => String(c).padEnd(14).slice(0, 14)).join(' │ ');
    console.log('   │ ' + formatted);
  });
  console.log('');

  // 3. Chat: summarize
  console.log('3. Chat: \"Summarize this document\"');
  const sum = await apiCall('POST', '/api/chat', { message: 'Summarize this document' });
  sum.reply.split('\\\n').forEach(l => console.log('   │ ' + l));
  console.log('');

  // 4. Chat: analyze data
  console.log('4. Chat: \"Analyze the revenue data\"');
  const rev = await apiCall('POST', '/api/chat', { message: 'Analyze the revenue data' });
  rev.reply.split('\\\n').forEach(l => console.log('   │ ' + l));
  console.log('');

  // 5. Chat: rewrite
  console.log('5. Chat: \"Rewrite the executive summary\"');
  const rw = await apiCall('POST', '/api/chat', { message: 'Rewrite the executive summary' });
  rw.reply.split('\\\n').forEach(l => console.log('   │ ' + l));
  if (rw.action) {
    console.log('');
    console.log('   ⟶  Proposed action: ' + rw.action.type);
  }
  console.log('');

  console.log('─'.repeat(60));
  console.log('  Demo complete. Open http://localhost:' + PORT + '/taskpane.html');
  console.log('  for the interactive chat UI. Press Ctrl+C to stop.');
  console.log('─'.repeat(60));
  console.log('');
});
"
