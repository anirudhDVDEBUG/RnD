#!/usr/bin/env python3
"""ZeroClaw Subagent Orchestration — end-to-end demo.

Demonstrates:
  1. Task decomposition into subtasks
  2. Routing subtasks to specialized agents (research, code, review)
  3. Parallel execution of independent agents
  4. Merging results into a unified report
"""

import json
import sys

from zeroclaw.orchestrator import Orchestrator


DIVIDER = "=" * 70


def print_header(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def run_demo(task: str, strategy: str = "parallel_then_merge") -> None:
    print_header(f"ZEROCLAW ORCHESTRATION  [{strategy.upper()}]")
    print(f"\n  Task: {task}\n")

    orch = Orchestrator(strategy=strategy)

    # Step 1: Decompose
    subtasks = orch.decompose(task)
    print("  [1] TASK DECOMPOSITION")
    for i, st in enumerate(subtasks, 1):
        print(f"      Subtask {i}: {st['agent']:>10} -> {st['task']}")

    # Step 2+3: Route & Execute
    print(f"\n  [2] DISPATCHING ({strategy})")
    result = orch.run(task)

    # Step 4: Display results
    print(f"\n  [3] AGENT RESULTS")
    for d in result.details:
        status_icon = "OK" if d["status"] == "success" else "!!"
        print(f"      [{status_icon}] {d['agent']:>10} ({d['type']})  {d['elapsed_ms']:.0f}ms")
        if isinstance(d["output"], dict):
            for k, v in d["output"].items():
                if isinstance(v, list):
                    print(f"           {k}:")
                    for item in v[:3]:
                        if isinstance(item, dict):
                            print(f"             - {item}")
                        else:
                            print(f"             - {item}")
                elif isinstance(v, dict):
                    print(f"           {k}:")
                    for sk, sv in v.items():
                        print(f"             {sk}: {sv}")
                else:
                    print(f"           {k}: {v}")

    # Step 5: Merged summary
    print_header("MERGED RESULT")
    print(f"  Status:     {result.overall_status}")
    print(f"  Agents:     {result.agent_count}")
    print(f"  Total time: {result.total_elapsed_ms:.0f}ms")
    print(f"  Summary:    {result.summary}")
    if result.conflicts:
        print(f"  Conflicts:")
        for c in result.conflicts:
            print(f"    - {c}")
    else:
        print(f"  Conflicts:  None")
    print()


def main() -> None:
    print_header("ZEROCLAW SUBAGENT ORCHESTRATION DEMO")
    print("  Pattern: Decompose -> Route -> Execute -> Merge")
    print("  Source:  github.com/muhammadqasimkalhoro94-blip/claude-zeroclaw-agentics")

    # Demo 1: Parallel strategy (default)
    run_demo(
        task="Add user authentication with OAuth2 to the API server",
        strategy="parallel_then_merge",
    )

    # Demo 2: Sequential strategy (chained context)
    run_demo(
        task="Refactor the payment module to support Stripe and PayPal",
        strategy="sequential",
    )

    # Demo 3: Custom agents
    print_header("CUSTOM AGENT REGISTRATION")
    from zeroclaw.agents import AgentSpec
    security_agent = AgentSpec(
        name="security",
        role="Scan for vulnerabilities and enforce security policies",
        agent_type="review",
        tools=["Bash", "Grep"],
    )
    orch = Orchestrator(agents=[security_agent])
    orch.config.register(security_agent)
    result = security_agent.execute("Audit authentication module for OWASP top-10")
    print(f"  Security agent result: {json.dumps(result.output, indent=4)}")

    print_header("DEMO COMPLETE")
    print("  All orchestration pipelines ran successfully.")
    print("  See HOW_TO_USE.md for integration with Claude Code skills.")
    print()


if __name__ == "__main__":
    main()
