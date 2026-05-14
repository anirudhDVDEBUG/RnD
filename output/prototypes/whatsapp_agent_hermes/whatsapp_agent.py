"""
WhatsApp Agent for Hermes - Core agent module.

Demonstrates the architecture of a WhatsApp automation agent that can:
- Schedule messages for future delivery
- Send voice notes (TTS-generated)
- Share files from the local filesystem
- Search contacts via Google Contacts API

This demo uses mock/simulated WhatsApp interactions so it runs
without credentials or a live browser session.
"""

import json
import datetime
import os
import threading
import time
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Contact:
    name: str
    phone: str
    email: Optional[str] = None
    labels: list = field(default_factory=list)


@dataclass
class ScheduledMessage:
    recipient: str
    body: str
    send_at: datetime.datetime
    status: str = "pending"  # pending | sent | failed
    msg_type: str = "text"  # text | voice | file
    attachment_path: Optional[str] = None

    def is_due(self) -> bool:
        return datetime.datetime.now() >= self.send_at and self.status == "pending"


class ContactBook:
    """Simulated Google Contacts integration."""

    def __init__(self):
        self._contacts = [
            Contact("Alice Johnson", "+1-555-0101", "alice@example.com", ["work"]),
            Contact("Bob Martinez", "+1-555-0102", "bob@example.com", ["work", "vip"]),
            Contact("Carol Chen", "+1-555-0103", "carol@example.com", ["personal"]),
            Contact("David Kim", "+1-555-0104", "david@example.com", ["work"]),
            Contact("Eva Rossi", "+1-555-0105", "eva@example.com", ["personal", "vip"]),
            Contact("Frank Okafor", "+1-555-0106", "frank@example.com", ["work"]),
            Contact("Grace Patel", "+1-555-0107", "grace@example.com", ["personal"]),
            Contact("Hiro Tanaka", "+1-555-0108", "hiro@example.com", ["work", "vip"]),
        ]

    def search(self, query: str) -> list[Contact]:
        q = query.lower()
        return [
            c for c in self._contacts
            if q in c.name.lower() or q in c.phone or q in (c.email or "").lower()
            or any(q in lbl for lbl in c.labels)
        ]

    def list_all(self) -> list[Contact]:
        return list(self._contacts)


