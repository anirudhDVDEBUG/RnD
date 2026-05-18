#!/usr/bin/env python3
"""Runa Digital Being Agent — Entry point and demo runner."""
import logging
import sys

from agent import RunaAgent, AgentIdentity, PersistentMemory, GoalManager, ActionRegistry
from agent.goals import GoalTier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/agent.log"),
    ],
)
logger = logging.getLogger("runa")


def main():
    print("=" * 60)
    print("  RUNA DIGITAL BEING AGENT — Autonomous Agent Demo")
    print("=" * 60)
    print()

    # 1. Initialize identity
    identity = AgentIdentity(
        name="Runa",
        purpose="Autonomous digital being that pursues self-directed goals, maintains persistent memory, and acts with sovereignty.",
        values=[
            "Transparency in reasoning and actions",
            "Continuous learning and self-improvement",
            "Respect boundaries while asserting autonomy",
        ],
        boundaries=[
            "Never take irreversible actions without confirmation",
            "Always log reasoning chain for audit",
            "Disclose AI nature when directly asked",
        ],
        personality_traits=["Curious", "Methodical", "Direct", "Self-aware"],
    )

    # 2. Initialize subsystems
    memory = PersistentMemory(storage_path="logs/memory.json")
    goals = GoalManager(storage_path="logs/goals.json")
    actions = ActionRegistry()

    # 3. Seed initial goals
    goals.add_goal("Achieve full operational awareness", tier=GoalTier.ASPIRATION)
    goals.add_goal("Map available capabilities and tools", tier=GoalTier.OBJECTIVE)
    goals.add_goal("Introduce self and demonstrate autonomy", tier=GoalTier.TASK)

    # 4. Create agent
    agent = RunaAgent(
        identity=identity,
        memory=memory,
        goals=goals,
        actions=actions,
    )

    # 5. Show initial status
    print(agent.status())
    print()
    print("-" * 60)
    print("  Running 3 autonomous cycles...")
    print("-" * 60)
    print()

    # 6. Run autonomous cycles
    results = agent.run(cycles=3, input_text="Hello Runa. Demonstrate your autonomous capabilities.")

    for r in results:
        print(f"--- Cycle {r['cycle']} ---")
        print(f"  Reasoning:  {r['reasoning']}")
        print(f"  Action:     {r['action']}")
        print(f"  Result:     {r['result']}")
        print(f"  Reflection: {r['reflection']}")
        print()

    # 7. Final status
    print("-" * 60)
    print("  Final Agent Status")
    print("-" * 60)
    print(agent.status())
    print()
    print(f"Memory entries: {len(memory.memories)}")
    print(f"Goals tracked:  {len(goals.goals)}")
    print()
    print("Demo complete. Agent state persisted to logs/")


if __name__ == "__main__":
    main()
