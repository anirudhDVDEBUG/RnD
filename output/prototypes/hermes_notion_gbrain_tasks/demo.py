#!/usr/bin/env python3
"""
Demo: Hermes Notion GBrain Task Manager
Simulates the full pipeline with mock data — no API keys needed.
"""

import json
from hermes_agent import HermesAgent

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

DEMO_MESSAGES = [
    ("whatsapp", "Add a task to review the Q3 report by Friday"),
    ("slack", "Remind me to deploy the new API to staging in 3 days #dev"),
    ("whatsapp", "Schedule a meeting with the design team tomorrow #design"),
    ("slack", "Todo: update the onboarding docs by Wednesday"),
    ("whatsapp", "I need to fix the login bug urgently #dev"),
    ("slack", "Show my tasks"),
    ("whatsapp", "Complete task review the Q3 report"),
    ("slack", "List tasks"),
]


def print_header():
    print(f"\n{BOLD}{'='*70}")
    print(f"  HERMES NOTION GBRAIN — Task Management Demo")
    print(f"  Natural Language → NLP Parse → GBrain Enrich → Notion")
    print(f"{'='*70}{RESET}\n")


def print_message(source: str, message: str, index: int):
    icon = "📱" if source == "whatsapp" else "💬"
    label = "WhatsApp" if source == "whatsapp" else "Slack"
    print(f"{BOLD}[{index}] {icon} {label}:{RESET} \"{message}\"")


def print_parse_result(result: dict):
    print(f"  {DIM}├─ Intent: {result['task']['intent']} (confidence: {result['task']['confidence']:.0%}){RESET}")
    if "task" in result and "title" in result["task"]:
        print(f"  {DIM}├─ Title: {result['task']['title']}{RESET}")
        print(f"  {DIM}├─ Priority: {result['task']['priority']}{RESET}")
        if result["task"].get("due_date"):
            print(f"  {DIM}├─ Due: {result['task']['due_date']}{RESET}")
        if result["task"].get("tags"):
            print(f"  {DIM}├─ Tags: {', '.join(result['task']['tags'])}{RESET}")


def print_enrichment(result: dict):
    if "task" in result and "gbrain_enrichment" in result.get("task", {}):
        gb = result["task"]["gbrain_enrichment"]
        score = gb.get("enrichment_score", 0)
        color = GREEN if score > 0.5 else YELLOW
        print(f"  {color}├─ GBrain Score: {score:.0%}{RESET}")
        if gb.get("knowledge_context") and score > 0.5:
            ctx = gb["knowledge_context"][:80]
            print(f"  {color}├─ Context: {ctx}...{RESET}" if len(gb["knowledge_context"]) > 80 else f"  {color}├─ Context: {ctx}{RESET}")
        if gb.get("related_documents"):
            print(f"  {color}├─ Docs: {', '.join(gb['related_documents'])}{RESET}")


def print_result(result: dict):
    action = result.get("action", "unknown")
    if action == "created":
        print(f"  {GREEN}└─ ✓ {result['reply']}{RESET}")
        print(f"  {DIM}   Notion Page ID: {result['notion_page_id']}{RESET}")
    elif action == "listed":
        print(f"  {CYAN}└─ {result['reply']}{RESET}")
    elif action == "completed":
        print(f"  {MAGENTA}└─ ✓ {result['reply']}{RESET}")
    else:
        print(f"  {YELLOW}└─ {result['reply']}{RESET}")


def main():
    print_header()
    agent = HermesAgent()

    for i, (source, message) in enumerate(DEMO_MESSAGES, 1):
        print_message(source, message, i)
        result = agent.process_message(message, source=source)

        if result.get("action") == "created":
            print_parse_result(result)
            print_enrichment(result)
        print_result(result)
        print()

    # Final summary
    print(f"{BOLD}{'─'*70}")
    print(f"  SUMMARY")
    print(f"{'─'*70}{RESET}")
    tasks = agent.notion.list_tasks()
    print(f"  Total tasks in Notion: {len(tasks)}")
    for task in tasks:
        print(agent.notion.format_task_summary(task))
    print()

    # Show raw JSON for one task
    print(f"{BOLD}{'─'*70}")
    print(f"  SAMPLE NOTION PAGE (JSON)")
    print(f"{'─'*70}{RESET}")
    if tasks:
        print(json.dumps(tasks[0], indent=2, default=str))
    print()


if __name__ == "__main__":
    main()