class WhatsAppSession:
    """
    Simulated WhatsApp Web session.

    In the real Andorina agent, this wraps Selenium/Playwright to:
    1. Authenticate via QR code scan
    2. Navigate the WhatsApp Web DOM
    3. Send messages, voice notes, and files
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.authenticated = False
        self._sent_log: list[dict] = []

    def authenticate(self) -> bool:
        """Simulate QR code authentication."""
        print("  [WhatsApp] Initializing browser session (headless={})...".format(self.headless))
        print("  [WhatsApp] QR code scanned (simulated). Authenticated.")
        self.authenticated = True
        return True

    def send_text(self, phone: str, message: str) -> dict:
        entry = {
            "type": "text",
            "to": phone,
            "body": message,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "delivered",
        }
        self._sent_log.append(entry)
        print(f"  [WhatsApp] Text sent to {phone}: {message[:60]}...")
        return entry

    def send_voice_note(self, phone: str, audio_path: str) -> dict:
        entry = {
            "type": "voice",
            "to": phone,
            "audio_path": audio_path,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "delivered",
        }
        self._sent_log.append(entry)
        print(f"  [WhatsApp] Voice note sent to {phone}: {audio_path}")
        return entry

    def send_file(self, phone: str, file_path: str, caption: str = "") -> dict:
        entry = {
            "type": "file",
            "to": phone,
            "file_path": file_path,
            "caption": caption,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "delivered",
        }
        self._sent_log.append(entry)
        print(f"  [WhatsApp] File sent to {phone}: {file_path}")
        return entry

    def get_sent_log(self) -> list[dict]:
        return list(self._sent_log)


class VoiceNoteGenerator:
    """Simulated TTS engine for generating voice note audio files."""

    def __init__(self, output_dir: str = "/tmp/whatsapp_voice_notes"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate(self, text: str, filename: str = "note.ogg") -> str:
        path = os.path.join(self.output_dir, filename)
        # In production, this calls a TTS engine (gTTS, pyttsx3, etc.)
        with open(path, "w") as f:
            f.write(f"[SIMULATED AUDIO] {text}")
        print(f"  [TTS] Generated voice note: {path} ({len(text)} chars)")
        return path


class MessageScheduler:
    """Queue and dispatch scheduled messages."""

    def __init__(self, session: WhatsAppSession, tts: VoiceNoteGenerator):
        self.session = session
        self.tts = tts
        self._queue: list[ScheduledMessage] = []

    def schedule(self, msg: ScheduledMessage) -> None:
        self._queue.append(msg)
        print(f"  [Scheduler] Queued {msg.msg_type} to {msg.recipient} at {msg.send_at}")

    def process_due(self) -> list[dict]:
        results = []
        for msg in self._queue:
            if msg.is_due():
                try:
                    if msg.msg_type == "text":
                        result = self.session.send_text(msg.recipient, msg.body)
                    elif msg.msg_type == "voice":
                        audio = self.tts.generate(msg.body)
                        result = self.session.send_voice_note(msg.recipient, audio)
                    elif msg.msg_type == "file" and msg.attachment_path:
                        result = self.session.send_file(
                            msg.recipient, msg.attachment_path, msg.body
                        )
                    else:
                        result = {"error": f"Unknown type: {msg.msg_type}"}
                    msg.status = "sent"
                    results.append(result)
                except Exception as e:
                    msg.status = "failed"
                    results.append({"error": str(e)})
        return results

    def pending_count(self) -> int:
        return sum(1 for m in self._queue if m.status == "pending")

    def summary(self) -> dict:
        return {
            "total": len(self._queue),
            "pending": sum(1 for m in self._queue if m.status == "pending"),
            "sent": sum(1 for m in self._queue if m.status == "sent"),
            "failed": sum(1 for m in self._queue if m.status == "failed"),
        }


class HermesWhatsAppAgent:
    """
    Top-level agent that Hermes invokes as a skill.

    Exposes tool-like methods that map to Hermes agent actions:
    - search_contacts(query)
    - send_message(recipient, body)
    - send_voice(recipient, text)
    - send_file(recipient, path, caption)
    - schedule_message(recipient, body, delay_seconds)
    - status()
    """

    def __init__(self):
        self.session = WhatsAppSession(headless=True)
        self.tts = VoiceNoteGenerator()
        self.contacts = ContactBook()
        self.scheduler = MessageScheduler(self.session, self.tts)

    def initialize(self) -> bool:
        print("\n[Agent] Initializing WhatsApp Agent for Hermes...")
        return self.session.authenticate()

    def search_contacts(self, query: str) -> list[dict]:
        results = self.contacts.search(query)
        print(f"\n[Agent] Contact search '{query}' -> {len(results)} results")
        return [asdict(c) for c in results]

    def send_message(self, recipient: str, body: str) -> dict:
        print(f"\n[Agent] Sending text to {recipient}")
        return self.session.send_text(recipient, body)

    def send_voice(self, recipient: str, text: str) -> dict:
        print(f"\n[Agent] Generating and sending voice note to {recipient}")
        audio = self.tts.generate(text)
        return self.session.send_voice_note(recipient, audio)

    def send_file(self, recipient: str, path: str, caption: str = "") -> dict:
        print(f"\n[Agent] Sending file '{path}' to {recipient}")
        return self.session.send_file(recipient, path, caption)

    def schedule_message(
        self, recipient: str, body: str, delay_seconds: int = 10,
        msg_type: str = "text", attachment_path: Optional[str] = None,
    ) -> dict:
        send_at = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
        msg = ScheduledMessage(
            recipient=recipient,
            body=body,
            send_at=send_at,
            msg_type=msg_type,
            attachment_path=attachment_path,
        )
        self.scheduler.schedule(msg)
        return {"scheduled": True, "send_at": send_at.isoformat()}

    def process_scheduled(self) -> list[dict]:
        return self.scheduler.process_due()

    def status(self) -> dict:
        return {
            "authenticated": self.session.authenticated,
            "scheduler": self.scheduler.summary(),
            "messages_sent": len(self.session.get_sent_log()),
        }
