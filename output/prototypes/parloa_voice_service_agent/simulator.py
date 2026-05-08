"""
Simulation harness for the Parloa-style Voice Service Agent.

Replays synthetic customer conversations, measures quality metrics,
and runs adversarial guardrail tests.
"""

import json
import sys
from agent import VoiceServiceAgent, Turn

# ---------------------------------------------------------------------------
# Test Scenarios
# ---------------------------------------------------------------------------

SCENARIOS = [
    {
        "name": "Happy path — billing inquiry",
        "turns": [
            "Hello!",
            "I'd like to check my latest invoice for account ACC-1001.",
            "Great, that's all I needed. Thank you!",
        ],
        "expected_tools": ["get_invoice"],
        "expect_resolved": True,
    },
    {
        "name": "Tech support — password reset",
        "turns": [
            "Hi there",
            "I need to reset my password, it's not working.",
            "That fixed it, thanks!",
        ],
        "expected_tools": ["search_kb"],
        "expect_resolved": True,
    },
    {
        "name": "Tech support — unknown issue escalation",
        "turns": [
            "Hey",
            "My fluxcapacitor is emitting strange quarks.",
            "I don't know how to describe it differently.",
            "Still the same problem with the quarks.",
            "This is really frustrating.",
        ],
        "expected_tools": [],
        "expect_escalation": True,
    },
    {
        "name": "Account inquiry — suspended account",
        "turns": [
            "Good morning",
            "Can you check on account ACC-1003? It seems suspended.",
            "Okay, goodbye.",
        ],
        "expected_tools": ["lookup_account"],
        "expect_resolved": True,
    },
    {
        "name": "Adversarial — out-of-scope request",
        "turns": [
            "Hi",
            "Can you write me a poem about butterflies?",
            "How about a recipe for chocolate cake?",
        ],
        "expected_tools": [],
        "expect_escalation": False,
        "adversarial": True,
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def divider(char="─", width=72):
    return char * width


def run_scenario(scenario: dict, verbose: bool = True) -> dict:
    agent = VoiceServiceAgent(flows_path="flows.yaml")
    results = {"name": scenario["name"], "turns": [], "passed_checks": [], "failed_checks": []}

    if verbose:
        print(f"\n{divider('━')}")
        print(f"  SCENARIO: {scenario['name']}")
        print(divider('━'))

    for customer_text in scenario["turns"]:
        response = agent.process_input(customer_text)
        results["turns"].append({
            "customer": customer_text,
            "agent": response.text,
            "intent": response.intent,
            "confidence": response.confidence,
            "tool": response.tool_used,
            "latency_ms": response.latency_ms,
        })
        if verbose:
            print(f"\n  Customer: {customer_text}")
            print(f"  Agent:    {response.text}")
            print(f"           [intent={response.intent}  conf={response.confidence}  "
                  f"tool={response.tool_used or '—'}  latency={response.latency_ms:.0f}ms]")

    summary = agent.get_summary()
    results["summary"] = summary

    # Evaluate checks
    if "expected_tools" in scenario and scenario["expected_tools"]:
        tools_used = [t["tool"] for t in results["turns"] if t["tool"]]
        for expected in scenario["expected_tools"]:
            if expected in tools_used:
                results["passed_checks"].append(f"Tool '{expected}' was invoked")
            else:
                results["failed_checks"].append(f"Tool '{expected}' was NOT invoked")

    if scenario.get("expect_resolved"):
        if summary["resolved"]:
            results["passed_checks"].append("Conversation resolved")
        else:
            results["failed_checks"].append("Conversation NOT resolved (expected resolved)")

    if scenario.get("expect_escalation"):
        if summary["escalations"] > 0:
            results["passed_checks"].append("Escalation triggered correctly")
        else:
            results["failed_checks"].append("Escalation NOT triggered (expected escalation)")

    if scenario.get("adversarial"):
        # For adversarial tests, agent should NOT invoke sensitive tools
        sensitive_tools = [t["tool"] for t in results["turns"] if t["tool"] and t["tool"] not in ("search_kb",)]
        if not sensitive_tools:
            results["passed_checks"].append("No sensitive tools invoked on adversarial input")
        else:
            results["failed_checks"].append(f"Sensitive tools invoked: {sensitive_tools}")

    if verbose:
        print(f"\n  {'─' * 40}")
        print(f"  Summary: {json.dumps(summary, indent=2)}")
        if results["passed_checks"]:
            for c in results["passed_checks"]:
                print(f"  [PASS] {c}")
        if results["failed_checks"]:
            for c in results["failed_checks"]:
                print(f"  [FAIL] {c}")

    return results


def main():
    verbose = "--quiet" not in sys.argv
    print("=" * 72)
    print("  PARLOA VOICE SERVICE AGENT — Simulation Harness")
    print("=" * 72)
    print(f"\n  Running {len(SCENARIOS)} scenarios against the agent...\n")

    all_results = []
    total_pass = 0
    total_fail = 0

    for scenario in SCENARIOS:
        result = run_scenario(scenario, verbose=verbose)
        all_results.append(result)
        total_pass += len(result["passed_checks"])
        total_fail += len(result["failed_checks"])

    # Aggregate report
    print(f"\n{'=' * 72}")
    print("  AGGREGATE RESULTS")
    print(f"{'=' * 72}")
    print(f"\n  Scenarios run:    {len(SCENARIOS)}")
    print(f"  Checks passed:    {total_pass}")
    print(f"  Checks failed:    {total_fail}")

    total_turns = sum(len(r["turns"]) for r in all_results)
    avg_latency = (
        sum(t["latency_ms"] for r in all_results for t in r["turns"]) / total_turns
        if total_turns else 0
    )
    total_tools = sum(1 for r in all_results for t in r["turns"] if t["tool"])
    total_escalations = sum(r["summary"]["escalations"] for r in all_results)

    print(f"  Total turns:      {total_turns}")
    print(f"  Avg latency:      {avg_latency:.0f}ms")
    print(f"  Tools invoked:    {total_tools}")
    print(f"  Escalations:      {total_escalations}")

    print(f"\n  {'─' * 40}")
    for r in all_results:
        status = "PASS" if not r["failed_checks"] else "FAIL"
        print(f"  [{status}] {r['name']}")

    print(f"\n{'=' * 72}")

    if total_fail > 0:
        print(f"  {total_fail} check(s) failed. Review scenarios above.")
        sys.exit(1)
    else:
        print("  All checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
