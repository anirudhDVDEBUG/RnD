# How to Use click-to-mcp

## Install

```bash
pip install click-to-mcp
```

This pulls in `click` and `mcp` (the MCP SDK) as dependencies.

To install from source:

```bash
git clone https://github.com/Coding-Dev-Tools/click-to-mcp.git
cd click-to-mcp
pip install -e .
```

## MCP Server Configuration

Add this to your `~/.claude.json` (or `claude_desktop_config.json`) under the `mcpServers` key:

```json
{
  "mcpServers": {
    "devtools": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {}
    }
  }
}
```

Replace the path with wherever your MCP wrapper script lives. After saving, restart Claude Desktop or your MCP client. The tools (`greet`, `hash`, `now`, `prettyjson`, `wordcount`) will appear automatically.

## First 60 Seconds

### 1. Run the demo CLI directly

```bash
$ python3 demo_cli.py greet --name "World"
Hello, World! Welcome to DevTools.

$ python3 demo_cli.py hash "test" --algorithm md5
{
  "algorithm": "md5",
  "input": "test",
  "digest": "098f6bcd4621d373cade4e832627b4f6"
}
```

### 2. Wrap it as MCP (one line)

```python
from demo_cli import cli
from click_to_mcp import click_to_mcp

mcp_server = click_to_mcp(cli)
mcp_server.run()  # now serving over stdio MCP protocol
```

### 3. Run end-to-end

```bash
bash run.sh
```

This installs dependencies, runs each CLI command, verifies the MCP server can be created, and prints the config snippet.

### 4. Use from Claude

Once configured, ask Claude:

- "Hash the string 'hello' with sha256"
- "What time is it?"
- "Pretty-print this JSON: {\"a\":1}"

Claude will call the corresponding MCP tools automatically.

## Wrapping Your Own CLI

If you have an existing Click app:

```python
# your_app_mcp.py
from your_app import cli           # your Click group
from click_to_mcp import click_to_mcp

mcp_server = click_to_mcp(cli)

if __name__ == "__main__":
    mcp_server.run()
```

For Typer apps (which use Click under the hood):

```python
import typer
from click_to_mcp import click_to_mcp

app = typer.Typer()

@app.command()
def do_something(name: str):
    typer.echo(f"Done: {name}")

mcp_server = click_to_mcp(typer.main.get_command(app))

if __name__ == "__main__":
    mcp_server.run()
```

## Key Mapping Rules

| Click concept | MCP equivalent |
|---------------|---------------|
| `@cli.command()` | One MCP tool |
| `@click.option("--foo")` | Tool parameter `foo` |
| `required=True` | Required MCP parameter |
| `click.Choice(["a","b"])` | Enum parameter |
| Command docstring | Tool description |
| Option `help=` | Parameter description |
| Nested `@click.group()` | Flattened tool namespace |
