"""PRTS Terminal Service — interactive REPL for agent orchestration."""

from __future__ import annotations

import cmd
import json
import textwrap
from typing import Any

from orchestrator.dispatcher import Dispatcher

BANNER = r"""
 ____  ____ _____ ____
|  _ \|  _ \_   _/ ___|
| |_) | |_) || | \___ \
|  __/|  _ < | |  ___) |
|_|   |_| \_\|_| |____/   Rebuild Terminal Service v0.1

Type 'help' for available commands.
"""


def _pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, default=str)


class TerminalService(cmd.Cmd):
    prompt = "PRTS> "
    intro = BANNER

    def __init__(self, dispatcher: Dispatcher) -> None:
        super().__init__()
        self.dispatcher = dispatcher

    # -- commands -----------------------------------------------------------

    def do_list(self, _arg: str) -> None:
        """List all registered agents and their status."""
        agents = self.dispatcher.list_agents()
        if not agents:
            print("  (no agents registered)")
            return
        fmt = "  {name:<14} {state:<12} execs={executions}  uptime={uptime_s}s"
        print()
        for a in agents:
            print(fmt.format(**a))
        print()

    def do_status(self, name: str) -> None:
        """Show detailed status for one agent: status <name>"""
        agent = self.dispatcher.get(name.strip())
        if agent is None:
            print(f"  Agent '{name}' not found. Use 'list' to see agents.")
            return
        print(_pretty(agent.status()))

    def do_dispatch(self, arg: str) -> None:
        """Dispatch a task: dispatch <type> [payload]"""
        parts = arg.strip().split(None, 1)
        if not parts:
            print("  Usage: dispatch <task_type> [payload]")
            return
        task_type = parts[0]
        payload = parts[1] if len(parts) > 1 else ""
        result = self.dispatcher.dispatch(task_type, payload)
        print(_pretty(result))

    def do_rebuild(self, name: str) -> None:
        """Rebuild (hot-restart) an agent: rebuild <name>"""
        name = name.strip()
        if not name:
            print("  Usage: rebuild <agent_name>")
            return
        msg = self.dispatcher.rebuild_agent(name)
        print(f"  {msg}")

    def do_help_tasks(self, _arg: str) -> None:
        """Show which task types each agent handles."""
        for info in self.dispatcher.list_agents():
            agent = self.dispatcher.get(info["name"])
            if agent:
                types = ", ".join(agent.task_types) or "(none)"
                print(f"  {agent.name}: {types}")

    def do_exit(self, _arg: str) -> bool:
        """Exit the PRTS terminal."""
        print("  Shutting down PRTS...")
        return True

    do_quit = do_exit
    do_EOF = do_exit

    def default(self, line: str) -> None:
        print(f"  Unknown command: {line}. Type 'help' for options.")

    # -- non-interactive batch mode -----------------------------------------

    def run_batch(self, commands: list[str]) -> None:
        """Execute a list of commands then exit (for demo/testing)."""
        for c in commands:
            print(f"{self.prompt}{c}")
            self.onecmd(c)
            print()

    def run(self) -> None:
        """Start the interactive loop."""
        self.cmdloop()
