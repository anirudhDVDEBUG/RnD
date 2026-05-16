"""Multi-armed bandit router with Thompson Sampling, UCB1, and epsilon-greedy."""
from __future__ import annotations
import math, random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class ArmStats:
    """Running stats for one (task_type, agent) arm."""
    successes: float = 1.0   # Beta prior alpha
    failures: float = 1.0    # Beta prior beta
    pulls: int = 0
    total_reward: float = 0.0

    @property
    def mean_reward(self) -> float:
        return self.total_reward / max(self.pulls, 1)

class BanditRouter:
    """Routes tasks to agents using a bandit strategy."""

    def __init__(
        self,
        agents: List[str],
        strategy: str = "thompson_sampling",
        exploration_rate: float = 0.1,
        decay: float = 0.95,
    ):
        self.agents = agents
        self.strategy = strategy
        self.exploration_rate = exploration_rate
        self.decay = decay
        # arms[task_type][agent_name] = ArmStats
        self.arms: Dict[str, Dict[str, ArmStats]] = {}

    def _ensure_arms(self, task_type: str) -> Dict[str, ArmStats]:
        if task_type not in self.arms:
            self.arms[task_type] = {a: ArmStats() for a in self.agents}
        return self.arms[task_type]

    def select(self, task_type: str) -> Tuple[str, Dict[str, float]]:
        """Pick an agent for *task_type*. Returns (agent, scores_dict)."""
        arms = self._ensure_arms(task_type)
        scores: Dict[str, float] = {}

        if self.strategy == "thompson_sampling":
            for agent, st in arms.items():
                scores[agent] = random.betavariate(st.successes, st.failures)
        elif self.strategy == "ucb1":
            total_pulls = sum(s.pulls for s in arms.values()) or 1
            for agent, st in arms.items():
                if st.pulls == 0:
                    scores[agent] = float("inf")
                else:
                    scores[agent] = st.mean_reward + math.sqrt(
                        2 * math.log(total_pulls) / st.pulls
                    )
        elif self.strategy == "epsilon_greedy":
            if random.random() < self.exploration_rate:
                chosen = random.choice(self.agents)
                scores = {a: (1.0 if a == chosen else 0.0) for a in self.agents}
            else:
                for agent, st in arms.items():
                    scores[agent] = st.mean_reward
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        best = max(scores, key=lambda a: scores[a])
        return best, scores

    def update(self, task_type: str, agent: str, reward: float) -> None:
        """Record outcome and update arm stats."""
        arms = self._ensure_arms(task_type)
        st = arms[agent]
        st.pulls += 1
        st.total_reward += reward
        # Update Beta params for Thompson Sampling
        st.successes += reward
        st.failures += (1.0 - reward)
        # Apply decay to other arms so recent data weighs more
        for other, ost in arms.items():
            if other != agent:
                ost.successes *= self.decay
                ost.failures *= self.decay

    def summary(self) -> str:
        lines = []
        for task_type, arms in sorted(self.arms.items()):
            lines.append(f"\n  Task: {task_type}")
            for agent, st in sorted(arms.items(), key=lambda x: -x[1].mean_reward):
                lines.append(
                    f"    {agent:12s}  pulls={st.pulls:3d}  "
                    f"mean_reward={st.mean_reward:.3f}  "
                    f"alpha={st.successes:.1f} beta={st.failures:.1f}"
                )
        return "\n".join(lines)
