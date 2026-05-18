#!/usr/bin/env python3
"""
AI Memory Reader — CLI tool for discovering and browsing AI agent memory files.

Scans known directories for Claude Code, Codex, Cursor, Gemini, and OpenClaw
memory files, then renders a browsable summary in the terminal.
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Try rich for nice output, fall back to plain text
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.tree import Tree
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


@dataclass
class MemoryFile:
    agent: str
    path: Path
    size_bytes: int
    preview: str = ""


@dataclass
class AgentConfig:
    name: str
    base_paths: list
    patterns: list = field(default_factory=lambda: ["*.md", "*.txt", "*.json"])


# Known AI agent memory locations
AGENT_CONFIGS = [
    AgentConfig(
        name="Claude Code",
        base_paths=[
            "~/.claude",
            "~/.claude/projects",
        ],
        patterns=["CLAUDE.md", "*.md", "memory/*.md"],
    ),
    AgentConfig(
        name="Codex",
        base_paths=[
            "~/.codex",
            "~/.codex/memory",
        ],
        patterns=["*.md", "*.txt"],
    ),
    AgentConfig(
        name="Cursor",
        base_paths=[
            "~/.cursor",
            "~/.cursor/rules",
        ],
        patterns=["*.md", "*.mdc", "*.txt"],
    ),
    AgentConfig(
        name="Gemini",
        base_paths=[
            "~/.gemini",
            "~/.gemini/memory",
        ],
        patterns=["*.md", "*.txt", "*.json"],
    ),
    AgentConfig(
        name="OpenClaw",
        base_paths=[
            "~/.openclaw",
            "~/.openclaw/memory",
        ],
        patterns=["*.md", "*.txt"],
    ),
]


def discover_memory_files(configs: list[AgentConfig]) -> list[MemoryFile]:
    """Scan known directories for AI agent memory files."""
    found = []
    for config in configs:
        for base in config.base_paths:
            base_path = Path(base).expanduser()
            if not base_path.exists():
                continue
            for pattern in config.patterns:
                for match in base_path.glob(pattern):
                    if match.is_file():
                        try:
                            content = match.read_text(errors="replace")
                            preview = content[:200].strip()
                            found.append(MemoryFile(
                                agent=config.name,
                                path=match,
                                size_bytes=match.stat().st_size,
                                preview=preview,
                            ))
                        except (PermissionError, OSError):
                            continue
            # Also scan subdirectories one level deep
            if base_path.is_dir():
                for subdir in base_path.iterdir():
                    if subdir.is_dir():
                        for pattern in config.patterns:
                            for match in subdir.glob(pattern):
                                if match.is_file():
                                    try:
                                        content = match.read_text(errors="replace")
                                        preview = content[:200].strip()
                                        found.append(MemoryFile(
                                            agent=config.name,
                                            path=match,
                                            size_bytes=match.stat().st_size,
                                            preview=preview,
                                        ))
                                    except (PermissionError, OSError):
                                        continue
    # Deduplicate by path
    seen = set()
    unique = []
    for mf in found:
        if str(mf.path) not in seen:
            seen.add(str(mf.path))
            unique.append(mf)
    return unique


def generate_mock_files(mock_dir: Path) -> list[MemoryFile]:
    """Generate mock memory files for demonstration purposes."""
    mock_dir.mkdir(parents=True, exist_ok=True)

    mock_data = [
        ("Claude Code", "CLAUDE.md", """# Project Memory

## Preferences
- User prefers Python 3.11+
- Always use type hints
- Run tests before committing

## Architecture Notes
- FastAPI backend at /api
- React frontend at /web
- PostgreSQL for persistence
"""),
        ("Claude Code", "memory/debugging.md", """# Debugging Notes

## 2026-05-15: Auth Token Expiry
- Root cause: JWT refresh logic had off-by-one in expiry check
- Fix: Added 30s buffer before token expiry triggers refresh

## 2026-05-10: Memory Leak in Worker
- Discovered via heaptrack
- Cause: unclosed DB connections in async pool
- Fix: Added context manager pattern to all DB calls
"""),
        ("Codex", "codex_memory.md", """# Codex Session Memory

## Project Context
Working on e-commerce recommendation engine.
Stack: Python, scikit-learn, Redis for caching.

## Key Decisions
- Collaborative filtering over content-based (better cold-start handling)
- Redis TTL set to 1 hour for recommendation cache
- A/B test framework integrated via LaunchDarkly
"""),
        ("Cursor", "cursor_rules.md", """# Cursor Rules

## Code Style
- Use functional components with hooks (no class components)
- Tailwind CSS for styling, no inline styles
- All API calls through centralized api/ directory

