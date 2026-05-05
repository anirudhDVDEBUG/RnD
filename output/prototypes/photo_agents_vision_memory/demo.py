#!/usr/bin/env python3
"""Demo: Photo-agents vision-grounded layered memory and self-written skills."""

import shutil
import os

from photo_agents import Agent, MemoryLayer, VisionGrounding, SkillRegistry


def clean_demo_dirs():
    """Remove previous demo artifacts."""
    for d in ["./memory", "./skills"]:
        if os.path.exists(d):
            shutil.rmtree(d)


def main():
    print("=" * 60)
    print("  Photo-agents Demo: Vision-Grounded Layered Memory")
    print("  Self-Evolving Agents with Self-Written Skills")
    print("=" * 60)

    clean_demo_dirs()

    # --- 1. Set up layered memory ---
    print("\n[1] Initializing layered memory system...")
    memory = MemoryLayer(
        working_memory_size=10,
        episodic_store="./memory/episodes",
        semantic_store="./memory/knowledge",
    )

    # --- 2. Enable vision grounding ---
    print("[2] Enabling vision grounding (screenshot-based memory anchors)...")
    vision = VisionGrounding(
        capture_dir="./memory/vision",
        capture_interval="on_action",
        embedding_model="clip",
    )

    # --- 3. Create the self-evolving agent ---
    print("[3] Creating autonomous agent with self-skill extraction...\n")
    agent = Agent(
        memory=memory,
        vision=vision,
        skill_dir="./skills",
        auto_skill_extraction=True,
        name="PhotoAgent-1",
    )

    # --- 4. Run agent on a task ---
    print("-" * 60)
    print("  TASK 1: Navigate and extract data")
    print("-" * 60)
    result1 = agent.run(task="Open browser, navigate to example.com, extract page title", steps=4)

    # --- 5. Demonstrate skill learning ---
    print("-" * 60)
    print("  SKILL LEARNING: Repeat actions to trigger auto-extraction")
    print("-" * 60)

    # Manually register a skill to show the system
    registry = SkillRegistry(skill_dir="./skills")
    registry.register_skill(
        name="navigate_to_url",
        description="Open browser and navigate to a specified URL",
        action_sequence=["Open browser", "Type URL in address bar", "Press Enter", "Wait for page load"],
    )

    # Simulate repeated action patterns to trigger auto-extraction
    registry.record_action_sequence(["Click button", "Fill form", "Submit"], success=True)
    registry.record_action_sequence(["Click button", "Fill form", "Submit"], success=True)  # triggers extraction

    print(f"\n  Available skills after learning: {registry.list_skills()}")
    print()

    # Execute a learned skill
    print("  Executing skill 'navigate_to_url':")
    output = registry.execute_skill("navigate_to_url")
    print(output)
    print()

    # --- 6. Demonstrate memory recall ---
    print("-" * 60)
    print("  MEMORY RECALL: Episodic retrieval")
    print("-" * 60)
    recalled = memory.episodic.recall("navigate")
    print(f"\n  Episodes matching 'navigate': {len(recalled)}")
    for i, ep in enumerate(recalled):
        print(f"    Episode {i+1}: actions={ep['actions']}, outcome={ep['outcome']}")

    # Semantic memory
    print(f"\n  Semantic facts stored: {memory.semantic.count}")
    task_memory = memory.semantic.retrieve("current_task")
    print(f"  Last task remembered: {task_memory}")

    # --- 7. Vision capture summary ---
    print(f"\n  Vision captures taken: {vision.capture_count}")
    print(f"  Capture directory: {vision.capture_dir}")

    # --- 8. Final summary ---
    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)
    print(f"  Working memory items:  {len(memory.working)}")
    print(f"  Episodic episodes:     {memory.episodic.count}")
    print(f"  Semantic facts:        {memory.semantic.count}")
    print(f"  Vision captures:       {vision.capture_count}")
    print(f"  Skills learned:        {registry.list_skills()}")
    print(f"  Auto-extracted skills: {[s for s in registry.list_skills() if 'auto' in s]}")
    print("=" * 60)


if __name__ == "__main__":
    main()
