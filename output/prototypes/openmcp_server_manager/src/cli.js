#!/usr/bin/env node

/**
 * MCP Server Manager CLI
 * Command-line interface for managing MCP server configurations.
 */

const { MCPServerManager } = require("./manager");

const USAGE = `
mcp-manager - CLI for managing MCP server configurations

Commands:
  add <name> <command> [args...]   Add a new MCP server
  remove <name>                    Remove an MCP server
  list                             List all configured servers
  show <name>                      Show details for a server
  update <name> <field>=<value>    Update a server field
  validate <name>                  Validate a server config
  export                           Export configs for Claude Code
  help                             Show this help message

Options:
  --config <path>   Path to config file (default: ./mcp-servers.json)
  --env KEY=VAL     Set environment variable (use with add)
  --type <type>     Transport type: stdio|sse (default: stdio)

Examples:
  mcp-manager add filesystem node node_modules/.bin/mcp-filesystem /tmp
  mcp-manager add github npx -y @modelcontextprotocol/server-github --env GITHUB_TOKEN=ghp_xxx
  mcp-manager list
  mcp-manager export
`;

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = { command: null, positional: [], flags: {} };

  let i = 0;
  if (args.length > 0 && !args[0].startsWith("--")) {
    parsed.command = args[0];
    i = 1;
  }

  while (i < args.length) {
    if (args[i] === "--config" && i + 1 < args.length) {
      parsed.flags.config = args[++i];
    } else if (args[i] === "--env" && i + 1 < args.length) {
      if (!parsed.flags.env) parsed.flags.env = {};
      const [k, ...vParts] = args[++i].split("=");
      parsed.flags.env[k] = vParts.join("=");
    } else if (args[i] === "--type" && i + 1 < args.length) {
      parsed.flags.type = args[++i];
    } else if (!args[i].startsWith("--")) {
      parsed.positional.push(args[i]);
    }
    i++;
  }

  return parsed;
}

function run(argv) {
  const { command, positional, flags } = parseArgs(argv || process.argv);
  const mgr = new MCPServerManager(flags.config);

  switch (command) {
    case "add": {
      if (positional.length < 2) {
        console.error("Usage: mcp-manager add <name> <command> [args...]");
        process.exit(1);
      }
      const [name, cmd, ...cmdArgs] = positional;
      const result = mgr.add(name, {
        command: cmd,
        args: cmdArgs,
        env: flags.env || {},
        type: flags.type || "stdio",
      });
      console.log(result.message);
      break;
    }

    case "remove": {
      if (positional.length < 1) {
        console.error("Usage: mcp-manager remove <name>");
        process.exit(1);
      }
      const result = mgr.remove(positional[0]);
      console.log(result.message);
      break;
    }

    case "list": {
      const servers = mgr.list();
      if (servers.length === 0) {
        console.log("No MCP servers configured.");
      } else {
        console.log(`\n  MCP Servers (${servers.length}):\n`);
        for (const s of servers) {
          const envCount = s.env ? Object.keys(s.env).length : 0;
          console.log(`  [${s.type || "stdio"}] ${s.name}`);
          console.log(`    command: ${s.command} ${(s.args || []).join(" ")}`);
          if (envCount > 0) console.log(`    env vars: ${envCount}`);
          console.log();
        }
      }
      break;
    }

    case "show": {
      if (positional.length < 1) {
        console.error("Usage: mcp-manager show <name>");
        process.exit(1);
      }
      const server = mgr.get(positional[0]);
      if (!server) {
        console.error(`Server "${positional[0]}" not found.`);
        process.exit(1);
      }
      console.log(JSON.stringify({ [positional[0]]: server }, null, 2));
      break;
    }

    case "validate": {
      if (positional.length < 1) {
        console.error("Usage: mcp-manager validate <name>");
        process.exit(1);
      }
      const result = mgr.validate(positional[0]);
      if (result.valid) {
        console.log(`Server "${positional[0]}" is valid.`);
      } else {
        console.error(`Server "${positional[0]}" has errors:`);
        result.errors.forEach((e) => console.error(`  - ${e}`));
        process.exit(1);
      }
      break;
    }

    case "update": {
      if (positional.length < 2) {
        console.error("Usage: mcp-manager update <name> <field>=<value>");
        process.exit(1);
      }
      const [name, ...updates] = positional;
      const fields = {};
      for (const u of updates) {
        const [k, ...vParts] = u.split("=");
        fields[k] = vParts.join("=");
      }
      const result = mgr.update(name, fields);
      console.log(result.message);
      break;
    }

    case "export": {
      const exported = mgr.exportForClaude();
      if (Object.keys(exported).length === 0) {
        console.log("No servers to export.");
      } else {
        console.log("\nPaste this into your ~/.claude.json mcpServers block:\n");
        console.log(JSON.stringify({ mcpServers: exported }, null, 2));
      }
      break;
    }

    case "help":
    default:
      console.log(USAGE);
  }
}

if (require.main === module) {
  run();
}

module.exports = { run };
