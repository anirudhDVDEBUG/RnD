#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

// ── Color helpers (no deps) ─────────────────────────────────────────
const c = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  green: "\x1b[32m",
  cyan: "\x1b[36m",
  yellow: "\x1b[33m",
  magenta: "\x1b[35m",
  white: "\x1b[37m",
  bgCyan: "\x1b[46m",
  bgGreen: "\x1b[42m",
};

function heading(text) {
  console.log(`\n${c.bold}${c.cyan}=== ${text} ===${c.reset}\n`);
}

function ok(text) {
  console.log(`  ${c.green}+${c.reset} ${text}`);
}

function info(text) {
  console.log(`  ${c.dim}${text}${c.reset}`);
}

function label(key, value) {
  console.log(`  ${c.yellow}${key}:${c.reset} ${value}`);
}

// ── Profile data model ──────────────────────────────────────────────
function defaultProfile(name, opts = {}) {
  return {
    name,
    description: opts.description || "",
    skills: opts.skills || [],
    mcpServers: opts.mcpServers || [],
    plugins: opts.plugins || [],
    env: opts.env || {},
  };
}

// ── Core functions ──────────────────────────────────────────────────
function initProfile(dir, profileName) {
  const cueDir = path.join(dir, ".cue");
  if (!fs.existsSync(cueDir)) fs.mkdirSync(cueDir, { recursive: true });

  const profile = defaultProfile(profileName, {
    description: `Profile for ${path.basename(dir)}`,
  });
  const profilePath = path.join(cueDir, `${profileName}.json`);
  fs.writeFileSync(profilePath, JSON.stringify(profile, null, 2));
  return { profilePath, profile };
}

function listProfiles(dir) {
  const cueDir = path.join(dir, ".cue");
  if (!fs.existsSync(cueDir)) return [];
  return fs
    .readdirSync(cueDir)
    .filter((f) => f.endsWith(".json") && f !== "active.json")
    .map((f) => {
      const data = JSON.parse(fs.readFileSync(path.join(cueDir, f), "utf8"));
      return data;
    });
}

function setActive(dir, profileName) {
  const cueDir = path.join(dir, ".cue");
  fs.writeFileSync(
    path.join(cueDir, "active.json"),
    JSON.stringify({ active: profileName })
  );
}

function getActive(dir) {
  const activePath = path.join(dir, ".cue", "active.json");
  if (!fs.existsSync(activePath)) return null;
  return JSON.parse(fs.readFileSync(activePath, "utf8")).active;
}

function loadProfile(dir, profileName) {
  const profilePath = path.join(dir, ".cue", `${profileName}.json`);
  if (!fs.existsSync(profilePath)) return null;
  return JSON.parse(fs.readFileSync(profilePath, "utf8"));
}

function addSkill(dir, profileName, skillName) {
  const profile = loadProfile(dir, profileName);
  if (!profile) return null;
  if (!profile.skills.includes(skillName)) profile.skills.push(skillName);
  const profilePath = path.join(dir, ".cue", `${profileName}.json`);
  fs.writeFileSync(profilePath, JSON.stringify(profile, null, 2));
  return profile;
}

function addMcp(dir, profileName, serverName) {
  const profile = loadProfile(dir, profileName);
  if (!profile) return null;
  if (!profile.mcpServers.includes(serverName))
    profile.mcpServers.push(serverName);
  const profilePath = path.join(dir, ".cue", `${profileName}.json`);
  fs.writeFileSync(profilePath, JSON.stringify(profile, null, 2));
  return profile;
}

function addPlugin(dir, profileName, pluginName) {
  const profile = loadProfile(dir, profileName);
  if (!profile) return null;
  if (!profile.plugins.includes(pluginName))
    profile.plugins.push(pluginName);
  const profilePath = path.join(dir, ".cue", `${profileName}.json`);
  fs.writeFileSync(profilePath, JSON.stringify(profile, null, 2));
  return profile;
}

function renderStatus(profile) {
  label("Profile", `${c.bold}${profile.name}${c.reset}`);
  label("Description", profile.description);
  if (profile.skills.length)
    label("Skills", profile.skills.join(", "));
  if (profile.mcpServers.length)
    label("MCP Servers", profile.mcpServers.join(", "));
  if (profile.plugins.length)
    label("Plugins", profile.plugins.join(", "));
}

