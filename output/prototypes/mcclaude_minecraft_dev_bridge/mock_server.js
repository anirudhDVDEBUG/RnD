/**
 * mock_server.js — Simulates a Minecraft server with McClaude plugin.
 * Provides a WebSocket endpoint that mimics the real McClaude bridge,
 * so the MCP server demo can connect without a real Minecraft instance.
 */

const WebSocket = require('ws');

const MOCK_PORT = 25580;

// Simulated console log lines
const CONSOLE_LINES = [
  '[Server] Starting minecraft server version 1.21.4',
  '[Server] Loading properties',
  '[Server] Default game type: SURVIVAL',
  '[Server] Preparing level "world"',
  '[Server] Preparing start region for dimension minecraft:overworld',
  '[Server] Done (3.241s)! For help, type "help"',
  '[Skript] Loading all scripts...',
  '[Skript] Loaded 4 scripts with 12 triggers and 3 commands',
  '[McClaude] Bridge started on port 25580',
  '[McClaude] Encryption: AES-256-GCM active',
  '[Server] Steve joined the game',
  '[Server] Steve has made the advancement [Getting an Upgrade]',
];

// Simulated Skript files on the "server"
const SKRIPT_FILES = {
  'welcome.sk': `on join:
    send "&aWelcome to the server, %player%!" to player
    broadcast "&e%player% &7has joined the game"
    wait 2 seconds
    send "&7Type /help for commands" to player
`,
  'shop.sk': `command /shop:
    trigger:
        open chest inventory with 3 rows named "&6Server Shop" to player
        set slot 0 of player's current inventory to diamond named "&bDiamond" with lore "&7Price: $100"
        set slot 1 of player's current inventory to iron ingot named "&7Iron Ingot" with lore "&7Price: $10"
`,
  'anticheat.sk': `on move:
    if player is not op:
        if player's speed is greater than 5:
            kick player due to "Moving too fast!"
            broadcast "&c%player% was kicked for speed hacking"
`,
  'events.sk': `every 30 minutes:
    broadcast "&6[Event] &eDouble XP is now active for 5 minutes!"
    wait 5 minutes
    broadcast "&6[Event] &7Double XP has ended."
`,
};

// Command responses
const COMMAND_RESPONSES = {
  'list': '[Server] There are 3/20 players online: Steve, Alex, Notch',
  'tps': '[Server] TPS from last 1m, 5m, 15m: 19.98, 19.95, 19.92',
  'version': '[Server] This server is running Paper version git-Paper-196 (MC: 1.21.4)',
  'plugins': '[Server] Plugins (4): McClaude, Skript, WorldEdit, EssentialsX',
  'reload': '[Server] Reload complete.',
  'help': '[Server] Available commands: list, tps, version, plugins, reload, give, tp, gamemode',
  'give Steve diamond 64': '[Server] Gave 64 [Diamond] to Steve',
  'tp Steve 0 100 0': '[Server] Teleported Steve to 0.0, 100.0, 0.0',
  'gamemode creative Steve': '[Server] Set Steve\'s game mode to Creative Mode',
};

function startMockServer() {
  const wss = new WebSocket.Server({ port: MOCK_PORT });
  let consoleIndex = 0;

  console.log(`[MockServer] Minecraft mock server started on ws://localhost:${MOCK_PORT}`);

  wss.on('connection', (ws) => {
    console.log('[MockServer] Client connected (simulating McClaude bridge)');

    ws.on('message', (data) => {
      let msg;
      try {
        msg = JSON.parse(data.toString());
      } catch {
        ws.send(JSON.stringify({ error: 'Invalid JSON' }));
        return;
      }

      const { action, payload } = msg;

      switch (action) {
        case 'read_console': {
          const count = payload?.lines || 5;
          const lines = [];
          for (let i = 0; i < count; i++) {
            lines.push(CONSOLE_LINES[(consoleIndex + i) % CONSOLE_LINES.length]);
          }
          consoleIndex = (consoleIndex + count) % CONSOLE_LINES.length;
          ws.send(JSON.stringify({ action: 'console_output', lines }));
          break;
        }

        case 'run_command': {
          const cmd = (payload?.command || '').trim();
          const response = COMMAND_RESPONSES[cmd] || `[Server] Unknown command: ${cmd}`;
          ws.send(JSON.stringify({ action: 'command_result', command: cmd, output: response }));
          break;
        }

        case 'list_scripts': {
          ws.send(JSON.stringify({
            action: 'script_list',
            files: Object.keys(SKRIPT_FILES),
          }));
          break;
        }

        case 'read_script': {
          const filename = payload?.filename;
          const content = SKRIPT_FILES[filename];
          if (content) {
            ws.send(JSON.stringify({ action: 'script_content', filename, content }));
          } else {
            ws.send(JSON.stringify({ action: 'error', message: `Script not found: ${filename}` }));
          }
          break;
        }

        case 'write_script': {
          const fname = payload?.filename;
          const fcontent = payload?.content;
          if (fname && fcontent) {
            SKRIPT_FILES[fname] = fcontent;
            ws.send(JSON.stringify({ action: 'script_saved', filename: fname }));
          } else {
            ws.send(JSON.stringify({ action: 'error', message: 'Missing filename or content' }));
          }
          break;
        }

        case 'eval': {
          const code = payload?.code || '';
          // Simulate eval results
          ws.send(JSON.stringify({
            action: 'eval_result',
            code,
            result: `Evaluated on server: ${code.substring(0, 50)}... => Success`,
            success: true,
          }));
          break;
        }

        default:
          ws.send(JSON.stringify({ action: 'error', message: `Unknown action: ${action}` }));
      }
    });

    ws.on('close', () => {
      console.log('[MockServer] Client disconnected');
    });
  });

  return wss;
}

module.exports = { startMockServer, MOCK_PORT };

if (require.main === module) {
  startMockServer();
}
