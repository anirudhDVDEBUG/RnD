#!/usr/bin/env python3
"""
CLI entry point for deepseek-loop agent.
Mirrors the Rust CLI's interface: prompt arg, --cron, --allow-* flags.
"""

import argparse
import sys

from deepseek_loop import AgentLoop, PermissionMode
from cron_scheduler import CronScheduler


def main():
    parser = argparse.ArgumentParser(
        prog="deepseek-loop",
        description="Claude-Code-shaped agent loop over the DeepSeek API",
    )
    parser.add_argument("prompt", nargs="?", default=None, help="Prompt to send to the agent")
    parser.add_argument("--model", default="deepseek-chat", help="DeepSeek model to use")
    parser.add_argument("--max-turns", type=int, default=10, help="Maximum agent loop turns")
    parser.add_argument("--cron", default=None, help="Cron expression for recurring runs (e.g. '*/5 * * * *')")
    parser.add_argument("--interval", default=None, help="Simple interval for recurring runs (e.g. '5m')")

    perm_group = parser.add_mutually_exclusive_group()
    perm_group.add_argument("--allow-all", action="store_true", help="Allow all tools without prompting")
    perm_group.add_argument("--allow-read", action="store_true", help="Allow read-only tools without prompting")
    perm_group.add_argument("--allow-bash", action="store_true", help="Allow bash + read tools without prompting")

    args = parser.parse_args()

    # Determine permission mode
    if args.allow_all:
        mode = PermissionMode.ALLOW_ALL
    elif args.allow_bash:
        mode = PermissionMode.ALLOW_BASH
    elif args.allow_read:
        mode = PermissionMode.ALLOW_READ
    else:
        mode = PermissionMode.ASK

    prompt = args.prompt
    if not prompt and not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    if not prompt:
        prompt = "Analyze this codebase and summarize its structure."

    # Cron / interval mode
    if args.cron or args.interval:
        scheduler = CronScheduler()

        def run_task():
            agent = AgentLoop(permission_mode=mode, max_turns=args.max_turns, model=args.model)
            agent.run(prompt)

        if args.interval:
            scheduler.add_interval(args.interval, run_task, name="agent-loop")
        else:
            scheduler.add_cron(args.cron, run_task, name="agent-loop")

        print(f"Scheduler started. Press Ctrl+C to stop.")
        try:
            scheduler.run_loop()
        except KeyboardInterrupt:
            print("\nStopped.")
        return

    # One-shot mode
    agent = AgentLoop(permission_mode=mode, max_turns=args.max_turns, model=args.model)
    agent.run(prompt)
    print()  # final newline


if __name__ == "__main__":
    main()
