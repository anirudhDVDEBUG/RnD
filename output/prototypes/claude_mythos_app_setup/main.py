#!/usr/bin/env python3
"""
main.py — Entry point for Claude Mythos AI client.

Usage:
    python3 main.py                  # Run demo (mock mode)
    python3 main.py --interactive    # Interactive chat session
    python3 main.py --template NAME  # Use specific template
    python3 main.py --list           # List available templates
"""

import argparse
import os
import sys

from mythos_client import MythosConfig, MythosClient, list_templates, interactive_session


def main():
    parser = argparse.ArgumentParser(description="Claude Mythos AI Client")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive chat")
    parser.add_argument("--template", "-t", default=None, help="Prompt template to use")
    parser.add_argument("--list", "-l", action="store_true", help="List available templates")
    parser.add_argument("--model", "-m", default=None, help="Claude model ID")
    parser.add_argument("--mock", action="store_true", help="Force mock mode (no API calls)")
    args = parser.parse_args()

    # Load or create config
    config = MythosConfig.load()

    # Override with env / flags
    api_key = os.environ.get("ANTHROPIC_API_KEY", config.api_key)
    config.api_key = api_key
    if args.model:
        config.model = args.model
    if args.template:
        config.active_template = args.template

    if args.list:
        list_templates(config)
        return

    use_mock = args.mock or not config.api_key
    if use_mock and not args.mock:
        print("[info] No ANTHROPIC_API_KEY found — running in mock mode.")
        print("[info] Set the env var or run with --mock to suppress this.\n")

    client = MythosClient(config, mock=use_mock)

    if args.interactive:
        interactive_session(client)
    else:
        # Run the demo
        from demo import run_demo
        run_demo()


if __name__ == "__main__":
    main()
