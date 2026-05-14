"""
Discord MCP Control Plane — Mock Server

Demonstrates the MCP tool/resource/prompt surface that DiscordMCP exposes,
without requiring a real Discord bot token. Uses in-memory fake guilds,
channels, members, and messages so `bash run.sh` works out of the box.
"""

import json
import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Mock Discord data layer
# ---------------------------------------------------------------------------

MOCK_GUILDS = {
    "1001": {
        "id": "1001",
        "name": "AI Builders Hub",
        "owner_id": "2001",
        "member_count": 342,
        "channels": {
            "3001": {"id": "3001", "name": "general", "type": "text"},
            "3002": {"id": "3002", "name": "bot-commands", "type": "text"},
            "3003": {"id": "3003", "name": "voice-lounge", "type": "voice"},
        },
        "members": {
            "2001": {"id": "2001", "username": "alice", "roles": ["admin", "member"]},
            "2002": {"id": "2002", "username": "bob", "roles": ["member"]},
            "2003": {"id": "2003", "username": "claude-bot", "roles": ["bot", "member"]},
        },
    },
    "1002": {
        "id": "1002",
        "name": "Marketing Ops",
        "owner_id": "2004",
        "member_count": 58,
        "channels": {
            "3010": {"id": "3010", "name": "campaigns", "type": "text"},
            "3011": {"id": "3011", "name": "analytics", "type": "text"},
        },
        "members": {
            "2004": {"id": "2004", "username": "dana", "roles": ["admin", "member"]},
            "2005": {"id": "2005", "username": "eve", "roles": ["member"]},
        },
    },
}

MOCK_MESSAGES: dict[str, list[dict]] = {
    "3001": [
        {"id": "m1", "author": "alice", "content": "Welcome to the hub!", "timestamp": "2026-05-13T09:00:00Z"},
        {"id": "m2", "author": "bob", "content": "Excited to build with MCP tools.", "timestamp": "2026-05-13T09:05:00Z"},
        {"id": "m3", "author": "claude-bot", "content": "Hello! I can help manage this server via MCP.", "timestamp": "2026-05-13T09:06:00Z"},
    ],
    "3002": [
        {"id": "m4", "author": "bob", "content": "!status", "timestamp": "2026-05-13T10:00:00Z"},
    ],
    "3010": [
        {"id": "m5", "author": "dana", "content": "Q2 campaign brief is ready for review.", "timestamp": "2026-05-13T11:00:00Z"},
    ],
}

_next_msg_id = 100


# ---------------------------------------------------------------------------
# MCP Tool implementations
# ---------------------------------------------------------------------------

