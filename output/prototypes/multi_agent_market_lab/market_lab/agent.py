"""Research agent that autonomously gathers market intelligence."""
import random
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MarketSignal:
    """A market signal discovered by an agent."""
    source: str
    segment: str
    signal_type: str  # "opportunity", "threat", "trend", "anomaly"
    confidence: float
    summary: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class ResearchAgent:
    """An autonomous research agent focused on a specific market segment."""
    name: str
    segment: str
    budget: float  # allocation budget (0.0 - 1.0)
    capabilities: list = field(default_factory=list)
    signals: list = field(default_factory=list)
    iterations: int = 0
    _active: bool = True

    def research(self, mock_sources: Optional[list] = None) -> list[MarketSignal]:
        """Run one research iteration, returning discovered signals."""
        if not self._active:
            return []

        self.iterations += 1
        sources = mock_sources or self._default_sources()
        discovered = []

        for source in sources:
            if random.random() < 0.6 * self.budget:
                signal = MarketSignal(
                    source=source,
                    segment=self.segment,
                    signal_type=random.choice(["opportunity", "threat", "trend", "anomaly"]),
                    confidence=round(random.uniform(0.3, 0.95), 2),
                    summary=self._generate_summary(source),
                )
                discovered.append(signal)

        self.signals.extend(discovered)
        return discovered

    def pause(self):
        self._active = False

    def resume(self):
        self._active = True

    @property
    def performance_score(self) -> float:
        """Score based on signal count and average confidence."""
        if not self.signals:
            return 0.0
        avg_conf = sum(s.confidence for s in self.signals) / len(self.signals)
        return round(len(self.signals) * avg_conf / max(self.iterations, 1), 3)

    def _default_sources(self) -> list:
        return [
            f"{self.segment}_news_feed",
            f"{self.segment}_social_mentions",
            f"{self.segment}_patent_filings",
            f"{self.segment}_earnings_reports",
        ]

    def _generate_summary(self, source: str) -> str:
        templates = [
            f"Emerging competitor activity detected in {self.segment} via {source}",
            f"New market entry signal from {source} — {self.segment} segment expanding",
            f"Price sensitivity shift observed in {self.segment} ({source})",
            f"Technology disruption indicator from {source} affecting {self.segment}",
            f"Consumer sentiment change in {self.segment} tracked via {source}",
        ]
        return random.choice(templates)
