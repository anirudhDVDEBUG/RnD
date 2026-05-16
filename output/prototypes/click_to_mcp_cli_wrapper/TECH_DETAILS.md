# Technical Details: click-to-mcp

## What It Does

click-to-mcp introspects a Click CLI application at runtime -- walking its command tree, extracting parameters (options, arguments, types, defaults, help text) -- and generates a fully-typed MCP (Model Context Protocol) tool definition for each command. When an MCP client (like Claude Desktop) calls a tool, click-to-mcp reconstructs the Click invocation, runs the command, captures stdout/stderr, and returns the output as an MCP tool result. The entire bridge is created with a single function call: `click_to_mcp(cli)`.

This solves a real friction point: many teams have Python CLIs for internal tooling (deployment scripts, data pipelines, admin commands) but exposing them to AI agents previously required manually writing MCP tool schemas and dispatch logic.

## Architecture

```
Click CLI Group
  |
  +-- command_1 (options, args, help)
  +-- command_2
  +-- nested_group/
       +-- command_3
  |
  v
click_to_mcp(cli)
  |
  +-- Walks click.Group.commands recursively
  +-- For each Command:
  |     - Extracts name, docstring -> MCP tool name + description
  |     - Extracts params (Option/Argument) -> MCP inputSchema
  |     - Maps click.Choice -> enum, click.INT -> integer, etc.
  |     - Tracks required vs optional
  +-- Registers each as an MCP tool handler
  +-- Returns MCP Server object (stdio transport)
  |
  v
MCP Server (stdio)
  |
  +-- Receives JSON-RPC tool calls from client
  +-- Dispatches to Click command via ctx.invoke()
  +-- Captures output, returns as tool result
```

### Key files (in the source repo)

- `click_to_mcp/__init__.py` -- exports `click_to_mcp()` function
- `click_to_mcp/converter.py` -- Click introspection and MCP schema generation
- `click_to_mcp/server.py` -- MCP server setup and tool dispatch

### Dependencies

- **click** (>=8.0) -- the CLI framework being wrapped
- **mcp** -- the Python MCP SDK (provides Server, stdio transport, tool registration)
- No LLM calls, no network requests, no API keys

## Limitations

- **Stdout-only capture**: Commands that write to files, modify databases, or produce side effects beyond stdout will execute those side effects but only return printed output to the MCP client.
- **No streaming**: Long-running commands block until complete; no incremental output.
- **No interactive prompts**: Click commands that use `click.prompt()` or `click.confirm()` will hang -- only fully non-interactive commands work.
- **Type coverage**: Complex custom Click parameter types may not map perfectly to JSON Schema types.
- **Security**: Any MCP client can invoke any wrapped command. There's no built-in auth or permission layer -- scope your CLI carefully.
- **Typer indirection**: Typer apps require `typer.main.get_command(app)` to extract the underlying Click object before wrapping.

## Why This Matters

For teams building Claude-driven products:

- **Agent factories**: If you're building agents that orchestrate internal tools, click-to-mcp lets you expose existing CLIs without rewriting them as custom MCP servers. Your deployment scripts, data transforms, and admin commands become agent-callable in minutes.
- **Lead-gen / marketing**: CLI tools for scraping, CRM updates, or campaign management become AI-accessible without API wrappers.
- **Rapid prototyping**: Test whether a CLI workflow is worth building a full MCP server for -- wrap it in one line, let an agent use it, iterate.
- **Migration path**: Teams with large Click-based tooling can incrementally expose commands to agents without rearchitecting.

The "zero boilerplate" value prop is real: for a 10-command CLI, you skip writing ~200 lines of MCP schema + dispatch code.