## Testing
- Jest + React Testing Library
- Minimum 80% coverage for new code
- E2E tests with Playwright for critical paths
"""),
        ("Gemini", "gemini_context.md", """# Gemini Memory

## User Profile
- Senior developer, 8 years experience
- Primary languages: TypeScript, Python, Rust
- Prefers concise explanations with code examples

## Recent Topics
- WebAssembly optimization techniques
- gRPC vs REST for microservices
- Kubernetes horizontal pod autoscaling
"""),
    ]

    files = []
    for agent, rel_path, content in mock_data:
        file_path = mock_dir / agent.lower().replace(" ", "_") / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        files.append(MemoryFile(
            agent=agent,
            path=file_path,
            size_bytes=len(content.encode()),
            preview=content[:200].strip(),
        ))
    return files


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def display_rich(files: list[MemoryFile], show_content: bool = False):
    """Display results using rich library."""
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]AI Memory Reader[/bold cyan]\n"
        "Discovers and displays AI agent memory files",
        border_style="cyan",
    ))

    # Summary table
    agents = {}
    for f in files:
        agents.setdefault(f.agent, []).append(f)

    table = Table(title="Discovered Memory Files")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Files", justify="right", style="green")
    table.add_column("Total Size", justify="right", style="yellow")

    for agent, agent_files in sorted(agents.items()):
        total = sum(f.size_bytes for f in agent_files)
        table.add_row(agent, str(len(agent_files)), format_size(total))

    console.print(table)
    console.print(f"\n[bold]Total:[/bold] {len(files)} memory files across {len(agents)} agents\n")

    # File tree
    tree = Tree("[bold]Memory Files[/bold]")
    for agent, agent_files in sorted(agents.items()):
        branch = tree.add(f"[cyan]{agent}[/cyan]")
        for f in agent_files:
            branch.add(f"[dim]{f.path.name}[/dim] ({format_size(f.size_bytes)})")

    console.print(tree)

    # Show content previews
    if show_content:
        console.print("\n")
        for f in files:
            console.print(Panel(
                Markdown(f.preview),
                title=f"[cyan]{f.agent}[/cyan] — {f.path.name}",
                border_style="dim",
            ))


def display_plain(files: list[MemoryFile], show_content: bool = False):
    """Fallback plain-text display."""
    print("=" * 60)
    print("  AI Memory Reader")
    print("  Discovers and displays AI agent memory files")
    print("=" * 60)

    agents = {}
    for f in files:
        agents.setdefault(f.agent, []).append(f)

    print(f"\n{'Agent':<15} {'Files':>6} {'Size':>10}")
    print("-" * 35)
    for agent, agent_files in sorted(agents.items()):
        total = sum(f.size_bytes for f in agent_files)
        print(f"{agent:<15} {len(agent_files):>6} {format_size(total):>10}")

    print(f"\nTotal: {len(files)} memory files across {len(agents)} agents\n")

    for agent, agent_files in sorted(agents.items()):
        print(f"\n[{agent}]")
        for f in agent_files:
            print(f"  - {f.path.name} ({format_size(f.size_bytes)})")

    if show_content:
        print("\n" + "=" * 60)
        print("  File Previews")
        print("=" * 60)
        for f in files:
            print(f"\n--- {f.agent} / {f.path.name} ---")
            print(f.preview)
            print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI Memory Reader — browse AI agent memory files")
    parser.add_argument("--mock", action="store_true", help="Use mock data for demonstration")
    parser.add_argument("--content", action="store_true", help="Show file content previews")
    parser.add_argument("--agent", type=str, help="Filter by agent name")
    parser.add_argument("--mock-dir", type=str, default="./.mock_memory",
                        help="Directory for mock data (default: ./.mock_memory)")
    args = parser.parse_args()

    # Discover real files
    real_files = discover_memory_files(AGENT_CONFIGS)

    if args.mock or not real_files:
        mock_dir = Path(args.mock_dir)
        mock_files = generate_mock_files(mock_dir)
        files = real_files + mock_files
        if not real_files:
            if RICH_AVAILABLE:
                from rich.console import Console
                Console().print("[dim]No real memory files found — showing mock data for demo[/dim]\n")
            else:
                print("(No real memory files found — showing mock data for demo)\n")
    else:
        files = real_files

    if args.agent:
        files = [f for f in files if args.agent.lower() in f.agent.lower()]

    if not files:
        print("No memory files found.")
        sys.exit(1)

    if RICH_AVAILABLE:
        display_rich(files, show_content=args.content)
    else:
        display_plain(files, show_content=args.content)


if __name__ == "__main__":
    main()
