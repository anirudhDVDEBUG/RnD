#!/usr/bin/env python3
"""
Claude Mythos AI Client — Python reference implementation.

A configurable frontend client for Anthropic's Claude API that supports
creative writing, roleplay, and custom prompt formatting with
SillyTavern-compatible prompt templates.
"""

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional


# ---------------------------------------------------------------------------
# Prompt template system
# ---------------------------------------------------------------------------

BUILTIN_TEMPLATES = {
    "creative_writing": {
        "name": "Creative Writing",
        "system_prompt": (
            "You are a world-class creative writing assistant. "
            "Craft vivid, emotionally resonant prose. Use sensory details, "
            "varied sentence structure, and compelling characterization. "
            "Follow the user's genre, tone, and style preferences."
        ),
        "format": "plain",
        "temperature": 0.9,
        "max_tokens": 2048,
    },
    "roleplay": {
        "name": "Roleplay / Character Chat",
        "system_prompt": (
            "You are an expert collaborative storyteller. Stay in character "
            "at all times. Use *asterisks* for actions, dialogue in quotes. "
            "Respond with 2-4 paragraphs that advance the scene, include "
            "sensory detail, and leave an opening for the user to continue."
        ),
        "format": "sillytavern",
        "temperature": 0.85,
        "max_tokens": 1024,
    },
    "general_assistant": {
        "name": "General Assistant",
        "system_prompt": (
            "You are Claude, a helpful, harmless, and honest AI assistant "
            "made by Anthropic. Answer the user's questions clearly and concisely."
        ),
        "format": "plain",
        "temperature": 0.7,
        "max_tokens": 1024,
    },
    "worldbuilding": {
        "name": "Worldbuilding Companion",
        "system_prompt": (
            "You are a worldbuilding consultant specializing in creating "
            "rich, consistent fictional universes. Help the user develop "
            "geography, cultures, magic systems, history, and political "
            "structures. Ask clarifying questions, suggest connections, "
            "and flag inconsistencies."
        ),
        "format": "plain",
        "temperature": 0.8,
        "max_tokens": 2048,
    },
}


# ---------------------------------------------------------------------------
# SillyTavern-compatible prompt formatter
# ---------------------------------------------------------------------------

def format_sillytavern(system_prompt: str, messages: list[dict]) -> list[dict]:
    """
    Wraps messages in SillyTavern-style formatting:
    - System prompt injected as the first message.
    - Character/user labels prepended.
    """
    formatted = [{"role": "user", "content": f"[System: {system_prompt}]\n\nPlease begin."}]
    first = True
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            label = "[User]"
        else:
            label = "[Character]"
        if first and role == "user":
            formatted[0]["content"] = f"[System: {system_prompt}]\n\n{label} {content}"
            first = False
        else:
            formatted.append({"role": role, "content": f"{label} {content}"})
    return formatted


def format_plain(system_prompt: str, messages: list[dict]) -> tuple[str, list[dict]]:
    """Plain format — system prompt goes as the API system parameter."""
    return system_prompt, messages


# ---------------------------------------------------------------------------
# Config manager
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.mythos/config.json")