// ── Demo scenario ───────────────────────────────────────────────────
function runDemo() {
  const tmpBase = path.join(__dirname, "..", "_demo_workspace");
  if (fs.existsSync(tmpBase))
    fs.rmSync(tmpBase, { recursive: true, force: true });

  const projectA = path.join(tmpBase, "ecommerce-api");
  const projectB = path.join(tmpBase, "marketing-site");
  fs.mkdirSync(projectA, { recursive: true });
  fs.mkdirSync(projectB, { recursive: true });

  console.log(
    `${c.bold}${c.bgCyan}${c.white} CUE  ${c.reset} ${c.bold}Agent Profile Manager — Demo${c.reset}`
  );
  console.log(
    `${c.dim}Per-directory profiles for Claude Code & Codex${c.reset}\n`
  );

  // ── Project A: ecommerce-api ──────────────────────────────────────
  heading("1. Initialize profile in ecommerce-api/");
  const resultA = initProfile(projectA, "default");
  ok(`Created ${path.relative(tmpBase, resultA.profilePath)}`);

  heading("2. Add skills, MCP servers, and plugins");
  addSkill(projectA, "default", "sql-query-builder");
  ok('Added skill "sql-query-builder"');
  addSkill(projectA, "default", "api-design-reviewer");
  ok('Added skill "api-design-reviewer"');
  addMcp(projectA, "default", "postgres-mcp");
  ok('Added MCP server "postgres-mcp"');
  addMcp(projectA, "default", "redis-mcp");
  ok('Added MCP server "redis-mcp"');
  addPlugin(projectA, "default", "eslint-autofix");
  ok('Added plugin "eslint-autofix"');

  setActive(projectA, "default");
  ok('Set active profile to "default"');

  heading("3. Current status for ecommerce-api/");
  const profileA = loadProfile(projectA, "default");
  renderStatus(profileA);

  // ── Create a second profile for staging ───────────────────────────
  heading("4. Create a second profile: staging");
  initProfile(projectA, "staging");
  addSkill(projectA, "staging", "sql-query-builder");
  addMcp(projectA, "staging", "postgres-mcp");
  addMcp(projectA, "staging", "datadog-mcp");
  addPlugin(projectA, "staging", "log-viewer");
  ok('Created profile "staging" with monitoring tools');

  heading("5. List all profiles in ecommerce-api/");
  const profiles = listProfiles(projectA);
  profiles.forEach((p) => {
    const activeTag =
      getActive(projectA) === p.name
        ? ` ${c.bgGreen}${c.white} ACTIVE ${c.reset}`
        : "";
    console.log(
      `  ${c.cyan}*${c.reset} ${c.bold}${p.name}${c.reset}${activeTag}  (${p.skills.length} skills, ${p.mcpServers.length} MCPs, ${p.plugins.length} plugins)`
    );
  });

  heading("6. Switch to staging profile");
  setActive(projectA, "staging");
  ok('Switched active profile to "staging"');
  const stagingProfile = loadProfile(projectA, "staging");
  renderStatus(stagingProfile);

  // ── Project B: marketing-site ─────────────────────────────────────
  heading("7. Initialize a different project: marketing-site/");
  initProfile(projectB, "default");
  addSkill(projectB, "default", "seo-content-optimizer");
  addSkill(projectB, "default", "image-alt-generator");
  addMcp(projectB, "default", "analytics-mcp");
  addPlugin(projectB, "default", "lighthouse-ci");
  setActive(projectB, "default");
  ok("Created and activated marketing-site profile");

  heading("8. Auto-detect: simulating directory change");
  info("Entering ecommerce-api/ ...");
  const detectedA = getActive(projectA);
  ok(`Auto-detected profile: "${detectedA}"`);
  const loadedA = loadProfile(projectA, detectedA);
  renderStatus(loadedA);

  console.log("");
  info("Entering marketing-site/ ...");
  const detectedB = getActive(projectB);
  ok(`Auto-detected profile: "${detectedB}"`);
  const loadedB = loadProfile(projectB, detectedB);
  renderStatus(loadedB);

  // ── Generated file tree ───────────────────────────────────────────
  heading("9. Generated file tree");
  function tree(dir, prefix) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    entries.forEach((e, i) => {
      const isLast = i === entries.length - 1;
      const connector = isLast ? "└── " : "├── ";
      console.log(`${prefix}${connector}${e.name}`);
      if (e.isDirectory()) {
        tree(
          path.join(dir, e.name),
          prefix + (isLast ? "    " : "│   ")
        );
      }
    });
  }
  console.log(`  ${c.bold}_demo_workspace/${c.reset}`);
  tree(tmpBase, "  ");

  // ── Cleanup ───────────────────────────────────────────────────────
  heading("Done");
  console.log(
    `  ${c.dim}Demo workspace created at _demo_workspace/ — inspect the .cue/ dirs.${c.reset}`
  );
  console.log(
    `  ${c.dim}In production, install globally: npm install -g cue-ai${c.reset}\n`
  );
}

// ── CLI entry point ─────────────────────────────────────────────────
const cmd = process.argv[2];
if (cmd === "demo") {
  runDemo();
} else {
  console.log("Usage: node src/cue.js demo");
  console.log("  Runs an end-to-end demo of cue profile management.");
}
