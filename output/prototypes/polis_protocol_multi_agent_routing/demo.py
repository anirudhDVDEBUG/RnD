#!/usr/bin/env python3
"""Polis Protocol demo: simulate multi-agent routing with Thompson Sampling."""
from __future__ import annotations
import os, random, sys

# Ensure repo root is on path
sys.path.insert(0, os.path.dirname(__file__))

from polis.cards import load_cards
from polis.bandit import BanditRouter
from polis.ledger import Ledger, LessonEntry

POLIS_DIR = os.path.join(os.path.dirname(__file__), ".polis")
LESSONS_PATH = os.path.join(POLIS_DIR, "lessons", "ledger.json")

# ---------------------------------------------------------------------------
# Ground-truth reward matrix (simulated — no API keys needed)
# Higher = agent is better at this task type
# ---------------------------------------------------------------------------
TRUE_REWARDS = {
    "code_generation":  {"claude": 0.92, "gpt": 0.78, "gemini": 0.65, "codex": 0.85},
    "web_research":     {"claude": 0.55, "gpt": 0.72, "gemini": 0.90, "codex": 0.30},
    "data_analysis":    {"claude": 0.88, "gpt": 0.70, "gemini": 0.75, "codex": 0.50},
    "creative_writing": {"claude": 0.75, "gpt": 0.90, "gemini": 0.68, "codex": 0.25},
    "code_review":      {"claude": 0.95, "gpt": 0.80, "gemini": 0.60, "codex": 0.70},
    "summarization":    {"claude": 0.82, "gpt": 0.78, "gemini": 0.88, "codex": 0.40},
}

TASK_DESCRIPTIONS = {
    "code_generation": "Implement new authentication middleware",
    "web_research": "Research competitor pricing strategies",
    "data_analysis": "Analyze Q2 sales funnel conversion rates",
    "creative_writing": "Write product launch blog post",
    "code_review": "Review PR #247: database migration refactor",
    "summarization": "Summarize 50-page technical spec document",
}

SAMPLE_LESSONS = {
    "code_generation": "Provide full file context for best results.",
    "web_research": "Include specific date ranges to narrow search scope.",
    "data_analysis": "Supply raw CSV directly; avoid pre-summarized data.",
    "creative_writing": "Give brand voice examples for consistent tone.",
    "code_review": "Include the diff plus surrounding 50 lines of context.",
    "summarization": "Specify desired output length upfront.",
}

def sim_reward(task_type: str, agent: str) -> float:
    """Simulate a noisy reward draw."""
    base = TRUE_REWARDS.get(task_type, {}).get(agent, 0.5)
    noisy = base + random.gauss(0, 0.08)
    return max(0.0, min(1.0, noisy))


def main():
    random.seed(42)

    # 1. Load capability cards
    agents_dir = os.path.join(POLIS_DIR, "agents")
    cards = load_cards(agents_dir)
    print("=" * 65)
    print("  POLIS PROTOCOL — Multi-Agent Routing Demo")
    print("=" * 65)
    print(f"\nLoaded {len(cards)} agent capability cards:")
    for name, card in cards.items():
        print(f"  {name:10s} | vendor={card.vendor:10s} | ctx={card.max_context:>9,} | cost={card.cost_tier}")
    print()

    # 2. Initialize router and ledger
    agent_names = list(cards.keys())
    router = BanditRouter(agent_names, strategy="thompson_sampling", decay=0.95)
    ledger = Ledger(LESSONS_PATH)

    # Warm-start from any existing lessons
    n_warm = ledger.replay_into(router)
    if n_warm:
        print(f"Warm-started router from {n_warm} historical lessons.\n")

    # 3. Simulate 60 task routing rounds
    NUM_ROUNDS = 60
    task_types = list(TRUE_REWARDS.keys())
    correct_picks = 0
    total_reward = 0.0

    print("-" * 65)
    print(f"{'Round':>5}  {'Task Type':<20} {'Selected':>10} {'Best':>10} {'Reward':>8} {'Match':>6}")
    print("-" * 65)

    for i in range(1, NUM_ROUNDS + 1):
        task_type = random.choice(task_types)
        agent, scores = router.select(task_type)
        reward = sim_reward(task_type, agent)
        router.update(task_type, agent, reward)

        best_agent = max(TRUE_REWARDS[task_type], key=lambda a: TRUE_REWARDS[task_type][a])
        is_correct = agent == best_agent
        if is_correct:
            correct_picks += 1
        total_reward += reward

        # Log every 5th round or last round
        if i % 5 == 0 or i == NUM_ROUNDS:
            print(f"{i:5d}  {task_type:<20} {agent:>10} {best_agent:>10} {reward:8.3f} {'  YES' if is_correct else '   no'}")

        # Record lesson
        outcome = "success" if reward >= 0.7 else ("partial" if reward >= 0.4 else "failure")
        entry = LessonEntry(
            date=f"2026-05-{16 + i // 10:02d}",
            task_type=task_type,
            agent=agent,
            task_description=TASK_DESCRIPTIONS.get(task_type, task_type),
            outcome=outcome,
            reward=round(reward, 3),
            lesson=SAMPLE_LESSONS.get(task_type, "No specific lesson."),
        )
        ledger.append(entry)

    # 4. Summary
    print("-" * 65)
    accuracy = correct_picks / NUM_ROUNDS * 100
    avg_reward = total_reward / NUM_ROUNDS
    print(f"\nResults over {NUM_ROUNDS} rounds:")
    print(f"  Optimal agent selected: {correct_picks}/{NUM_ROUNDS} ({accuracy:.1f}%)")
    print(f"  Average reward:         {avg_reward:.3f}")
    print(f"  Lessons recorded:       {len(ledger.entries)}")

    # 5. Show learned routing preferences
    print("\nLearned routing table (bandit arm stats):")
    print(router.summary())

    # 6. Show what a single routing decision looks like
    print("\n" + "=" * 65)
    print("  Example: Route a new 'code_generation' task")
    print("=" * 65)
    agent, scores = router.select("code_generation")
    print(f"  Thompson Sampling scores: { {a: round(s, 3) for a, s in scores.items()} }")
    print(f"  Selected agent: {agent}")
    card = cards[agent]
    print(f"  Agent details:  vendor={card.vendor}, max_context={card.max_context:,}, cost={card.cost_tier}")
    print(f"  Strengths:      {', '.join(card.strengths)}")
    print()

    # 7. Save ledger as markdown too
    md_path = os.path.join(POLIS_DIR, "lessons", "ledger.md")
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w") as f:
        f.write(ledger.to_markdown())
    print(f"Lessons ledger saved to: {md_path}")
    print(f"Lessons JSON saved to:   {LESSONS_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()
