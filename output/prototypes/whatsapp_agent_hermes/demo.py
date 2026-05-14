#!/usr/bin/env python3
"""
WhatsApp Agent for Hermes - Interactive Demo

Runs through all major capabilities with mock data so you can evaluate
the agent without needing a live WhatsApp session or API keys.
"""

import json
import time
import datetime
from whatsapp_agent import HermesWhatsAppAgent

SEPARATOR = "=" * 60


def section(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def main():
    print("""
 ╔═══════════════════════════════════════════════════════╗
 ║   WhatsApp Agent for Hermes  -  Demo Run             ║
 ║   Autonomous WhatsApp manager via Andorina           ║
 ╚═══════════════════════════════════════════════════════╝
    """)

    agent = HermesWhatsAppAgent()

    # --- 1. Initialize ---
    section("1. Authentication (simulated QR scan)")
    agent.initialize()
    print(f"\n  Status: {json.dumps(agent.status(), indent=2)}")

    # --- 2. Contact Search ---
    section("2. Contact Search")

    for query in ["vip", "alice", "work"]:
        results = agent.search_contacts(query)
        for c in results:
            print(f"    {c['name']:20s}  {c['phone']:15s}  {c.get('email',''):25s}  labels={c['labels']}")
        print()

    # --- 3. Send Text Messages ---
    section("3. Send Text Messages")
    agent.send_message("+1-555-0101", "Hi Alice, the Q3 report is ready for review.")
    agent.send_message("+1-555-0102", "Bob, can we reschedule our 3pm to 4pm?")

    # --- 4. Send Voice Notes ---
    section("4. Send Voice Notes (TTS)")
    agent.send_voice(
        "+1-555-0105",
        "Hey Eva, just a quick voice note to confirm our dinner reservation at 7pm tonight."
    )

    # --- 5. Send Files ---
    section("5. Send Files from PC")
    # Create a sample file to send
    sample_file = "/tmp/whatsapp_demo_report.txt"
    with open(sample_file, "w") as f:
        f.write("Q3 Revenue Report\n" + "-" * 30 + "\nTotal: $1.2M | Growth: +15%\n")

    agent.send_file("+1-555-0101", sample_file, "Here's the Q3 report")

    # --- 6. Schedule Messages ---
    section("6. Schedule Messages for Future Delivery")

    agent.schedule_message(
        "+1-555-0103",
        "Good morning Carol! Don't forget our standup at 9am.",
        delay_seconds=1,
        msg_type="text",
    )
    agent.schedule_message(
        "+1-555-0108",
        "Hiro, the signed contract is attached.",
        delay_seconds=1,
        msg_type="voice",
    )
    agent.schedule_message(
        "+1-555-0104",
        "Weekly metrics report",
        delay_seconds=2,
        msg_type="file",
        attachment_path=sample_file,
    )

    print(f"\n  Scheduler status: {json.dumps(agent.scheduler.summary(), indent=2)}")

    print("\n  Waiting for scheduled messages to become due...")
    time.sleep(2.5)

    results = agent.process_scheduled()
    print(f"\n  Processed {len(results)} scheduled message(s)")

    # --- 7. Final Status ---
    section("7. Final Agent Status")
    status = agent.status()
    print(json.dumps(status, indent=2))

    # --- 8. Full Send Log ---
    section("8. Complete Message Log")
    for i, entry in enumerate(agent.session.get_sent_log(), 1):
        print(f"  [{i}] {entry['type']:6s} -> {entry['to']:15s}  @ {entry['timestamp']}")

    print(f"\n{SEPARATOR}")
    print("  Demo complete. All features exercised with mock data.")
    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    main()
