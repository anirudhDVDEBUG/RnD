/**
 * demo.js — End-to-end demonstration of the McClaude MCP bridge.
 * Starts a mock Minecraft server, connects as an MCP client, and
 * exercises all four capabilities: console, commands, Skript editing, eval.
 */

const WebSocket = require('ws');
const chalk = require('chalk');
const { startMockServer, MOCK_PORT } = require('./mock_server');

const DIVIDER = chalk.gray('─'.repeat(60));

function header(title) {
  console.log('\n' + DIVIDER);
  console.log(chalk.bold.cyan(`  ${title}`));
  console.log(DIVIDER);
}

function log(label, value) {
  console.log(chalk.yellow(`  [${label}]`) + ' ' + value);
}

function sendAndWait(ws, msg) {
  return new Promise((resolve) => {
    ws.once('message', (data) => resolve(JSON.parse(data.toString())));
    ws.send(JSON.stringify(msg));
  });
}

async function runDemo() {
  console.log(chalk.bold.green('\n  McClaude Minecraft Dev Bridge — Demo'));
  console.log(chalk.gray('  Simulating Claude Code <-> Minecraft server via MCP bridge\n'));

  // 1. Start mock server
  const wss = startMockServer();
  await new Promise((r) => setTimeout(r, 500));

  // 2. Connect client
  const ws = new WebSocket(`ws://localhost:${MOCK_PORT}`);
  await new Promise((resolve, reject) => {
    ws.on('open', resolve);
    ws.on('error', reject);
  });

  // ── Demo 1: Read Console ──────────────────────────────────────
  header('1. Read Server Console');
  const consoleResult = await sendAndWait(ws, {
    action: 'read_console',
    payload: { lines: 6 },
  });
  for (const line of consoleResult.lines) {
    log('CONSOLE', line);
  }

  // ── Demo 2: Run Commands ──────────────────────────────────────
  header('2. Run Server Commands');
  const commands = ['list', 'tps', 'plugins', 'give Steve diamond 64'];
  for (const cmd of commands) {
    const result = await sendAndWait(ws, {
      action: 'run_command',
      payload: { command: cmd },
    });
    log('CMD', chalk.white(`/${cmd}`));
    log('OUT', chalk.green(result.output));
  }

  // ── Demo 3: Edit Skript Files ──────────────────────────────────
  header('3. Skript File Management');

  // List scripts
  const listResult = await sendAndWait(ws, { action: 'list_scripts' });
  log('FILES', `Found ${listResult.files.length} scripts: ${listResult.files.join(', ')}`);

  // Read a script
  const readResult = await sendAndWait(ws, {
    action: 'read_script',
    payload: { filename: 'welcome.sk' },
  });
  console.log(chalk.yellow('  [READ]') + ` welcome.sk:`);
  for (const line of readResult.content.split('\n')) {
    if (line.trim()) console.log(chalk.gray('    | ') + chalk.white(line));
  }

  // Write a modified script
  const newScript = `on join:
    send "&a&lWelcome back, %player%!" to player
    send "&7Server uptime: %server uptime%" to player
    broadcast "&e%player% &7has joined! &a(%number of players%/%max players%)"
    play sound "entity.player.levelup" to player
`;
  const writeResult = await sendAndWait(ws, {
    action: 'write_script',
    payload: { filename: 'welcome.sk', content: newScript },
  });
  log('WRITE', chalk.green(`Saved ${writeResult.filename} with enhanced welcome message`));

  // Verify the write
  const verifyResult = await sendAndWait(ws, {
    action: 'read_script',
    payload: { filename: 'welcome.sk' },
  });
  console.log(chalk.yellow('  [VERIFY]') + ` Updated welcome.sk:`);
  for (const line of verifyResult.content.split('\n')) {
    if (line.trim()) console.log(chalk.gray('    | ') + chalk.white(line));
  }

  // ── Demo 4: Eval Code ─────────────────────────────────────────
  header('4. Evaluate Code on Server');
  const evalSnippets = [
    'Bukkit.getOnlinePlayers().size()',
    'Bukkit.getServer().getTPS()[0]',
    'player.getInventory().addItem(new ItemStack(Material.DIAMOND, 64))',
  ];
  for (const code of evalSnippets) {
    const evalResult = await sendAndWait(ws, {
      action: 'eval',
      payload: { code },
    });
    log('EVAL', chalk.white(code));
    log('RESULT', chalk.green(evalResult.result));
  }

  // ── Summary ───────────────────────────────────────────────────
  header('Summary');
  console.log(chalk.white('  McClaude MCP bridge capabilities demonstrated:'));
  console.log(chalk.green('    [x]') + ' Console reading — live server log streaming');
  console.log(chalk.green('    [x]') + ' Command execution — run any server command');
  console.log(chalk.green('    [x]') + ' Skript editing — read/write .sk files via WebDAV');
  console.log(chalk.green('    [x]') + ' Code eval — execute code snippets on the server');
  console.log('');
  console.log(chalk.gray('  In production, communication is AES-256-GCM encrypted.'));
  console.log(chalk.gray('  See HOW_TO_USE.md for real server setup instructions.'));
  console.log('');

  // Cleanup
  ws.close();
  wss.close();
}

runDemo().catch((err) => {
  console.error(chalk.red('Demo error:'), err.message);
  process.exit(1);
});
