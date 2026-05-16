# How to Use WPVibe AI — WordPress MCP Server

## What this is

A WordPress plugin (listed as "Vibe AI" on WordPress.org) that exposes an SSE-based MCP server on your WordPress site. Once connected, Claude Code can manage posts, pages, themes, plugins, and run WP-CLI commands directly.

## Prerequisites

- A self-hosted WordPress site (6.0+) with HTTPS
- PHP 7.4+ on the server
- Admin access to install plugins
- Claude Code (or any MCP-compatible client)

---

## Step 1: Install the WordPress plugin

**Option A — WordPress admin (recommended):**

1. Go to **Plugins > Add New** in wp-admin.
2. Search for **"Vibe AI"** by Awesome Motive.
3. Click **Install Now**, then **Activate**.
4. Go to **Settings > Vibe AI** and click **Generate API Key**. Copy the key.

**Option B — Git clone:**

```bash
cd /path/to/wordpress/wp-content/plugins
git clone https://github.com/awesomemotive/wpvibe-ai-mcp.git wpvibe-ai-mcp
```

Then activate in wp-admin and generate the API key at Settings > Vibe AI.

## Step 2: Configure Claude Code MCP

Add this block to your `~/.claude.json` (or project-level `.claude/settings.json`), inside the `mcpServers` key:

```json
{
  "mcpServers": {
    "wpvibe": {
      "type": "sse",
      "url": "https://your-site.com/wp-json/wpvibe-ai/v1/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Replace:
- `your-site.com` with your actual WordPress domain
- `YOUR_API_KEY_HERE` with the key from Step 1

Restart Claude Code after saving. The WPVibe tools will appear in your tool list.

## Step 3 (alternative): Use as a Claude Skill

If you want trigger-phrase activation, drop the skill file:

```bash
mkdir -p ~/.claude/skills/wpvibe_wordpress_mcp
# Copy the SKILL.md from the source repo into this directory
```

**Trigger phrases:** "WordPress MCP", "WPVibe", "Vibe AI plugin", "manage WordPress with AI", "edit WordPress theme via Claude", "connect Claude to WordPress".

---

## First 60 seconds

After configuring the MCP server, try these prompts in Claude Code:

```
> List all draft posts on my WordPress site

  Claude calls wp_list_posts(status="draft") and returns:
  ┌────┬──────────────────────────────────┬────────┐
  │ ID │ Title                            │ Status │
  ├────┼──────────────────────────────────┼────────┤
  │  2 │ Getting Started with MCP         │ draft  │
  │  3 │ Theme Customization Guide        │ draft  │
  └────┴──────────────────────────────────┴────────┘

> Create a new post titled "Summer Sale Announcement" in the Marketing category

  Claude calls wp_create_post(title="Summer Sale Announcement",
    content="...", categories=["Marketing"], status="draft")
  → Post created (ID: 547), status: draft

> Read header.php from my active theme

  Claude calls wp_get_theme_file(file="header.php")
  → Returns the full PHP source of your theme header

> Run wp cache flush

  Claude calls wp_cli(command="cache flush")
  → "Success: The cache was flushed."
```

## Available tools (12 total)

| Tool | Description |
|------|-------------|
| `wp_list_posts` | List posts with status/category filters |
| `wp_create_post` | Create a new post (title, content, status, categories) |
| `wp_update_post` | Update post by ID |
| `wp_delete_post` | Trash a post by ID |
| `wp_list_pages` | List all pages |
| `wp_get_theme_file` | Read a file from the active theme |
| `wp_update_theme_file` | Write to a theme file |
| `wp_list_plugins` | List installed plugins and status |
| `wp_list_themes` | List installed themes |
| `wp_cli` | Execute any WP-CLI command |
| `wp_rest_api` | Call any WP REST API endpoint |
| `wp_site_info` | Get site metadata (version, theme, PHP, etc.) |

## Security notes

- **Always use HTTPS** — the API key is sent as a Bearer token.
- **Never commit your API key** to version control.
- The plugin respects WordPress roles and capabilities — the key inherits the generating user's permissions.
- Restrict the key to only the capabilities you need in Settings > Vibe AI.

## Running the mock demo (no WordPress needed)

```bash
bash run.sh
```

This starts a local mock server and exercises all 12 tools with sample WordPress data.
