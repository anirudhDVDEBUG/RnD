#!/usr/bin/env python3
"""
demo.py — End-to-end walkthrough of the Discord MCP Control Plane.

Runs entirely with mock data (no Discord token or network needed).
Exercises every MCP surface: tools, resources, and prompts.
"""

import json
from discord_mcp_server import (
    MCP_MANIFEST,
    call_tool,
    get_resource,
    get_prompt,
)

SEP = "=" * 64


def pp(label: str, data):
    print(f"\n{SEP}")
    print(f"  {label}")
    print(SEP)
    print(json.dumps(data, indent=2))


def main():
    print()
    print("  Discord MCP Control Plane — Interactive Demo")
    print("  (all data is mock — no Discord token required)")
    print()

    # ── 1. Show MCP manifest ──────────────────────────────────────────
    pp("MCP Manifest (tools / resources / prompts)", MCP_MANIFEST)

    # ── 2. Tool: server_info ──────────────────────────────────────────
    pp(
        "Tool: server_info(guild_id='1001')",
        call_tool("server_info", guild_id="1001"),
    )

    # ── 3. Tool: list_channels ────────────────────────────────────────
    pp(
        "Tool: list_channels(guild_id='1001')",
        call_tool("list_channels", guild_id="1001"),
    )

    # ── 4. Tool: list_members ─────────────────────────────────────────
    pp(
        "Tool: list_members(guild_id='1001')",
        call_tool("list_members", guild_id="1001"),
    )

    # ── 5. Tool: read_messages ────────────────────────────────────────
    pp(
        "Tool: read_messages(guild_id='1001', channel_id='3001')",
        call_tool("read_messages", guild_id="1001", channel_id="3001"),
    )

    # ── 6. Tool: send_message ─────────────────────────────────────────
    pp(
        "Tool: send_message(guild_id='1001', channel_id='3001', ...)",
        call_tool(
            "send_message",
            guild_id="1001",
            channel_id="3001",
            content="Automated update: build #47 passed all checks.",
        ),
    )

    # ── 7. Verify the new message shows up ────────────────────────────
    pp(
        "Tool: read_messages — after send (notice new msg at end)",
        call_tool("read_messages", guild_id="1001", channel_id="3001"),
    )

    # ── 8. Tool: create_channel ───────────────────────────────────────
    pp(
        "Tool: create_channel(guild_id='1001', name='ci-alerts')",
        call_tool("create_channel", guild_id="1001", name="ci-alerts"),
    )

    # ── 9. Tool: delete_message ───────────────────────────────────────
    pp(
        "Tool: delete_message(guild_id='1001', channel_id='3001', message_id='m2')",
        call_tool("delete_message", guild_id="1001", channel_id="3001", message_id="m2"),
    )

    # ── 10. Resource: guild metadata ──────────────────────────────────
    pp(
        "Resource: discord://guild/1002/metadata",
        get_resource("discord://guild/1002/metadata"),
    )

    # ── 11. Resource: channel list ────────────────────────────────────
    pp(
        "Resource: discord://guild/1002/channels",
        get_resource("discord://guild/1002/channels"),
    )

    # ── 12. Resource: message history ─────────────────────────────────
    pp(
        "Resource: discord://guild/1001/channel/3001/messages",
        get_resource("discord://guild/1001/channel/3001/messages"),
    )

    # ── 13. Prompt template ───────────────────────────────────────────
    pp("Prompt: summarize_channel", get_prompt("summarize_channel"))
    pp("Prompt: draft_announcement", get_prompt("draft_announcement"))
    pp("Prompt: moderate_check", get_prompt("moderate_check"))

    # ── 14. Multi-server demo ─────────────────────────────────────────
    pp(
        "Multi-server: server_info for 'Marketing Ops' (guild 1002)",
        call_tool("server_info", guild_id="1002"),
    )
    pp(
        "Multi-server: read campaigns channel (guild 1002, ch 3010)",
        call_tool("read_messages", guild_id="1002", channel_id="3010"),
    )

    # ── 15. Error handling ────────────────────────────────────────────
    pp(
        "Error handling: non-existent guild",
        call_tool("server_info", guild_id="9999"),
    )

    print(f"\n{SEP}")
    print("  Demo complete — all 7 tools, 3 resources, 3 prompts exercised.")
    print(f"{SEP}\n")


if __name__ == "__main__":
    main()
