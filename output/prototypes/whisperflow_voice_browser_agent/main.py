"""WhisperFlow: voice-first autonomous browser agent.

Runs an interactive loop:
  1. Capture voice command (Whisper STT or mock)
  2. Route to expert persona
  3. Take screenshot + page context
  4. Plan actions with GPT-4o Vision (or mock planner)
  5. Execute actions via Playwright (or mock browser)
  6. Record results in adaptive memory for self-healing
"""

import asyncio
import os
import sys

from voice_input import VoiceInput
from browser_agent import BrowserAgent
from vision_analyzer import VisionAnalyzer
from memory_store import MemoryStore
from expert_personas import route_to_expert

MOCK_MODE = os.environ.get("WHISPERFLOW_MOCK", "1") == "1"
MAX_COMMANDS = int(os.environ.get("WHISPERFLOW_MAX_COMMANDS", "5"))


def get_openai_client():
    if MOCK_MODE:
        return None
    from openai import OpenAI
    return OpenAI()


async def run_agent():
    print("=" * 60)
    print("  WhisperFlow — Voice-First Browser Agent")
    print("=" * 60)
    if MOCK_MODE:
        print("  Mode: MOCK (no API keys / hardware required)")
    else:
        print("  Mode: LIVE (using OpenAI API + Playwright + mic)")
    print()

    client = get_openai_client()
    voice = VoiceInput(client=client)
    browser = BrowserAgent()
    vision = VisionAnalyzer(client=client)
    memory = MemoryStore(path="memory.json")

    await browser.start(headless=True)

    # Start on a default page
    await browser.navigate("https://news.ycombinator.com")

    command_count = 0
    while command_count < MAX_COMMANDS:
        command_count += 1
        print(f"\n--- Command {command_count}/{MAX_COMMANDS} ---")

        # 1. Get voice command
        command = voice.record_until_silence()
        if command.lower() in ("quit", "exit", "stop"):
            print("Exiting...")
            break

        # 2. Route to expert
        expert = route_to_expert(command)

        # 3. Capture current state
        screenshot_b64 = await browser.screenshot_base64()
        page_context = await browser.get_page_context()
        print(f"[state] Page: {browser._mock_title if MOCK_MODE else 'live'} | "
              f"URL: {browser._mock_url if MOCK_MODE else 'live'}")

        # 4. Plan actions
        actions = vision.plan_actions(command, page_context, screenshot_b64)
        print(f"[plan] {len(actions)} action(s) planned")

        # 5. Execute actions with self-healing
        for i, action in enumerate(actions):
            print(f"  [{i+1}/{len(actions)}] {action.get('action')} ", end="")
            success = await browser.execute_action(action)
            selector = action.get("selector", "")
            url = browser._mock_url if MOCK_MODE else "unknown"

            if success:
                print("-> OK")
                if selector:
                    memory.record_success(url, selector)
            else:
                print("-> FAILED")
                if selector:
                    memory.record_failure(url, selector)
                    alt = memory.suggest_alternative(url, selector)
                    if alt:
                        print(f"  [self-heal] Trying alternative selector: {alt}")
                        retry_action = {**action, "selector": alt}
                        retry_ok = await browser.execute_action(retry_action)
                        if retry_ok:
                            memory.record_success(url, alt)
                            print("  [self-heal] Alternative succeeded!")

    # Summary
    stats = memory.stats()
    print("\n" + "=" * 60)
    print("  Session Summary")
    print("=" * 60)
    print(f"  Commands processed: {command_count}")
    print(f"  Memory entries:     {stats['entries']}")
    print(f"  Successful actions: {stats['successes']}")
    print(f"  Failed actions:     {stats['failures']}")
    print("=" * 60)

    await browser.close()


def main():
    asyncio.run(run_agent())


if __name__ == "__main__":
    main()
