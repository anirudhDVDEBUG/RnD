"""Load profiles, routing rules, hooks, and workflows from YAML configs."""

import os
from pathlib import Path

import yaml

from .models import AgentProfile, HookConfig, RoutingRule, Workflow, WorkflowStep


def load_profiles(profiles_dir: str) -> dict[str, AgentProfile]:
    """Load all agent profiles from a directory of YAML files."""
    profiles = {}
    profiles_path = Path(profiles_dir)
    if not profiles_path.exists():
        return profiles
    for f in sorted(profiles_path.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh) or {}
        name = data.get("agent", f.stem)
        profiles[name] = AgentProfile(
            agent=name,
            strengths=data.get("strengths", []),
            context_window=data.get("context_window", "medium"),
            preferred_tasks=data.get("preferred_tasks", []),
        )
    return profiles


def load_routing(routing_file: str) -> tuple[list[RoutingRule], str]:
    """Load routing rules and fallback agent from a YAML file."""
    with open(routing_file) as fh:
        data = yaml.safe_load(fh) or {}
    rules = []
    for r in data.get("rules", []):
        rules.append(RoutingRule(
            pattern=r["pattern"],
            route_to=r["route_to"],
            priority=r.get("priority", "medium"),
        ))
    fallback = data.get("fallback", "claude")
    return rules, fallback


def load_hooks(hooks_file: str) -> HookConfig:
    """Load hook configuration from a YAML file."""
    with open(hooks_file) as fh:
        data = yaml.safe_load(fh) or {}
    return HookConfig(
        pre_task=data.get("pre_task", []),
        post_task=data.get("post_task", []),
        handoff=data.get("handoff", []),
    )


def load_workflow(workflow_file: str) -> Workflow:
    """Load a multi-agent workflow from a YAML file."""
    with open(workflow_file) as fh:
        data = yaml.safe_load(fh) or {}
    steps = []
    for s in data.get("steps", []):
        steps.append(WorkflowStep(
            agent=s["agent"],
            task=s["task"],
            input_path=s.get("input"),
            output_path=s.get("output"),
        ))
    return Workflow(name=data.get("name", "unnamed"), steps=steps)
