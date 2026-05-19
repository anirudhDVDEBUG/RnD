"""
Agent Design Patterns — 7x6 Framework
======================================
A queryable catalogue of 28 agent design patterns organized across
7 architectural layers and 6 design concerns. Based on the companion repo
to "Designing AI Agents" (Manning) by Jia Huang.

Usage:
    from agent_patterns import PatternFramework
    fw = PatternFramework()
    fw.recommend("I need a research agent that decomposes tasks and uses tools")
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

# ---------------------------------------------------------------------------
# Core data model
# ---------------------------------------------------------------------------

LAYERS = [
    "Single Agent",
    "Multi-Agent",
    "Planning",
    "Tool Use",
    "Memory",
    "Guardrails",
    "Harness",
]

CONCERNS = [
    "Decomposition",
    "Orchestration",
    "Context Engineering",
    "Evaluation",
    "Error Recovery",
    "Human-in-the-Loop",
]


@dataclass
class Pattern:
    """One cell in the 7x6 grid that has a named pattern."""
    name: str
    layer: str
    concern: str
    summary: str
    when_to_use: str
    example_frameworks: List[str] = field(default_factory=list)
    composable_with: List[str] = field(default_factory=list)

    @property
    def coordinate(self) -> str:
        row = LAYERS.index(self.layer) + 1
        col = CONCERNS.index(self.concern) + 1
        return f"({row},{col})"

    def short(self) -> str:
        return f"[{self.coordinate}] {self.name} ({self.layer} / {self.concern})"


# ---------------------------------------------------------------------------
# Pattern catalogue — 28 verified patterns
# ---------------------------------------------------------------------------

def _build_catalogue() -> List[Pattern]:
    """Return the 28-pattern catalogue."""
    patterns = [
        # --- Layer 1: Single Agent ---
        Pattern(
            name="Task Decomposition Agent",
            layer="Single Agent", concern="Decomposition",
            summary="Breaks a complex goal into ordered sub-tasks a single agent can execute sequentially.",
            when_to_use="When one agent must handle a multi-step workflow end-to-end.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["ReAct Loop", "Tool Router"],
        ),
        Pattern(
            name="ReAct Loop",
            layer="Single Agent", concern="Orchestration",
            summary="Reason-Act-Observe cycle: the agent thinks, acts, observes the result, then repeats.",
            when_to_use="General-purpose single-agent problem solving with tool access.",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["Task Decomposition Agent", "Scratchpad Memory"],
        ),
        Pattern(
            name="Prompt Chaining",
            layer="Single Agent", concern="Context Engineering",
            summary="Splits a prompt into stages, feeding the output of one stage as context to the next.",
            when_to_use="When a single prompt is too complex or exceeds context limits.",
            example_frameworks=["Aider", "DeerFlow"],
            composable_with=["Sliding Window Memory", "Self-Eval Gate"],
        ),
        Pattern(
            name="Self-Eval Gate",
            layer="Single Agent", concern="Evaluation",
            summary="Agent evaluates its own output against criteria before returning it.",
            when_to_use="High-stakes outputs where quality must be verified before delivery.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["Prompt Chaining", "Retry with Reflection"],
        ),
        Pattern(
            name="Retry with Reflection",
            layer="Single Agent", concern="Error Recovery",
            summary="On failure, the agent reflects on what went wrong and retries with an improved approach.",
            when_to_use="Tasks where first-attempt failures are common (code generation, API calls).",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["Self-Eval Gate", "ReAct Loop"],
        ),
        Pattern(
            name="Approval Checkpoint",
            layer="Single Agent", concern="Human-in-the-Loop",
            summary="Agent pauses at critical decision points and asks the human for approval.",
            when_to_use="When actions are irreversible or high-risk (deployments, payments, deletions).",
            example_frameworks=["Claude Code"],
            composable_with=["Task Decomposition Agent", "Guardrail Validator"],
        ),

        # --- Layer 2: Multi-Agent ---
        Pattern(
            name="Divide and Conquer",
            layer="Multi-Agent", concern="Decomposition",
            summary="A coordinator splits work across specialist agents, each handling a sub-problem.",
            when_to_use="When sub-tasks require different expertise or can run in parallel.",
            example_frameworks=["DeerFlow", "OpenHands"],
            composable_with=["Supervisor Orchestrator", "Result Aggregator"],
        ),
        Pattern(
            name="Supervisor Orchestrator",
            layer="Multi-Agent", concern="Orchestration",
            summary="A supervisor agent routes tasks to workers, monitors progress, and merges results.",
            when_to_use="Complex workflows needing centralized coordination.",
            example_frameworks=["DeerFlow", "Claude Code"],
            composable_with=["Divide and Conquer", "Consensus Evaluator"],
        ),
        Pattern(
            name="Shared Blackboard",
            layer="Multi-Agent", concern="Context Engineering",
            summary="Agents read/write to a shared data store (blackboard) for coordination.",
            when_to_use="When agents need asynchronous communication without direct messaging.",
            example_frameworks=["OpenHands"],
            composable_with=["Supervisor Orchestrator", "Conflict Resolver"],
        ),
        Pattern(
            name="Consensus Evaluator",
            layer="Multi-Agent", concern="Evaluation",
            summary="Multiple agents vote or debate to converge on the best answer.",
            when_to_use="High-uncertainty tasks where diverse perspectives reduce error.",
            example_frameworks=["DeerFlow"],
            composable_with=["Divide and Conquer", "Escalation Handler"],
        ),

        # --- Layer 3: Planning ---
        Pattern(
            name="Hierarchical Task Network",
            layer="Planning", concern="Decomposition",
            summary="Recursively decomposes goals into sub-goals until reaching primitive actions.",
            when_to_use="Deep multi-level planning with dependent sub-tasks.",
            example_frameworks=["DeerFlow"],
            composable_with=["Plan-Execute-Replan", "Tool Router"],
        ),
        Pattern(
            name="Plan-Execute-Replan",
            layer="Planning", concern="Orchestration",
            summary="Creates a plan, executes steps, then replans when observations invalidate the plan.",
            when_to_use="Dynamic environments where initial plans become stale.",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["Hierarchical Task Network", "Retry with Reflection"],
        ),
        Pattern(
            name="Goal-Context Alignment",
            layer="Planning", concern="Context Engineering",
            summary="Continuously aligns the agent's working context with the current sub-goal.",
            when_to_use="Long-running plans where context drift is a risk.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["Plan-Execute-Replan", "Sliding Window Memory"],
        ),
        # --- Layer 4: Tool Use ---
        Pattern(
            name="Tool Router",
            layer="Tool Use", concern="Decomposition",
            summary="Routes sub-tasks to the appropriate tool based on task type.",
            when_to_use="Agents with access to many tools that need intelligent selection.",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["ReAct Loop", "Tool Error Wrapper"],
        ),
        Pattern(
            name="Tool Chaining Pipeline",
            layer="Tool Use", concern="Orchestration",
            summary="Chains tool calls in sequence, passing output of one tool as input to the next.",
            when_to_use="Data transformation pipelines (fetch → parse → transform → store).",
            example_frameworks=["Aider", "Claude Code"],
            composable_with=["Tool Router", "Tool Error Wrapper"],
        ),
        Pattern(
            name="Tool Result Injection",
            layer="Tool Use", concern="Context Engineering",
            summary="Injects tool results directly into the agent's context for reasoning.",
            when_to_use="When tool outputs need to be reasoned over, not just passed through.",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["Prompt Chaining", "Sliding Window Memory"],
        ),
        Pattern(
            name="Tool Error Wrapper",
            layer="Tool Use", concern="Error Recovery",
            summary="Wraps tool calls with error handling: catch, diagnose, retry or fallback.",
            when_to_use="Unreliable external APIs or tools that may timeout/fail.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["Retry with Reflection", "Tool Router"],
        ),

        # --- Layer 5: Memory ---
        Pattern(
            name="Scratchpad Memory",
            layer="Memory", concern="Context Engineering",
            summary="A working-memory buffer the agent uses to track intermediate results.",
            when_to_use="Multi-step reasoning where intermediate state must be preserved.",
            example_frameworks=["Claude Code", "OpenHands"],
            composable_with=["ReAct Loop", "Sliding Window Memory"],
        ),
        Pattern(
            name="Sliding Window Memory",
            layer="Memory", concern="Decomposition",
            summary="Maintains a fixed-size window of recent context, evicting oldest items.",
            when_to_use="Long conversations or sessions that exceed context window limits.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["Scratchpad Memory", "RAG Retriever"],
        ),
        Pattern(
            name="RAG Retriever",
            layer="Memory", concern="Orchestration",
            summary="Retrieves relevant documents from a vector store to augment the prompt.",
            when_to_use="When the agent needs access to a large knowledge base beyond context limits.",
            example_frameworks=["DeerFlow", "OpenHands"],
            composable_with=["Sliding Window Memory", "Goal-Context Alignment"],
        ),
        Pattern(
            name="Memory Consolidation",
            layer="Memory", concern="Evaluation",
            summary="Periodically summarizes and compresses memory to retain key information.",
            when_to_use="Very long sessions where raw history is too large to keep.",
            example_frameworks=["Claude Code"],
            composable_with=["Scratchpad Memory", "Sliding Window Memory"],
        ),

        # --- Layer 6: Guardrails ---
        Pattern(
            name="Input Validator",
            layer="Guardrails", concern="Decomposition",
            summary="Validates and sanitizes inputs before the agent processes them.",
            when_to_use="User-facing agents that receive untrusted input.",
            example_frameworks=["Claude Code"],
            composable_with=["Output Validator", "Guardrail Validator"],
        ),
        Pattern(
            name="Output Validator",
            layer="Guardrails", concern="Evaluation",
            summary="Checks agent outputs against safety rules, format specs, or business logic.",
            when_to_use="Production agents where output quality/safety must be guaranteed.",
            example_frameworks=["Claude Code", "Aider"],
            composable_with=["Input Validator", "Self-Eval Gate"],
        ),
        Pattern(
            name="Guardrail Validator",
            layer="Guardrails", concern="Orchestration",
            summary="A middleware layer that enforces constraints between agent steps.",
            when_to_use="Multi-step agents that must stay within policy at every step.",
            example_frameworks=["Claude Code"],
            composable_with=["Output Validator", "Approval Checkpoint"],
        ),
        Pattern(
            name="Escalation Handler",
            layer="Guardrails", concern="Human-in-the-Loop",
            summary="Detects when the agent is outside its competence and escalates to a human.",
            when_to_use="Customer-facing systems where wrong answers have real consequences.",
            example_frameworks=["Claude Code", "DeerFlow"],
            composable_with=["Approval Checkpoint", "Consensus Evaluator"],
        ),

        # --- Layer 7: Harness ---
        Pattern(
            name="Harness Orchestrator",
            layer="Harness", concern="Orchestration",
            summary="The outer harness (Claude Code, Aider, etc.) that manages agent lifecycle.",
            when_to_use="Production deployment of agents that need session management and tool registration.",
            example_frameworks=["Claude Code", "Aider", "OpenHands", "DeerFlow"],
            composable_with=["Supervisor Orchestrator", "Conflict Resolver"],
        ),
        Pattern(
            name="Conflict Resolver",
            layer="Harness", concern="Error Recovery",
            summary="Detects and resolves conflicts when multiple agents edit shared resources.",
            when_to_use="Multi-agent coding systems with concurrent file edits.",
            example_frameworks=["Aider", "OpenHands"],
            composable_with=["Shared Blackboard", "Harness Orchestrator"],
        ),
        Pattern(
            name="Result Aggregator",
            layer="Harness", concern="Context Engineering",
            summary="Collects, deduplicates, and merges results from parallel agent runs.",
            when_to_use="Fan-out/fan-in architectures where parallel results must be synthesized.",
            example_frameworks=["DeerFlow"],
            composable_with=["Divide and Conquer", "Supervisor Orchestrator"],
        ),
    ]
    return patterns


# ---------------------------------------------------------------------------
# Framework API
# ---------------------------------------------------------------------------

class PatternFramework:
    """Queryable 7x6 agent design pattern framework."""

    def __init__(self):
        self.patterns: List[Pattern] = _build_catalogue()
        self._by_name: Dict[str, Pattern] = {p.name: p for p in self.patterns}

    # -- Queries --

    def by_layer(self, layer: str) -> List[Pattern]:
        return [p for p in self.patterns if p.layer.lower() == layer.lower()]

    def by_concern(self, concern: str) -> List[Pattern]:
        return [p for p in self.patterns if p.concern.lower() == concern.lower()]

    def by_coordinate(self, row: int, col: int) -> Optional[Pattern]:
        layer = LAYERS[row - 1] if 1 <= row <= 7 else None
        concern = CONCERNS[col - 1] if 1 <= col <= 6 else None
        if not layer or not concern:
            return None
        matches = [p for p in self.patterns if p.layer == layer and p.concern == concern]
        return matches[0] if matches else None

    def get(self, name: str) -> Optional[Pattern]:
        return self._by_name.get(name)

    def search(self, query: str) -> List[Pattern]:
        q = query.lower()
        scored: List[Tuple[int, Pattern]] = []
        for p in self.patterns:
            score = 0
            for word in q.split():
                if word in p.name.lower():
                    score += 3
                if word in p.summary.lower():
                    score += 2
                if word in p.when_to_use.lower():
                    score += 1
                if word in p.layer.lower():
                    score += 1
                if word in p.concern.lower():
                    score += 1
            if score > 0:
                scored.append((score, p))
        scored.sort(key=lambda x: -x[0])
        return [p for _, p in scored]

    def recommend(self, use_case: str, top_n: int = 5) -> List[Pattern]:
        """Recommend top-N patterns for a described use case."""
        return self.search(use_case)[:top_n]

    # -- Display --

    def grid(self) -> str:
        """Render the 7x6 grid as a text table."""
        col_w = 26
        header = "Layer / Concern".ljust(18) + "".join(c[:col_w-1].ljust(col_w) for c in CONCERNS)
        lines = [header, "-" * len(header)]
        for layer in LAYERS:
            row_patterns = {p.concern: p for p in self.patterns if p.layer == layer}
            cells = []
            for concern in CONCERNS:
                p = row_patterns.get(concern)
                cells.append((p.name[:col_w-2] if p else "-").ljust(col_w))
            lines.append(layer.ljust(18) + "".join(cells))
        return "\n".join(lines)

    def detail(self, pattern: Pattern) -> str:
        lines = [
            f"Pattern: {pattern.name}  {pattern.coordinate}",
            f"Layer:   {pattern.layer}",
            f"Concern: {pattern.concern}",
            f"",
            f"Summary:",
            f"  {pattern.summary}",
            f"",
            f"When to use:",
            f"  {pattern.when_to_use}",
            f"",
            f"Frameworks: {', '.join(pattern.example_frameworks)}",
            f"Composes with: {', '.join(pattern.composable_with)}",
        ]
        return "\n".join(lines)

    def architecture_for(self, archetype: str) -> Dict:
        """Return a named architecture preset."""
        presets = {
            "autonomous_agent": {
                "name": "Autonomous Agent",
                "description": "Single agent that plans, acts, and self-corrects.",
                "patterns": [
                    "Task Decomposition Agent", "ReAct Loop", "Tool Router",
                    "Scratchpad Memory", "Retry with Reflection", "Self-Eval Gate",
                ],
            },
            "agent_swarm": {
                "name": "Agent Swarm",
                "description": "Multiple specialist agents coordinated by a supervisor.",
                "patterns": [
                    "Divide and Conquer", "Supervisor Orchestrator",
                    "Shared Blackboard", "Guardrail Validator",
                    "Harness Orchestrator", "Conflict Resolver",
                ],
            },
            "research_agent": {
                "name": "Research Agent",
                "description": "Deep-research agent with planning, retrieval, and human oversight.",
                "patterns": [
                    "Hierarchical Task Network", "Plan-Execute-Replan",
                    "RAG Retriever", "Goal-Context Alignment",
                    "Tool Result Injection", "Approval Checkpoint",
                ],
            },
            "production_pipeline": {
                "name": "Production Pipeline",
                "description": "Hardened pipeline with guardrails, evaluation, and error recovery.",
                "patterns": [
                    "Harness Orchestrator", "Input Validator", "Output Validator",
                    "Tool Error Wrapper", "Escalation Handler", "Memory Consolidation",
                ],
            },
        }
        key = archetype.lower().replace(" ", "_").replace("-", "_")
        preset = presets.get(key)
        if not preset:
            return {"error": f"Unknown archetype. Choose from: {', '.join(presets.keys())}"}
        preset["pattern_details"] = [self._by_name[n] for n in preset["patterns"] if n in self._by_name]
        return preset
