#!/usr/bin/env python3
"""
Demo: Public-Channel Coding Agent Workflow
===========================================
Simulates a team using a Shopify River-style coding agent
that works exclusively in public Slack channels.
"""

from channel_agent import PublicChannelAgent, ChannelWorkspace, ChannelType
import json

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
RESET = "\033[0m"
RULE = f"{DIM}{'─' * 60}{RESET}"


def fmt_response(resp, indent="  "):
    """Format an agent response for terminal display."""
    lines = []
    if resp.refused:
        lines.append(f"{indent}{RED}REFUSED{RESET}: {resp.text}")
    else:
        lines.append(f"{indent}{GREEN}AGENT{RESET}: {resp.text}")
    if resp.code:
        lines.append(f"{indent}{DIM}```python{RESET}")
        for code_line in resp.code.split("\n"):
            lines.append(f"{indent}{CYAN}{code_line}{RESET}")
        lines.append(f"{indent}{DIM}```{RESET}")
    if resp.thread_id:
        lines.append(f"{indent}{DIM}[threaded: {resp.thread_id[:20]}...]{RESET}")
    return "\n".join(lines)


def main():
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  Public-Channel Coding Agent Workflow Demo{RESET}")
    print(f"{BOLD}  Inspired by Shopify's River / Lehrwerkstatt pattern{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    ws = ChannelWorkspace()

    # --- Scenario 1: DM Refused ---
    print(f"{BOLD}Scenario 1: Developer tries to DM the agent{RESET}")
    print(RULE)
    resp = ws.send_message(
        user="alice",
        text="Hey, can you help me write a sorting function?",
        channel="@alice",
        channel_type=ChannelType.DM,
    )
    print(f"  {BLUE}alice (DM){RESET}: Hey, can you help me write a sorting function?")
    print(fmt_response(resp))
    print()

    # --- Scenario 2: Private channel refused ---
    print(f"{BOLD}Scenario 2: Request from a private channel{RESET}")
    print(RULE)
    resp = ws.send_message(
        user="bob",
        text="Review my authentication module",
        channel="#secret-project",
        channel_type=ChannelType.PRIVATE,
    )
    print(f"  {BLUE}bob (#secret-project, private){RESET}: Review my auth module")
    print(fmt_response(resp))
    print()

    # --- Scenario 3: Public channel, non-standard name ---
    print(f"{BOLD}Scenario 3: Public channel with non-standard name{RESET}")
    print(RULE)
    ws.create_channel("#general")
    resp = ws.send_message(
        user="carol",
        text="Can you explain how decorators work?",
        channel="#general",
        channel_type=ChannelType.PUBLIC,
    )
    print(f"  {BLUE}carol (#general){RESET}: Can you explain how decorators work?")
    print(fmt_response(resp))
    print()

    # --- Scenario 4: Proper public channel, coding request ---
    print(f"{BOLD}Scenario 4: Correct usage -- #alice_agent public channel{RESET}")
    print(RULE)
    ws.create_channel("#alice_agent")
    resp = ws.send_message(
        user="alice",
        text="Write a function to aggregate sales data by region",
        channel="#alice_agent",
        channel_type=ChannelType.PUBLIC,
    )
    print(f"  {BLUE}alice (#alice_agent){RESET}: Write a function to aggregate sales data")
    print(fmt_response(resp))
    print()

    # --- Scenario 5: Team collaboration in thread ---
    print(f"{BOLD}Scenario 5: Team collaboration -- others jump in{RESET}")
    print(RULE)
    thread = resp.thread_id
    ws.add_reaction("#alice_agent", 0, "dave", "eyes")
    ws.add_thread_reply(thread, "dave",
        "Nice! Consider using defaultdict for cleaner aggregation.")
    ws.add_thread_reply(thread, "eve",
        "We have a similar utility in utils/aggregators.py -- maybe reuse that?")
    print(f"  {YELLOW}dave{RESET} reacted with :eyes:")
    print(f"  {YELLOW}dave{RESET} (thread): Nice! Consider using defaultdict.")
    print(f"  {YELLOW}eve{RESET} (thread): We have a similar utility in utils/aggregators.py")
    print()

    # --- Scenario 6: Code review in public ---
    print(f"{BOLD}Scenario 6: Public code review{RESET}")
    print(RULE)
    ws.create_channel("#bob_agent")
    resp = ws.send_message(
        user="bob",
        text="Review the payment processing module for security issues",
        channel="#bob_agent",
        channel_type=ChannelType.PUBLIC,
    )
    print(f"  {BLUE}bob (#bob_agent){RESET}: Review the payment processing module")
    print(fmt_response(resp))
    print()

    # --- Scenario 7: Refactoring suggestion ---
    print(f"{BOLD}Scenario 7: Refactoring in public{RESET}")
    print(RULE)
    resp = ws.send_message(
        user="carol",
        text="Refactor the data pipeline to use list comprehensions",
        channel="#alice_agent",
        channel_type=ChannelType.PUBLIC,
    )
    print(f"  {BLUE}carol (#alice_agent){RESET}: Refactor the data pipeline")
    print(fmt_response(resp))
    print()

    # --- Summary: Searchable History ---
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  Searchable Interaction History{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    history = ws.agent.get_searchable_history()
    for i, entry in enumerate(history, 1):
        status = f"{RED}REFUSED{RESET}" if "REFUSED" in entry["action"] else f"{GREEN}OK{RESET}"
        print(f"  {i}. [{status}] {entry['action']:20s} "
              f"user={entry['user']:8s} channel={entry['channel']:20s} "
              f"{DIM}{entry['text_preview'][:40]}{RESET}")

    print(f"\n{RULE}")
    print(f"  Total interactions: {len(history)}")
    print(f"  Refused (DM/private): {sum(1 for h in history if 'REFUSED' in h['action'])}")
    print(f"  Processed in public: {sum(1 for h in history if h['action'] == 'PROCESSED')}")
    print(f"  Channels active: {list(ws.channels.keys())}")
    print(f"{RULE}")

    # --- Search demo ---
    print(f"\n{BOLD}  Search Demo: query='review'{RESET}")
    print(RULE)
    results = ws.agent.search_history("review")
    for r in results:
        print(f"  Found: {r['user']} in {r['channel']} -- {r['text_preview']}")

    # --- Export channel log ---
    print(f"\n{BOLD}  Channel Log Export: #alice_agent{RESET}")
    print(RULE)
    log = ws.get_channel_log("#alice_agent")
    print(f"  {json.dumps(log, indent=2, default=str)[:600]}")

    print(f"\n{BOLD}  Design Principles (from Shopify's River){RESET}")
    print(RULE)
    principles = [
        ("Transparency", "All agent work happens in public channels"),
        ("No DMs", "Agent refuses private conversations"),
        ("Searchable", "Every interaction is indexed and findable"),
        ("Open participation", "Anyone can join, react, add context"),
        ("Named channels", "#person_agent pattern for discoverability"),
        ("Osmosis learning", "No curriculum needed -- learning by proximity"),
    ]
    for name, desc in principles:
        print(f"  {GREEN}{name:22s}{RESET} {desc}")

    print(f"\n{BOLD}Done. All interactions logged and searchable.{RESET}\n")


if __name__ == "__main__":
    main()
