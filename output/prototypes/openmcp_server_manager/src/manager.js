/**
 * MCP Server Configuration Manager
 * Core module for adding, removing, listing, and exporting MCP server configs.
 */

const fs = require("fs");
const path = require("path");

const DEFAULT_CONFIG_PATH = path.join(process.cwd(), "mcp-servers.json");

class MCPServerManager {
  constructor(configPath) {
    this.configPath = configPath || DEFAULT_CONFIG_PATH;
    this.servers = {};
    this._load();
  }

  _load() {
    try {
      if (fs.existsSync(this.configPath)) {
        const raw = fs.readFileSync(this.configPath, "utf-8");
        const data = JSON.parse(raw);
        this.servers = data.mcpServers || {};
      }
    } catch {
      this.servers = {};
    }
  }

  _save() {
    const data = { mcpServers: this.servers };
    fs.writeFileSync(this.configPath, JSON.stringify(data, null, 2), "utf-8");
  }

  add(name, { command, args = [], env = {}, type = "stdio" }) {
    if (this.servers[name]) {
      return { ok: false, message: `Server "${name}" already exists. Use update() to modify.` };
    }
    this.servers[name] = { command, args, env, type };
    this._save();
    return { ok: true, message: `Server "${name}" added.` };
  }

  update(name, fields) {
    if (!this.servers[name]) {
      return { ok: false, message: `Server "${name}" not found.` };
    }
    Object.assign(this.servers[name], fields);
    this._save();
    return { ok: true, message: `Server "${name}" updated.` };
  }

  remove(name) {
    if (!this.servers[name]) {
      return { ok: false, message: `Server "${name}" not found.` };
    }
    delete this.servers[name];
    this._save();
    return { ok: true, message: `Server "${name}" removed.` };
  }

  list() {
    return Object.entries(this.servers).map(([name, config]) => ({
      name,
      ...config,
    }));
  }

  get(name) {
    return this.servers[name] || null;
  }

  exportForClaude() {
    // Export in the format expected by ~/.claude.json mcpServers block
    const out = {};
    for (const [name, config] of Object.entries(this.servers)) {
      out[name] = {
        command: config.command,
        args: config.args || [],
      };
      if (config.env && Object.keys(config.env).length > 0) {
        out[name].env = config.env;
      }
      if (config.type && config.type !== "stdio") {
        out[name].type = config.type;
      }
    }
    return out;
  }

  validate(name) {
    const server = this.servers[name];
    if (!server) return { valid: false, errors: [`Server "${name}" not found.`] };
    const errors = [];
    if (!server.command) errors.push("Missing 'command' field.");
    if (server.args && !Array.isArray(server.args)) errors.push("'args' must be an array.");
    if (server.env && typeof server.env !== "object") errors.push("'env' must be an object.");
    return { valid: errors.length === 0, errors };
  }

  count() {
    return Object.keys(this.servers).length;
  }
}

module.exports = { MCPServerManager };
