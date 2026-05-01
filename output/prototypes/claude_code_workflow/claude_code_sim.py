#!/usr/bin/env python3
"""
Claude Code Workflow Simulator

Demonstrates key Claude Code CLI concepts:
- CLI commands and their purposes
- CLAUDE.md project configuration
- Permission modes
- Git workflow integration
- Interactive session simulation

No API key required - uses mock data to illustrate workflows.
"""

import os
import sys
import json
import time
import textwrap
from pathlib import Path

# ANSI colors
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"
RESET = "\033[0m"
BG_DARK = "\033[48;5;236m"

DEMO_DIR = Path("/tmp/claude-code-demo-project")


def banner(text):
    width = 60
    print(f"\n{BOLD}{CYAN}{'=' * width}")
    print(f"  {text}")
    print(f"{'=' * width}{RESET}\n")


def section(text):
    print(f"\n{BOLD}{YELLOW}--- {text} ---{RESET}\n")


def cmd(text):
    print(f"  {DIM}${RESET} {GREEN}{text}{RESET}")


def output(text):
    for line in text.strip().split("\n"):
        print(f"    {line}")


def pause(seconds=0.5):
    time.sleep(seconds)


def demo_cli_commands():
    """Demonstrate core Claude Code CLI commands."""
    banner("1. Claude Code CLI Commands")

    commands = [
        ("claude", "Start interactive REPL session", "Opens an agentic coding session in your terminal"),
        ('claude "fix the login bug"', "One-shot command", "Runs a single task and exits"),
        ('claude -p "explain auth flow"', "Print-only mode", "Read-only analysis, no file changes"),
        ("claude /help", "Show slash commands", "Lists all available in-session commands"),
        ("claude /init", "Initialize project", "Creates CLAUDE.md configuration file"),
        ("claude /compact", "Compress context", "Reduces token usage when context is large"),
        ("claude /cost", "Show usage", "Displays token count and estimated cost"),
        ("claude /commit", "Smart commit", "Generates commit message from staged changes"),
    ]

    print(f"  {'Command':<35} {'Description':<25} {'Detail'}")
    print(f"  {'-'*35} {'-'*25} {'-'*40}")
    for c, desc, detail in commands:
        print(f"  {GREEN}{c:<35}{RESET} {BOLD}{desc:<25}{RESET} {DIM}{detail}{RESET}")
    pause(0.3)


def demo_project_config():
    """Create and show a CLAUDE.md project configuration."""
    banner("2. Project Configuration (CLAUDE.md)")

    claude_md_content = textwrap.dedent("""\
    # CLAUDE.md - Project Configuration

    ## Build & Test
    - Run tests: `pytest tests/ -v`
    - Lint: `ruff check .`
    - Build: `python -m build`

    ## Code Style
    - Use type hints on all public functions
    - Follow PEP 8 naming conventions
    - Max line length: 100 characters

    ## Git Rules
    - Never commit directly to main
    - Use conventional commit messages (feat:, fix:, docs:)
    - Squash merge feature branches

    ## Architecture
    - src/ contains application code
    - tests/ mirrors src/ structure
    - Use dependency injection for services
    """)

    # Create demo project structure
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    claude_md_path = DEMO_DIR / "CLAUDE.md"
    claude_md_path.write_text(claude_md_content)

    print(f"  Created: {CYAN}{claude_md_path}{RESET}\n")
    print(f"{BG_DARK}")
    for line in claude_md_content.strip().split("\n"):
        print(f"  {line}")
    print(f"{RESET}")

    pause(0.3)


def demo_scaffold_project():
    """Create a mock project to demonstrate workflows."""
    banner("3. Demo Project Structure")

    # Create project files
    files = {
        "src/__init__.py": "",
        "src/app.py": textwrap.dedent("""\
            from dataclasses import dataclass

            @dataclass
            class User:
                name: str
                email: str
                active: bool = True

            def get_active_users(users: list[User]) -> list[User]:
                return [u for u in users if u.active]

            def format_greeting(user: User) -> str:
                return f"Hello, {user.name}!"
        """),
        "src/utils.py": textwrap.dedent("""\
            import hashlib

            def hash_email(email: str) -> str:
                return hashlib.sha256(email.encode()).hexdigest()[:12]

            def validate_email(email: str) -> bool:
                return "@" in email and "." in email.split("@")[-1]
        """),
        "tests/__init__.py": "",
        "tests/test_app.py": textwrap.dedent("""\
            from src.app import User, get_active_users, format_greeting

            def test_get_active_users():
                users = [
                    User("Alice", "alice@example.com", True),
                    User("Bob", "bob@example.com", False),
                ]
                active = get_active_users(users)
                assert len(active) == 1
                assert active[0].name == "Alice"

            def test_format_greeting():
                user = User("Alice", "alice@example.com")
                assert format_greeting(user) == "Hello, Alice!"
        """),
    }

    for filepath, content in files.items():
        p = DEMO_DIR / filepath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    # Show tree
    print(f"  Project root: {CYAN}{DEMO_DIR}{RESET}\n")
    tree_lines = [
        "claude-code-demo-project/",
        "  CLAUDE.md",
        "  src/",
        "    __init__.py",
        "    app.py",
        "    utils.py",
        "  tests/",
        "    __init__.py",
        "    test_app.py",
    ]
    for line in tree_lines:
        icon = "dir" if line.rstrip().endswith("/") else "file"
        color = CYAN if icon == "dir" else RESET
        print(f"    {color}{line}{RESET}")

    pause(0.3)


