"""Route tasks to agents based on pattern matching and priority."""

import re

from .models import AgentProfile, RoutingRule


class Router:
    def __init__(self, rules: list[RoutingRule], profiles: dict[str, AgentProfile], fallback: str = "claude"):
        self.rules = rules
        self.profiles = profiles
        self.fallback = fallback

    def route(self, task: str) -> tuple[str, str, float]:
        """Route a task to an agent. Returns (agent_name, reason, confidence)."""
        task_lower = task.lower()
        best_match = None
        best_weight = -1

        for rule in self.rules:
            patterns = rule.pattern.split("|")
            matched = [p for p in patterns if re.search(p, task_lower)]
            if matched:
                weight = rule.priority_weight * len(matched)
                if weight > best_weight:
                    best_weight = weight
                    best_match = rule

        if best_match:
            confidence = min(best_weight / 6.0, 1.0)
            matched_patterns = [p for p in best_match.pattern.split("|") if re.search(p, task_lower)]
            reason = f"Matched patterns: {', '.join(matched_patterns)} (priority: {best_match.priority})"
            return best_match.route_to, reason, confidence

        # Fallback: check profiles for strength-based matching
        best_agent = self.fallback
        best_score = 0.0
        for name, profile in self.profiles.items():
            score = profile.match_score(task)
            if score > best_score:
                best_score = score
                best_agent = name

        if best_score > 0:
            return best_agent, f"Profile strength match (score: {best_score:.1f})", min(best_score / 5.0, 0.8)

        return self.fallback, "Fallback (no pattern or profile match)", 0.3
