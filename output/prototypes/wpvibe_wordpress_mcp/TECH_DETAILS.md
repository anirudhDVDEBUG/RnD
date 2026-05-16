# Technical Details — WPVibe AI MCP Server

## What it does

WPVibe AI (WordPress.org name: "Vibe AI") is a WordPress plugin that registers an SSE-based MCP (Model Context Protocol) endpoint at `/wp-json/wpvibe-ai/v1/mcp`. When an MCP client (Claude Code, Cursor, ChatGPT, Windsurf) connects with a valid Bearer token, the plugin exposes 12+ tools that map to WordPress operations: CRUD on posts/pages, theme file I/O, plugin/theme listing, WP-CLI execution, and raw REST API passthrough. All authorization flows through WordPress's native roles and capabilities system — the API key inherits permissions from the WordPress user who generated it.

The plugin uses WordPress's REST API infrastructure (`register_rest_route`) for the transport layer, then speaks JSON-RPC 2.0 over that HTTP channel. SSE is used for the streaming direction (server-to-client session events and keepalives), while tool calls use standard POST request/response.

## Architecture

```
Claude Code (MCP client)
    │
    ├── SSE GET  ──→  /wp-json/wpvibe-ai/v1/mcp  (session start, keepalives)
    └── POST     ──→  /wp-json/wpvibe-ai/v1/mcp  (JSON-RPC tool calls)
                            │
                    WordPress REST API layer
                            │
                    ┌───────┴───────┐
                    │  WPVibe Plugin │
                    ├───────────────┤
                    │ Auth handler   │  ← Bearer token → WP user capabilities
                    │ Tool registry  │  ← 12 tools (posts, themes, CLI, etc.)
                    │ WP-CLI bridge  │  ← shells out to wp-cli if available
                    │ Abilities API  │  ← extensible capability discovery
                    └───────────────┘
                            │
                    WordPress core (wpdb, WP_Query, etc.)
```

### Key files in the source repo

| Path | Purpose |
|------|---------|
| `wpvibe-ai-mcp.php` | Plugin bootstrap, REST route registration |
| `includes/class-mcp-server.php` | JSON-RPC dispatcher, SSE session management |
| `includes/tools/` | One class per MCP tool (posts, pages, themes, cli, etc.) |
| `includes/class-auth.php` | API key generation, Bearer token validation |
| `includes/class-abilities.php` | WordPress Abilities API integration |
| `admin/settings.php` | Admin UI for key management and capability scoping |

### Dependencies

- **Runtime:** WordPress 6.0+, PHP 7.4+. No external PHP packages — uses only WordPress core APIs.
- **Optional:** WP-CLI (for `wp_cli` tool). If WP-CLI is not installed, that tool returns an error.
- **Client side:** Any MCP client that supports SSE transport (Claude Code, Cursor, etc.).

### Data flow for a tool call

1. Client sends `POST /wp-json/wpvibe-ai/v1/mcp` with `Authorization: Bearer <key>` and JSON-RPC body `{ method: "tools/call", params: { name: "wp_create_post", arguments: { title: "...", content: "..." } } }`.
2. WordPress REST layer routes to the plugin's callback.
3. Auth handler validates the Bearer token, resolves it to a WP user, checks `current_user_can('edit_posts')`.
4. Tool handler calls `wp_insert_post()` (or equivalent WP function).
5. Result is returned as JSON-RPC response with `content: [{ type: "text", text: "..." }]`.

## Limitations

- **SSE only** — no stdio or WebSocket transport. The client must support SSE-based MCP.
- **No file uploads via MCP tools** — media management is limited to metadata; binary uploads require separate endpoints.
- **WP-CLI requires shell access** — shared hosting without CLI access cannot use the `wp_cli` tool.
- **Single-site only** — multisite networks are not fully supported (tools operate on the site where the plugin is installed).
- **No real-time streaming of long operations** — WP-CLI commands that take minutes will time out at the HTTP layer.
- **Security surface** — exposing theme file editing and WP-CLI via an API key is powerful but risky. A leaked key with admin capabilities gives full site control.

## Why this matters for Claude-driven products

### Content marketing / lead-gen pipelines
Claude Code + WPVibe = fully automated content pipeline. An agent can research a topic, draft a post, create it as a WordPress draft, even assign categories and tags — without a human touching wp-admin. For agencies running 10+ WordPress sites, this is the connector that lets a single Claude Code workflow publish across all of them.

### Agent factories
WPVibe is the "WordPress actuator" in a multi-agent system. A planning agent decides what content to publish; an execution agent uses the WPVibe MCP tools to create the post, update theme banners, or flush caches. The tool surface is clean enough to compose into larger pipelines.

### Ad creative / marketing automation
Theme editing tools let an agent swap out promotional banners, update landing page copy, or inject A/B test variants — all through MCP calls. Combined with analytics tools, this enables closed-loop optimization: read performance data, generate new copy, deploy it, measure again.

### Voice AI / conversational agents
A voice agent could say "publish that blog post we discussed" and the backend uses WPVibe tools to execute the action. The MCP interface abstracts away the WordPress complexity.

## Mock demo (this repo)

The `server.js` in this repo implements a faithful mock of the WPVibe MCP endpoint — same routes, same JSON-RPC protocol, same tool schemas — but with in-memory mock data instead of a real WordPress database. Run `bash run.sh` to see all 12 tools in action.
