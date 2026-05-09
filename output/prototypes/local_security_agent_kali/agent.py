#!/usr/bin/env python3
"""Autonomous security agent — plan-act-observe loop powered by a local LLM."""

import argparse
import json
import textwrap

import config
from llm_client import ask
from tools.recon import nmap_scan, whois_lookup
from tools.web import nikto_scan
from tools.exploit import searchsploit

TOOL_MAP = {
    "nmap_scan": nmap_scan,
    "nikto_scan": nikto_scan,
    "whois_lookup": whois_lookup,
    "searchsploit": searchsploit,
}


def build_prompt(objective: str, target: str, history: list) -> str:
    """Build a prompt with objective, target, and action history."""
    hist_text = ""
    for i, entry in enumerate(history, 1):
        result_snippet = entry["result"][:500]
        hist_text += f"\n--- Step {i}: {entry['action']} ---\n{result_snippet}\n"

    return textwrap.dedent(f"""\
        Objective: {objective}
        Target: {target}

        Previous actions and results:{hist_text if hist_text else " (none yet)"}

        Decide the next action. Respond with JSON only.""")


def parse_action(response: str) -> tuple:
    """Parse the LLM JSON response into (action, args)."""
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from surrounding text
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
        else:
            return "DONE", {"summary": "Failed to parse LLM response."}

    action = data.get("action", "DONE")
    if action == "DONE":
        return "DONE", {"summary": data.get("summary", "No summary.")}
    return action, data.get("args", {})


def run_agent(objective: str, target: str) -> list:
    """Execute the agent loop and return history."""
    history = []
    print(f"\n{'='*60}")
    print(f"  LOCAL SECURITY AGENT")
    print(f"  Objective : {objective}")
    print(f"  Target    : {target}")
    print(f"  Model     : {config.LLM_MODEL}")
    print(f"  Mock mode : {'ON' if config.MOCK_MODE else 'OFF'}")
    print(f"{'='*60}\n")

    for step in range(1, config.MAX_STEPS + 1):
        prompt = build_prompt(objective, target, history)
        print(f"[Step {step}] Querying LLM for next action...")
        response = ask(prompt)

        action, args = parse_action(response)

        if action == "DONE":
            print(f"\n{'='*60}")
            print("  AGENT COMPLETE")
            print(f"{'='*60}")
            print(f"\nSummary:\n{args.get('summary', 'N/A')}\n")
            break

        if action not in TOOL_MAP:
            print(f"  Unknown action: {action} — skipping.")
            continue

        args_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
        print(f"  -> Running: {action}({args_str})")

        try:
            observation = TOOL_MAP[action](**args)
        except Exception as e:
            observation = f"ERROR: {e}"

        # Show truncated output
        preview = observation[:300].rstrip()
        if len(observation) > 300:
            preview += "\n  ... (truncated)"
        print(f"  Result:\n{textwrap.indent(preview, '    ')}\n")

        history.append({"action": action, "args": args, "result": observation})

    return history


def main():
    parser = argparse.ArgumentParser(description="Local Security Agent")
    parser.add_argument("--target", default="192.168.1.100",
                        help="Target IP or hostname")
    parser.add_argument("--objective", default="enumerate open services and check for known vulnerabilities",
                        help="Agent objective")
    args = parser.parse_args()

    run_agent(args.objective, args.target)


if __name__ == "__main__":
    main()
