---
name: click_to_mcp_cli_wrapper
description: |
  Auto-wrap any Click or Typer CLI application as an MCP server using click-to-mcp.
  Triggers: wrap CLI as MCP, click to mcp, convert CLI to MCP server, expose CLI tool via MCP, typer MCP bridge
---

# Click-to-MCP CLI Wrapper

Auto-wrap any Click or Typer CLI application as an MCP (Model Context Protocol) server so AI agents can invoke CLI tools natively.

## When to use

- "Wrap my Click CLI as an MCP server"
- "Convert this Typer app to an MCP-compatible tool"
- "Expose my CLI tool to AI agents via MCP"
- "Bridge a Python CLI to Model Context Protocol"
- "Make my Click commands available as MCP tools"

## How to use

### 1. Install click-to-mcp

```bash
pip install click-to-mcp
```

Or install from source:

```bash
git clone https://github.com/Coding-Dev-Tools/click-to-mcp.git
cd click-to-mcp
pip install -e .
```

### 2. Wrap a Click CLI

If you have an existing Click application (e.g., `mycli.py`):

```python
import click
from click_to_mcp import click_to_mcp

@click.group()
def cli():
    """My CLI tool."""
    pass

@cli.command()
@click.option("--name", required=True, help="Name to greet")
def greet(name):
    """Greet someone."""
    click.echo(f"Hello, {name}!")

# Wrap the Click group as an MCP server
mcp_server = click_to_mcp(cli)

if __name__ == "__main__":
    mcp_server.run()
```

### 3. Wrap a Typer CLI

click-to-mcp also supports Typer applications:

```python
import typer
from click_to_mcp import click_to_mcp

app = typer.Typer()

@app.command()
def process(input_file: str, output_file: str = "out.txt"):
    """Process a file."""
    typer.echo(f"Processing {input_file} -> {output_file}")

# Typer apps use Click under the hood, so this works directly
mcp_server = click_to_mcp(typer.main.get_command(app))

if __name__ == "__main__":
    mcp_server.run()
```

### 4. Configure in Claude Desktop or MCP client

Add to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-cli-tool": {
      "command": "python",
      "args": ["path/to/mycli_mcp.py"],
      "env": {}
    }
  }
}
```

### 5. Key features

- **Auto-discovery**: Automatically introspects Click commands, options, and arguments to generate MCP tool definitions
- **Click & Typer support**: Works with both Click groups/commands and Typer applications
- **Zero boilerplate**: One function call (`click_to_mcp()`) wraps your entire CLI
- **Preserves metadata**: Command descriptions, option help text, types, and defaults are carried over to MCP tool schemas
- **Nested groups**: Supports Click command groups with nested subcommands

### Tips

- Each Click command becomes a separate MCP tool
- Option names are converted to tool parameter names
- Required options become required MCP parameters
- Command and option help strings become MCP descriptions
- Use `click.Choice` types to expose enum-like parameters

## References

- **Repository**: https://github.com/Coding-Dev-Tools/click-to-mcp
- **Topics**: mcp-server, cli-wrapper, click, typer, python, developer-tools, model-context-protocol
- **Language**: Python
