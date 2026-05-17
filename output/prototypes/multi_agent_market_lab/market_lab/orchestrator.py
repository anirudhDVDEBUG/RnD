"""Orchestrator coordinates multiple research agents and manages allocation."""
from dataclasses import dataclass, field
from .agent import ResearchAgent, MarketSignal
from .experiment import Experiment, ExperimentTracker, ExperimentStatus


@dataclass
class AllocationResult:
    """Result of a rebalancing operation."""
    agent_name: str
    old_budget: float
    new_budget: float
    reason: str


class Orchestrator:
    """Coordinates independent research agents operating in parallel."""

    def __init__(self, config: dict):
        self.config = config
        self.agents: dict[str, ResearchAgent] = {}
        self.tracker = ExperimentTracker()
        self.allocation_history: list[list[AllocationResult]] = []
        self._setup_agents(config.get("agents", []))

    def _setup_agents(self, agent_configs: list):
        for cfg in agent_configs:
            agent = ResearchAgent(
                name=cfg["name"],
                segment=cfg["segment"],
                budget=cfg.get("budget", 0.25),
                capabilities=cfg.get("capabilities", ["web_search", "news_scan"]),
            )
            self.agents[agent.name] = agent

    def run_iteration(self) -> dict:
        """Run one research iteration across all active agents."""
        results = {}
        for name, agent in self.agents.items():
            signals = agent.research()
            results[name] = {
                "signals_found": len(signals),
                "signals": signals,
                "performance": agent.performance_score,
                "iterations": agent.iterations,
            }
        return results

    def run_experiment(self, experiment: Experiment, iterations: int = None) -> Experiment:
        """Execute a full experiment run."""
        iters = iterations or experiment.iteration_limit
        experiment.start()

        for i in range(iters):
            iter_results = self.run_iteration()
            total_signals = sum(r["signals_found"] for r in iter_results.values())
            avg_confidence = 0.0
            all_signals = []
            for r in iter_results.values():
                all_signals.extend(r["signals"])
            if all_signals:
                avg_confidence = sum(s.confidence for s in all_signals) / len(all_signals)

            experiment.record_iteration({
                "signals_found": total_signals,
                "avg_confidence": round(avg_confidence, 3),
                "agent_performance": {n: r["performance"] for n, r in iter_results.items()},
            })

        experiment.complete({"final_iteration": iters})
        return experiment

    def rebalance(self) -> list[AllocationResult]:
        """Dynamically rebalance allocation based on agent performance."""
        if not self.agents:
            return []

        scores = {name: agent.performance_score for name, agent in self.agents.items()}
        total_score = sum(scores.values())
        results = []

        if total_score == 0:
            equal_share = 1.0 / len(self.agents)
            for name, agent in self.agents.items():
                old = agent.budget
                agent.budget = round(equal_share, 3)
                results.append(AllocationResult(name, old, agent.budget, "equal distribution (no data)"))
        else:
            for name, agent in self.agents.items():
                old = agent.budget
                new_budget = round(scores[name] / total_score, 3)
                # Apply caps from config
                cap = self.config.get("allocation_cap", 0.6)
                floor = self.config.get("allocation_floor", 0.05)
                new_budget = max(floor, min(cap, new_budget))
                agent.budget = new_budget
                reason = "score-based" if new_budget != cap and new_budget != floor else "capped"
                results.append(AllocationResult(name, old, new_budget, reason))

        self.allocation_history.append(results)
        return results

    def status(self) -> dict:
        """Get current orchestrator status."""
        return {
            "agents": {
                name: {
                    "segment": a.segment,
                    "budget": a.budget,
                    "signals": len(a.signals),
                    "iterations": a.iterations,
                    "performance": a.performance_score,
                }
                for name, a in self.agents.items()
            },
            "experiments": self.tracker.summary(),
            "total_signals": sum(len(a.signals) for a in self.agents.values()),
        }
