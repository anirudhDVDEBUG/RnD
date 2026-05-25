---
name: datasette_agent_chat
description: |
  Set up and configure datasette-agent for agentic chat-based data exploration within Datasette instances.
  Triggers: datasette agent, datasette chat, datasette-agent plugin, agent chat datasette, data exploration agent
---

# Datasette Agent Chat

Configure and use `datasette-agent`, a Datasette plugin that adds an agentic chat interface for natural-language data exploration directly inside Datasette's UI.

## When to use

- "Set up datasette-agent for my Datasette instance"
- "Add an agent chat interface to Datasette"
- "I want to query my Datasette database using natural language"
- "Configure the Jump menu agent chat in Datasette"
- "Install datasette-agent and enable the chat plugin"

## How to use

### 1. Install datasette-agent

```bash
pip install datasette-agent
```

Requires **Datasette >= 1.0a30** for the `makeJumpSections()` JavaScript plugin hook.

### 2. Install or update Datasette if needed

```bash
pip install --upgrade datasette
```

### 3. Enable the plugin

`datasette-agent` is automatically enabled once installed. Launch Datasette as usual:

```bash
datasette serve mydb.db
```

### 4. Use the agent chat

1. Open your Datasette instance in a browser.
2. Press `/` to open the **Jump to** menu.
3. Below the search box, a **"Start a new agent chat"** input appears.
4. Type a natural-language query (e.g., "count entries", "show me the top 10 rows by date") and submit.
5. The agent runs an interactive conversation, executing SQL against your database and returning results.

### 5. JavaScript plugin hook integration

`datasette-agent` leverages the `makeJumpSections()` JavaScript plugin hook introduced in Datasette 1.0a30. This hook lets plugins inject custom UI sections into the Jump menu. No additional configuration is required — the plugin registers itself automatically.

### Key details

- **Current version:** 0.1a4 (alpha)
- **Plugin type:** JavaScript plugin hook (`makeJumpSections`)
- **UI entry point:** Jump menu (triggered by pressing `/`)
- **Capability:** Natural-language agentic queries against any connected Datasette database

## References

- [datasette-agent 0.1a4 announcement](https://simonwillison.net/2026/May/24/datasette-agent/#atom-everything)
- [datasette-agent GitHub releases](https://github.com/datasette/datasette-agent/releases/tag/0.1a4)
- [makeJumpSections() JavaScript plugin hook docs](https://docs.datasette.io/en/latest/javascript_plugins.html#javascript-plugins-makejumpsections)
- [Datasette 1.0a30 changelog](https://docs.datasette.io/en/latest/changelog.html#a30-2026-05-24)
