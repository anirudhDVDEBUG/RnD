#!/usr/bin/env python3
"""
demo.py — Non-interactive demo of Claude Mythos AI client.
Runs entirely with mock data (no API key needed).
"""

from mythos_client import MythosConfig, MythosClient, BUILTIN_TEMPLATES, list_templates, show_template_detail

DEMO_CONVERSATIONS = [
    {
        "template": "creative_writing",
        "messages": [
            {"role": "user", "content": "Write the opening paragraph of a noir mystery set in a rain-soaked Tokyo alley."},
        ],
    },
    {
        "template": "roleplay",
        "messages": [
            {"role": "user", "content": "You are Kael, a wandering knight who just entered a cursed forest. Describe what you see."},
        ],
    },
    {
        "template": "worldbuilding",
        "messages": [
            {"role": "user", "content": "I'm building a desert civilization that uses sound-based magic. Help me flesh out the magic system."},
        ],
    },
    {
        "template": "general_assistant",
        "messages": [
            {"role": "user", "content": "Explain the difference between Claude Sonnet and Opus models in two sentences."},
        ],
    },
]


def banner():
    print("=" * 64)
    print("  Claude Mythos AI — Demo Run (mock mode, no API key needed)")
    print("=" * 64)


def run_demo():
    banner()

    config = MythosConfig(model="claude-sonnet-4-20250514")
    client = MythosClient(config, mock=True)

    # 1. Show available templates
    print("\n[1/4] Available prompt templates")
    list_templates(config)

    # 2. Inspect a template
    print("[2/4] Inspecting 'roleplay' template")
    show_template_detail(config, "roleplay")

    # 3. Run demo conversations through each template
    print("[3/4] Running sample conversations\n")
    for i, conv in enumerate(DEMO_CONVERSATIONS, 1):
        tname = conv["template"]
        print(f"  --- Conversation {i}: template={tname} ---")
        config.active_template = tname
        response = client.chat(conv["messages"], tname)
        user_msg = conv["messages"][-1]["content"]
        print(f"  User:   {user_msg}")
        print(f"  Claude: {response}")
        print()

    # 4. Show SillyTavern formatting
    print("[4/4] SillyTavern prompt formatting example\n")
    from mythos_client import format_sillytavern
    template = BUILTIN_TEMPLATES["roleplay"]
    formatted = format_sillytavern(
        template["system_prompt"],
        [{"role": "user", "content": "I draw my sword and step forward."}],
    )
    print("  Formatted messages for API call:")
    for msg in formatted:
        print(f"    [{msg['role']}] {msg['content'][:100]}...")
    print()

    # 5. Config serialization
    print("[5/5] Config serialization (what gets saved to ~/.mythos/config.json)\n")
    import json
    from dataclasses import asdict
    config.active_template = "creative_writing"
    config.api_key = "sk-ant-XXXXX (redacted)"
    print(json.dumps(asdict(config), indent=2))
    print()

    print("=" * 64)
    print("  Demo complete. Run with ANTHROPIC_API_KEY set for live mode.")
    print("  Or launch interactive: python3 main.py --interactive")
    print("=" * 64)


if __name__ == "__main__":
    run_demo()