@dataclass
class MythosConfig:
    api_key: str = ""
    model: str = "claude-sonnet-4-20250514"
    active_template: str = "creative_writing"
    custom_templates: dict = field(default_factory=dict)
    base_url: str = "https://api.anthropic.com"

    @classmethod
    def load(cls, path: str = DEFAULT_CONFIG_PATH) -> "MythosConfig":
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        return cls()

    def save(self, path: str = DEFAULT_CONFIG_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    def get_template(self, name: Optional[str] = None) -> dict:
        name = name or self.active_template
        if name in self.custom_templates:
            return self.custom_templates[name]
        if name in BUILTIN_TEMPLATES:
            return BUILTIN_TEMPLATES[name]
        raise KeyError(f"Unknown template: {name}")


# ---------------------------------------------------------------------------
# API client (wraps anthropic SDK or uses mock)
# ---------------------------------------------------------------------------

class MythosClient:
    def __init__(self, config: MythosConfig, mock: bool = False):
        self.config = config
        self.mock = mock
        self._client = None
        if not mock:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=config.api_key)
            except ImportError:
                print("[warn] anthropic SDK not installed — falling back to mock mode")
                self.mock = True

    def chat(self, messages: list[dict], template_name: Optional[str] = None) -> str:
        template = self.config.get_template(template_name)
        system_prompt = template["system_prompt"]
        fmt = template.get("format", "plain")
        temperature = template.get("temperature", 0.7)
        max_tokens = template.get("max_tokens", 1024)

        if self.mock:
            return self._mock_response(system_prompt, messages, template)

        if fmt == "sillytavern":
            api_messages = format_sillytavern(system_prompt, messages)
            system_param = None
        else:
            system_param, api_messages = format_plain(system_prompt, messages)

        kwargs = dict(
            model=self.config.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=api_messages,
        )
        if system_param:
            kwargs["system"] = system_param

        response = self._client.messages.create(**kwargs)
        return response.content[0].text

    def _mock_response(self, system_prompt: str, messages: list[dict], template: dict) -> str:
        last_msg = messages[-1]["content"] if messages else "(empty)"
        tname = template["name"]
        return (
            f"--- MOCK RESPONSE (template: {tname}) ---\n"
            f"Model: {self.config.model}\n"
            f"Temperature: {template.get('temperature', 0.7)}\n"
            f"Format: {template.get('format', 'plain')}\n"
            f"System prompt: {system_prompt[:80]}...\n"
            f"User said: {last_msg[:120]}\n"
            f"---\n"
            f"[This is where Claude's creative response would appear. "
            f"The client has formatted your prompt using the '{tname}' template, "
            f"applied the system prompt, and would send it to the Anthropic API "
            f"using model {self.config.model}.]\n"
        )


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------

def list_templates(config: MythosConfig):
    print("\n  Available prompt templates:")
    print("  " + "-" * 50)
    all_templates = {**BUILTIN_TEMPLATES, **config.custom_templates}
    for key, tmpl in all_templates.items():
        active = " <-- active" if key == config.active_template else ""
        print(f"    {key:24s} {tmpl['name']}{active}")
    print()


def show_template_detail(config: MythosConfig, name: str):
    try:
        tmpl = config.get_template(name)
    except KeyError:
        print(f"  [error] Unknown template: {name}")
        return
    print(f"\n  Template: {tmpl['name']}")
    print(f"  Format:      {tmpl.get('format', 'plain')}")
    print(f"  Temperature: {tmpl.get('temperature', 0.7)}")
    print(f"  Max tokens:  {tmpl.get('max_tokens', 1024)}")
    print(f"  System prompt:\n    {tmpl['system_prompt']}\n")


def interactive_session(client: MythosClient):
    print("\n  Claude Mythos AI — Interactive Session")
    print("  Type /help for commands, /quit to exit.\n")
    messages = []

    while True:
        try:
            user_input = input("  You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if not user_input:
            continue
        if user_input == "/quit":
            print("  Goodbye!")
            break
        if user_input == "/help":
            print("  Commands: /templates, /use <name>, /inspect <name>, /clear, /quit")
            continue
        if user_input == "/templates":
            list_templates(client.config)
            continue
        if user_input.startswith("/use "):
            name = user_input[5:].strip()
            try:
                client.config.get_template(name)
                client.config.active_template = name
                print(f"  Switched to template: {name}")
            except KeyError:
                print(f"  [error] Unknown template: {name}")
            continue
        if user_input.startswith("/inspect "):
            show_template_detail(client.config, user_input[9:].strip())
            continue
        if user_input == "/clear":
            messages = []
            print("  Conversation cleared.")
            continue

        messages.append({"role": "user", "content": user_input})
        response = client.chat(messages)
        messages.append({"role": "assistant", "content": response})
        print(f"\n  Claude> {response}\n")
