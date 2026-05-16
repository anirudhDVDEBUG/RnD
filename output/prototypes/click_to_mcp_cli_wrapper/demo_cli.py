"""
Demo Click CLI application: a simple "devtools" suite.

This CLI has several commands that simulate useful developer utilities.
The purpose is to show how click-to-mcp auto-wraps each command as an MCP tool.
"""

import json
import hashlib
import datetime
import click


@click.group()
def cli():
    """DevTools CLI - a small developer utility belt."""
    pass


@cli.command()
@click.option("--name", required=True, help="Name to greet")
@click.option("--shout", is_flag=True, help="Greet in uppercase")
def greet(name, shout):
    """Greet someone by name."""
    msg = f"Hello, {name}! Welcome to DevTools."
    if shout:
        msg = msg.upper()
    click.echo(msg)


@cli.command()
@click.argument("text")
@click.option(
    "--algorithm",
    type=click.Choice(["md5", "sha1", "sha256"], case_sensitive=False),
    default="sha256",
    help="Hash algorithm to use",
)
def hash(text, algorithm):
    """Compute a hash digest of the given text."""
    h = hashlib.new(algorithm, text.encode()).hexdigest()
    click.echo(json.dumps({"algorithm": algorithm, "input": text, "digest": h}, indent=2))


@cli.command()
@click.option("--format", "fmt", default="%Y-%m-%d %H:%M:%S", help="strftime format string")
def now(fmt):
    """Print the current date/time."""
    click.echo(datetime.datetime.now().strftime(fmt))


@cli.command()
@click.argument("json_string")
@click.option("--indent", default=2, type=int, help="Indentation level")
def prettyjson(json_string, indent):
    """Pretty-print a JSON string."""
    try:
        data = json.loads(json_string)
        click.echo(json.dumps(data, indent=indent))
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON: {e}", err=True)


@cli.command()
@click.argument("text")
def wordcount(text):
    """Count words, characters, and lines in text."""
    words = len(text.split())
    chars = len(text)
    lines = text.count("\n") + 1
    click.echo(json.dumps({"words": words, "characters": chars, "lines": lines}, indent=2))


if __name__ == "__main__":
    cli()
