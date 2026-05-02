#!/usr/bin/env python3
"""PRTS — Rebuild Terminal Service: entry point."""

from __future__ import annotations

import sys

from agents.worker import ResearchAgent, CodeAgent, SummaryAgent
from orchestrator.dispatcher import Dispatcher
from terminal.interface import TerminalService


def build_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.register(ResearchAgent())
    dispatcher.register(CodeAgent())
    dispatcher.register(SummaryAgent())
    return dispatcher


def main() -> None:
    dispatcher = build_dispatcher()
    service = TerminalService(dispatcher)

    if "--demo" in sys.argv:
        # Non-interactive demo for run.sh / CI
        service.run_batch([
            "list",
            "dispatch research multi-agent orchestration",
            "dispatch code fib",
            "dispatch summarize The quick brown fox jumped over the lazy dog and then kept running through the forest",
            "status research",
            "rebuild coder",
            "list",
            "help_tasks",
        ])
    else:
        service.run()


if __name__ == "__main__":
    main()
