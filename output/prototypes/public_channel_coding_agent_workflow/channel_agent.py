"""
Public-Channel Coding Agent Workflow
=====================================
A simulation of the Shopify River-style pattern where coding agents
work exclusively in public channels, enabling osmosis learning.
"""

import json
import datetime
import re
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ChannelType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    DM = "im"


@dataclass
class Message:
    user: str
    text: str
    channel: str
    channel_type: ChannelType
    thread_id: Optional[str] = None
    timestamp: str = ""
    reactions: list = field(default_factory=list)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().isoformat()


@dataclass
class AgentResponse:
    text: str
    code: Optional[str] = None
    thread_id: Optional[str] = None
    refused: bool = False


class PublicChannelAgent:
    """Coding agent that only operates in public channels."""

    CHANNEL_PATTERN = re.compile(r"^#\w+_agent$")

    def __init__(self, name: str = "river"):
        self.name = name
        self.history: list[dict] = []

    def handle_message(self, message: Message) -> AgentResponse:
        """Route a message: refuse DMs, process public channel requests."""
        # Rule 1: Refuse DMs
        if message.channel_type == ChannelType.DM:
            return self._refuse_dm(message)

        # Rule 2: Refuse private channels
        if message.channel_type == ChannelType.PRIVATE:
            return self._refuse_private(message)

        # Rule 3: Warn if channel doesn't follow naming convention
        if not self.CHANNEL_PATTERN.match(message.channel):
            return self._suggest_rename(message)

        # Rule 4: Process the coding request in public
        return self._process_request(message)

    def _refuse_dm(self, message: Message) -> AgentResponse:
        self._log("REFUSED_DM", message)
        return AgentResponse(
            text=(
                f"Hey {message.user}! I only work in public channels so "
                f"everyone can learn from our conversation.\n\n"
                f"Create a channel like `#{message.user.lower()}_agent` "
                f"and invite me there. Your teammates will thank you!"
            ),
            refused=True,
        )

    def _refuse_private(self, message: Message) -> AgentResponse:
        self._log("REFUSED_PRIVATE", message)
        return AgentResponse(
            text=(
                f"This is a private channel. I need to work in public so the "
                f"whole team benefits from our session.\n\n"
                f"Move this to a public channel like `#{message.user.lower()}_agent`."
            ),
            refused=True,
        )

    def _suggest_rename(self, message: Message) -> AgentResponse:
        self._log("SUGGEST_RENAME", message)
        return AgentResponse(
            text=(
                f"I'll help here, but consider renaming this channel to "
                f"`#{message.user.lower()}_agent` so it's easy for others "
                f"to find and follow your coding sessions."
            ),
        )

    def _process_request(self, message: Message) -> AgentResponse:
        """Simulate processing a coding request in a public channel."""
        self._log("PROCESSED", message)

        # Simple pattern matching for demo coding tasks
        text_lower = message.text.lower()

        if "write a function" in text_lower or "create a function" in text_lower:
            return self._generate_function(message)
        elif "review" in text_lower:
            return self._review_code(message)
        elif "explain" in text_lower:
            return self._explain_code(message)
        elif "refactor" in text_lower:
            return self._refactor_code(message)
        else:
            return self._general_response(message)

    def _generate_function(self, message: Message) -> AgentResponse:
        thread = message.thread_id or message.timestamp
        return AgentResponse(
            text=f"Here's a function based on your request, {message.user}. "
                 f"Anyone watching: feel free to suggest improvements!",
            code=(
                "def process_data(items: list[dict]) -> dict:\n"
                '    """Process and aggregate items by category."""\n'
                "    result = {}\n"
                "    for item in items:\n"
                '        cat = item.get("category", "unknown")\n'
                "        result.setdefault(cat, []).append(item)\n"
                "    return result"
            ),
            thread_id=thread,
        )

    def _review_code(self, message: Message) -> AgentResponse:
        thread = message.thread_id or message.timestamp
        return AgentResponse(
            text=f"Code review in progress. Posting findings publicly "
                 f"so the team can discuss.",
            code=(
                "# Review findings:\n"
                "# 1. Missing input validation on line 12\n"
                "# 2. Consider using a dataclass instead of raw dict\n"
                "# 3. Add type hints for better IDE support\n"
                "# 4. The nested loop on line 25 could be O(n^2) - "
                "consider a set lookup"
            ),
            thread_id=thread,
        )

    def _explain_code(self, message: Message) -> AgentResponse:
        thread = message.thread_id or message.timestamp
        return AgentResponse(
            text=f"Great question, {message.user}! Explaining publicly "
                 f"so others can benefit too.",
            thread_id=thread,
        )

    def _refactor_code(self, message: Message) -> AgentResponse:
        thread = message.thread_id or message.timestamp
        return AgentResponse(
            text=f"Refactoring suggestion ready. Team: check this thread "
                 f"if you maintain similar code.",
            code=(
                "# Before: imperative style\n"
                "# results = []\n"
                "# for item in data:\n"
                "#     if item.is_valid():\n"
                "#         results.append(item.transform())\n\n"
                "# After: functional style\n"
                "results = [item.transform() for item in data if item.is_valid()]"
            ),
            thread_id=thread,
        )

    def _general_response(self, message: Message) -> AgentResponse:
        thread = message.thread_id or message.timestamp
        return AgentResponse(
            text=f"Working on it, {message.user}. Everything here is visible "
                 f"to the team -- jump in if you have context to add!",
            thread_id=thread,
        )

    def _log(self, action: str, message: Message):
        entry = {
            "action": action,
            "user": message.user,
            "channel": message.channel,
            "channel_type": message.channel_type.value,
            "timestamp": message.timestamp,
            "text_preview": message.text[:80],
        }
        self.history.append(entry)

    def get_searchable_history(self) -> list[dict]:
        """Return all interactions for indexing / search."""
        return self.history

    def search_history(self, query: str) -> list[dict]:
        """Search through past interactions."""
        query_lower = query.lower()
        return [
            entry for entry in self.history
            if query_lower in entry.get("text_preview", "").lower()
            or query_lower in entry.get("user", "").lower()
            or query_lower in entry.get("channel", "").lower()
        ]


