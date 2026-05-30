"""
agent_workflows — lightweight shim demonstrating the owf runtime API.

This is a self-contained demo module that mirrors the public API of
https://github.com/akakabrian/agent-workflows so you can evaluate the
workflow patterns (fan-out, pipeline, validate, budget, resume) without
needing the real package or any API keys.
"""

from .core import Workflow, Step, Adapter, FakeAdapter

__all__ = ["Workflow", "Step", "Adapter", "FakeAdapter"]