def tool_send_message(guild_id: str, channel_id: str, content: str) -> dict:
    global _next_msg_id
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    if channel_id not in guild["channels"]:
        return {"error": f"Channel {channel_id} not found in guild {guild_id}"}
    _next_msg_id += 1
    msg = {
        "id": f"m{_next_msg_id}",
        "author": "claude-bot",
        "content": content,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    MOCK_MESSAGES.setdefault(channel_id, []).append(msg)
    return {"ok": True, "message": msg}


def tool_read_messages(guild_id: str, channel_id: str, limit: int = 10) -> dict:
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    if channel_id not in guild["channels"]:
        return {"error": f"Channel {channel_id} not found"}
    msgs = MOCK_MESSAGES.get(channel_id, [])[-limit:]
    return {"channel": guild["channels"][channel_id]["name"], "messages": msgs}


def tool_list_channels(guild_id: str) -> dict:
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    return {"guild": guild["name"], "channels": list(guild["channels"].values())}


def tool_list_members(guild_id: str) -> dict:
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    return {"guild": guild["name"], "members": list(guild["members"].values())}


def tool_server_info(guild_id: str) -> dict:
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    return {
        "id": guild["id"],
        "name": guild["name"],
        "owner_id": guild["owner_id"],
        "member_count": guild["member_count"],
        "channel_count": len(guild["channels"]),
    }


def tool_create_channel(guild_id: str, name: str, channel_type: str = "text") -> dict:
    guild = MOCK_GUILDS.get(guild_id)
    if not guild:
        return {"error": f"Guild {guild_id} not found"}
    new_id = str(max(int(k) for k in guild["channels"]) + 1)
    ch = {"id": new_id, "name": name, "type": channel_type}
    guild["channels"][new_id] = ch
    return {"ok": True, "channel": ch}


def tool_delete_message(guild_id: str, channel_id: str, message_id: str) -> dict:
    msgs = MOCK_MESSAGES.get(channel_id, [])
    before = len(msgs)
    MOCK_MESSAGES[channel_id] = [m for m in msgs if m["id"] != message_id]
    deleted = before - len(MOCK_MESSAGES[channel_id])
    return {"ok": True, "deleted": deleted}


# ---------------------------------------------------------------------------
# MCP Resource implementations
# ---------------------------------------------------------------------------

def resource_guild_metadata(guild_id: str) -> dict:
    return tool_server_info(guild_id)


def resource_channel_list(guild_id: str) -> dict:
    return tool_list_channels(guild_id)


def resource_message_history(guild_id: str, channel_id: str) -> dict:
    return tool_read_messages(guild_id, channel_id, limit=50)


# ---------------------------------------------------------------------------
# MCP Prompt templates
# ---------------------------------------------------------------------------

PROMPT_TEMPLATES = {
    "summarize_channel": {
        "name": "summarize_channel",
        "description": "Summarize recent activity in a Discord channel",
        "arguments": [
            {"name": "guild_id", "required": True},
            {"name": "channel_id", "required": True},
        ],
        "template": "Read the last 50 messages in channel {channel_id} of guild {guild_id} and provide a concise summary of the discussion topics, key decisions, and action items.",
    },
    "draft_announcement": {
        "name": "draft_announcement",
        "description": "Draft a server announcement",
        "arguments": [
            {"name": "guild_id", "required": True},
            {"name": "topic", "required": True},
        ],
        "template": "Draft a clear, friendly announcement for the server {guild_id} about: {topic}. Keep it under 200 words.",
    },
    "moderate_check": {
        "name": "moderate_check",
        "description": "Check channel for moderation issues",
        "arguments": [
            {"name": "guild_id", "required": True},
            {"name": "channel_id", "required": True},
        ],
        "template": "Review recent messages in channel {channel_id} of guild {guild_id} and flag any messages that may violate community guidelines.",
    },
}


# ---------------------------------------------------------------------------
# MCP manifest (tool list, resource list, prompt list)
# ---------------------------------------------------------------------------

MCP_MANIFEST = {
    "name": "discord-mcp",
    "version": "1.0.0",
    "description": "Multi-server Discord control plane via MCP",
    "tools": [
        {"name": "send_message", "description": "Send a message to a Discord channel", "parameters": ["guild_id", "channel_id", "content"]},
        {"name": "read_messages", "description": "Read recent messages from a channel", "parameters": ["guild_id", "channel_id", "limit"]},
        {"name": "list_channels", "description": "List channels in a guild", "parameters": ["guild_id"]},
        {"name": "list_members", "description": "List members of a guild", "parameters": ["guild_id"]},
        {"name": "server_info", "description": "Get server metadata", "parameters": ["guild_id"]},
        {"name": "create_channel", "description": "Create a new channel", "parameters": ["guild_id", "name", "channel_type"]},
        {"name": "delete_message", "description": "Delete a message by ID", "parameters": ["guild_id", "channel_id", "message_id"]},
    ],
    "resources": [
        {"uri": "discord://guild/{guild_id}/metadata", "description": "Guild metadata"},
        {"uri": "discord://guild/{guild_id}/channels", "description": "Channel listing"},
        {"uri": "discord://guild/{guild_id}/channel/{channel_id}/messages", "description": "Message history"},
    ],
    "prompts": list(PROMPT_TEMPLATES.values()),
}


# ---------------------------------------------------------------------------
# Dispatch helpers
# ---------------------------------------------------------------------------

TOOL_DISPATCH = {
    "send_message": tool_send_message,
    "read_messages": tool_read_messages,
    "list_channels": tool_list_channels,
    "list_members": tool_list_members,
    "server_info": tool_server_info,
    "create_channel": tool_create_channel,
    "delete_message": tool_delete_message,
}


def call_tool(name: str, **kwargs) -> dict:
    fn = TOOL_DISPATCH.get(name)
    if not fn:
        return {"error": f"Unknown tool: {name}"}
    return fn(**kwargs)


def get_resource(uri: str) -> dict:
    parts = uri.replace("discord://", "").split("/")
    if len(parts) >= 3 and parts[0] == "guild" and parts[2] == "metadata":
        return resource_guild_metadata(parts[1])
    if len(parts) >= 3 and parts[0] == "guild" and parts[2] == "channels":
        return resource_channel_list(parts[1])
    if len(parts) >= 5 and parts[2] == "channel" and parts[4] == "messages":
        return resource_message_history(parts[1], parts[3])
    return {"error": f"Unknown resource URI: {uri}"}


def get_prompt(name: str) -> Optional[dict]:
    return PROMPT_TEMPLATES.get(name)
