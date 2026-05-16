# click-to-mcp: Turn Any Click CLI into an MCP Server in One Line

**One function call wraps your entire Click/Typer CLI as an MCP server** so AI agents (Claude, etc.) can invoke every command natively -- zero boilerplate, zero schema writing.

```
5 Click commands  -->  click_to_mcp(cli)  -->  5 MCP tools, ready to call
```

## Quick look

```python
from click_to_mcp import click_to_mcp
from my_cli import cli          # any Click group

mcp_server = click_to_mcp(cli)  # done
mcp_server.run()
```

Run `bash run.sh` for a full working demo (no API keys needed).

## Docs

| File | What's inside |
|------|--------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, config snippets, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, strategic value |

## Source

<https://github.com/Coding-Dev-Tools/click-to-mcp>
