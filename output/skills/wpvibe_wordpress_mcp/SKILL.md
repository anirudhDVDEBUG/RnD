---
name: wpvibe_wordpress_mcp
description: |
  Connect Claude Code to a self-hosted WordPress site via the WPVibe AI MCP server plugin.
  TRIGGER: when user mentions WordPress MCP, WPVibe, Vibe AI plugin, managing WordPress with AI,
  editing WordPress themes/content via Claude, or connecting Claude to WordPress.
---

# WPVibe — WordPress MCP Server

Connect Claude Code to a self-hosted WordPress site using the WPVibe AI MCP server plugin (listed on WordPress.org as "Vibe AI"). This enables theme editing, content management, REST API access, WP-CLI commands, and the WordPress Abilities API — all from within Claude Code.

## When to use

- "Connect Claude to my WordPress site"
- "Set up MCP for WordPress so I can manage content with AI"
- "Edit my WordPress theme using Claude Code"
- "Run WP-CLI commands on my WordPress site through Claude"
- "I want to manage WordPress posts and pages with AI"

## How to use

### 1. Install the WordPress plugin

1. In your WordPress admin dashboard, go to **Plugins → Add New**.
2. Search for **"Vibe AI"** (or "WPVibe") and install the plugin by Awesome Motive.
3. Activate the plugin.
4. Go to **Settings → Vibe AI** in your WordPress admin to configure the plugin and generate an API key/token.

Alternatively, install from source:

```bash
cd /path/to/wordpress/wp-content/plugins
git clone https://github.com/awesomemotive/wpvibe-ai-mcp.git wpvibe-ai-mcp
```

Then activate the plugin in the WordPress admin.

### 2. Configure the MCP client

Add the WPVibe MCP server to your Claude Code MCP configuration. The plugin exposes an SSE-based MCP endpoint on your WordPress site.

In your `.claude/settings.json` or MCP client config, add:

```json
{
  "mcpServers": {
    "wpvibe": {
      "type": "sse",
      "url": "https://your-wordpress-site.com/wp-json/wpvibe-ai/v1/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Replace `your-wordpress-site.com` with your actual WordPress domain and `YOUR_API_KEY` with the token generated in the plugin settings.

### 3. Available capabilities

Once connected, the MCP server exposes tools for:

- **Content Management** — Create, read, update, and delete posts, pages, and custom post types.
- **Theme Editing** — View and modify theme files directly.
- **REST API Access** — Call any WordPress REST API endpoint.
- **WP-CLI Commands** — Execute WP-CLI commands on the server (if WP-CLI is available).
- **WordPress Abilities API** — Discover and use registered WordPress capabilities.
- **Media Management** — Upload and manage media files.
- **Plugin/Theme Info** — List installed plugins and themes, check status.

### 4. Example usage

After configuration, you can ask Claude Code things like:

- "List all draft posts on my WordPress site"
- "Create a new blog post titled 'Hello World' with category 'News'"
- "Update the header.php in my active theme to add a banner"
- "Run `wp plugin list` on my site"
- "Show me the site's REST API index"

### 5. Security notes

- Always use HTTPS for your WordPress site when connecting via MCP.
- Keep your API key secret — do not commit it to version control.
- The plugin respects WordPress user roles and capabilities for authorization.
- Consider restricting the API key's permissions to only the capabilities you need.

## References

- **GitHub repository**: https://github.com/awesomemotive/wpvibe-ai-mcp
- **WordPress.org plugin**: Search for "Vibe AI" by Awesome Motive
- **Topics**: mcp-server, wordpress, ai-assistant, claude, wordpress-mcp, wp-cli