class ChannelWorkspace:
    """Manages the public-channel workspace and its agents."""

    def __init__(self):
        self.agent = PublicChannelAgent()
        self.channels: dict[str, list[Message]] = {}
        self.thread_replies: dict[str, list[dict]] = {}

    def create_channel(self, name: str) -> str:
        """Create a public channel."""
        if name not in self.channels:
            self.channels[name] = []
        return name

    def send_message(
        self,
        user: str,
        text: str,
        channel: str,
        channel_type: ChannelType = ChannelType.PUBLIC,
        thread_id: Optional[str] = None,
    ) -> AgentResponse:
        """Send a message to the agent and get a response."""
        msg = Message(
            user=user,
            text=text,
            channel=channel,
            channel_type=channel_type,
            thread_id=thread_id,
        )

        if channel_type == ChannelType.PUBLIC:
            self.channels.setdefault(channel, []).append(msg)

        response = self.agent.handle_message(msg)

        if response.thread_id:
            self.thread_replies.setdefault(response.thread_id, []).append({
                "agent": self.agent.name,
                "text": response.text,
                "code": response.code,
            })

        return response

    def add_reaction(self, channel: str, msg_index: int, user: str, emoji: str):
        """Any team member can react to a thread."""
        if channel in self.channels and msg_index < len(self.channels[channel]):
            self.channels[channel][msg_index].reactions.append(
                {"user": user, "emoji": emoji}
            )

    def add_thread_reply(self, thread_id: str, user: str, text: str):
        """Any team member can add context to a thread."""
        self.thread_replies.setdefault(thread_id, []).append({
            "user": user,
            "text": text,
        })

    def get_channel_log(self, channel: str) -> list[dict]:
        """Export channel log for searchability."""
        if channel not in self.channels:
            return []
        return [
            {
                "user": m.user,
                "text": m.text,
                "timestamp": m.timestamp,
                "reactions": m.reactions,
                "thread_id": m.thread_id,
            }
            for m in self.channels[channel]
        ]