def demo_interactive_session():
    """Simulate an interactive Claude Code session."""
    banner("4. Simulated Interactive Session")

    print(f"  {DIM}Simulating a Claude Code session...{RESET}\n")

    exchanges = [
        {
            "prompt": "What does this project do?",
            "thinking": "Reading src/app.py, src/utils.py, tests/test_app.py...",
            "response": textwrap.dedent("""\
                This project defines a simple User management module:

                - `src/app.py`: User dataclass with `get_active_users()` filter
                  and `format_greeting()` helper
                - `src/utils.py`: Email hashing and validation utilities
                - `tests/test_app.py`: Tests for active user filtering and greetings

                The codebase follows a clean src/tests structure with type hints."""),
        },
        {
            "prompt": "Add an email validation check to User creation",
            "thinking": "Editing src/app.py to import validate_email and add __post_init__...",
            "response": textwrap.dedent("""\
                I've updated `src/app.py` to validate emails on User creation:

                ```diff
                + from src.utils import validate_email
                +
                  @dataclass
                  class User:
                      name: str
                      email: str
                      active: bool = True
                +
                +     def __post_init__(self):
                +         if not validate_email(self.email):
                +             raise ValueError(f"Invalid email: {self.email}")
                ```

                The User dataclass now validates the email format at creation time."""),
        },
        {
            "prompt": "/commit",
            "thinking": "Analyzing staged changes...",
            "response": textwrap.dedent("""\
                Generated commit message:

                  feat: add email validation to User dataclass

                  Imports validate_email from utils and adds __post_init__
                  check to reject invalid email addresses at creation time.

                Commit created: a1b2c3d"""),
        },
    ]

    for ex in exchanges:
        # User prompt
        print(f"  {BOLD}{MAGENTA}> {ex['prompt']}{RESET}")
        pause(0.3)

        # Thinking
        print(f"  {DIM}[thinking] {ex['thinking']}{RESET}")
        pause(0.3)

        # Response
        for line in ex["response"].strip().split("\n"):
            print(f"  {line}")
        print()
        pause(0.3)


def demo_permission_modes():
    """Show permission mode configurations."""
    banner("5. Permission Modes")

    modes = [
        ("Default (interactive)", "Asks before file writes and shell commands",
         "claude", GREEN),
        ("Auto-accept edits", "Trusts file modifications, asks for shell",
         "claude --auto-accept-edits", YELLOW),
        ("Full auto (dangerous)", "Skips all permission prompts",
         "claude --dangerously-skip-permissions", RED),
    ]

    for name, desc, command, color in modes:
        print(f"  {color}{BOLD}{name}{RESET}")
        print(f"    {desc}")
        cmd(command)
        print()

    # Show settings.json allowlist example
    section("Custom Allowlist (settings.json)")
    settings = {
        "permissions": {
            "allow": [
                "Read",
                "Glob",
                "Grep",
                "Bash(npm test)",
                "Bash(npm run lint)",
            ]
        }
    }
    print(f"  {DIM}~/.claude/settings.json:{RESET}")
    for line in json.dumps(settings, indent=2).split("\n"):
        print(f"    {line}")

    pause(0.3)


def demo_piping():
    """Show how to pipe content into Claude Code."""
    banner("6. Piping & Chaining")

    examples = [
        ('cat error.log | claude "fix this error"', "Feed error logs for debugging"),
        ('git diff | claude "review these changes"', "Code review from diff"),
        ('claude -p "list all TODOs" | grep FIXME', "Filter Claude output"),
        ('cat schema.sql | claude "generate Python models"', "Transform formats"),
    ]

    for command, description in examples:
        print(f"  {BOLD}{description}{RESET}")
        cmd(command)
        print()

    pause(0.3)


def demo_best_practices():
    """Show best practices summary."""
    banner("7. Best Practices Summary")

    practices = [
        ("Start in project root", "Claude discovers your full codebase structure"),
        ("Use CLAUDE.md", "Encode conventions, build commands, style preferences"),
        ("Use /compact", "Compress context when conversations get long"),
        ("Review diffs", "Claude shows changes for approval before applying"),
        ("Leverage git integration", "Let Claude write meaningful commit messages"),
        ("Chain with pipes", "Combine with standard Unix tools for power workflows"),
    ]

    for i, (practice, detail) in enumerate(practices, 1):
        print(f"  {GREEN}{i}.{RESET} {BOLD}{practice}{RESET}")
        print(f"     {DIM}{detail}{RESET}")

    pause(0.3)


def demo_workflow_summary():
    """Final workflow summary with metrics."""
    banner("8. Workflow Summary")

    summary = {
        "CLI Commands Demonstrated": 8,
        "Project Files Created": 6,
        "Session Exchanges Simulated": 3,
        "Permission Modes Covered": 3,
        "Piping Examples": 4,
        "Best Practices Listed": 6,
    }

    for key, val in summary.items():
        print(f"  {BOLD}{key}:{RESET} {GREEN}{val}{RESET}")

    print(f"\n  {BOLD}Claude Code turns your terminal into an agentic coding environment.{RESET}")
    print(f"  {DIM}Install: npm install -g @anthropic-ai/claude-code{RESET}")
    print(f"  {DIM}Docs: https://docs.anthropic.com/en/docs/claude-code{RESET}")
    print()


def main():
    print(f"\n{BOLD}{CYAN}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║        Claude Code Workflow — Demo Simulator        ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    print(f"  {DIM}This demo illustrates Claude Code CLI concepts using")
    print(f"  mock data. No API key or installation required.{RESET}")

    demo_cli_commands()
    demo_project_config()
    demo_scaffold_project()
    demo_interactive_session()
    demo_permission_modes()
    demo_piping()
    demo_best_practices()
    demo_workflow_summary()

    print(f"  {GREEN}{BOLD}Demo complete.{RESET}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
