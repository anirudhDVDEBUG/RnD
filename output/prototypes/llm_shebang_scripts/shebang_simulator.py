#!/usr/bin/env python3
"""
shebang_simulator.py — Simulate running LLM shebang scripts locally without
the llm CLI or any API keys. Produces mock output to demonstrate the concept.

This is the demo harness for the prototype: it parses shebang scripts the same
way the real `llm` CLI would, then generates plausible mock responses so you
can see the end-to-end flow.
"""

import os
import sys
import yaml
import textwrap
from datetime import datetime

# Mock responses keyed by prompt fragments
MOCK_RESPONSES = {
    "pelican": textwrap.dedent("""\
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
          <circle cx="100" cy="80" r="30" fill="#f5a623" />
          <ellipse cx="100" cy="75" rx="35" ry="20" fill="#f5d76e" />
          <path d="M70 80 Q50 90 65 100" stroke="#e67e22" fill="none" stroke-width="3"/>
          <circle cx="90" cy="72" r="3" fill="black"/>
          <line x1="80" y1="110" x2="70" y2="150" stroke="#333" stroke-width="2"/>
          <line x1="120" y1="110" x2="130" y2="150" stroke="#333" stroke-width="2"/>
          <circle cx="70" cy="165" r="15" fill="none" stroke="#333" stroke-width="2"/>
          <circle cx="130" cy="165" r="15" fill="none" stroke="#333" stroke-width="2"/>
          <line x1="70" y1="165" x2="130" y2="165" stroke="#333" stroke-width="2"/>
          <text x="50" y="195" font-size="10" fill="#666">Pelican on a bicycle</text>
        </svg>"""),

    "haiku": textwrap.dedent(f"""\
        Clock strikes {datetime.now().strftime('%I:%M')} sharp
        Silence fills the afternoon
        Time drifts like the clouds"""),

    "commit": "feat: add user authentication middleware for API routes",

    "code review": textwrap.dedent("""\
        **Security**
        - No input sanitization on user-provided query parameters
        - SQL query uses string interpolation instead of parameterized queries

        **Performance**
        - N+1 query pattern in the loop at line 42; batch the lookups
        - Missing index on `users.email` column

        **Style**
        - Inconsistent naming: mix of camelCase and snake_case
        - Function `doStuff()` needs a descriptive name"""),
}

CALC_MOCK = textwrap.dedent("""\
    I'll solve this step by step using the available tools.

    [Tool call: multiply(2344, 5252)]
    → Result: 12,310,688

    [Tool call: add(12310688, 134)]
    → Result: 12,310,822

    The answer is **12,310,822**.""")


def find_mock_response(prompt_text: str) -> str:
    """Match prompt text against mock responses."""
    lower = prompt_text.lower()
    for key, response in MOCK_RESPONSES.items():
        if key in lower:
            return response
    return f"[Mock LLM response to: {prompt_text[:80]}...]"


def simulate_fragment(filepath: str, shebang_parts: list[str]) -> None:
    """Simulate a fragment-mode (-f) script."""
    with open(filepath) as f:
        lines = f.readlines()
    prompt = "".join(lines[1:]).strip()

    tools = [shebang_parts[i + 1] for i, p in enumerate(shebang_parts) if p == "-T" and i + 1 < len(shebang_parts)]

    print(f"{'=' * 60}")
    print(f"  Simulating fragment script: {os.path.basename(filepath)}")
    print(f"  Mode: fragment (-f)")
    if tools:
        print(f"  Tools: {', '.join(tools)}")
    print(f"{'=' * 60}")
    print(f"\n  PROMPT:\n  {prompt}\n")
    print(f"  RESPONSE:\n")

    response = find_mock_response(prompt)
    for line in response.split("\n"):
        print(f"  {line}")
    print()


def simulate_template(filepath: str, extra_args: list[str]) -> None:
    """Simulate a template-mode (-t) script."""
    with open(filepath) as f:
        lines = f.readlines()
    yaml_body = "".join(lines[1:])
    template = yaml.safe_load(yaml_body)

    model = template.get("model", "default")
    system = template.get("system", "")
    functions = template.get("functions", "")
    prompt_text = " ".join(extra_args) if extra_args else template.get("prompt", "")

    print(f"{'=' * 60}")
    print(f"  Simulating template script: {os.path.basename(filepath)}")
    print(f"  Mode: template (-t)")
    print(f"  Model: {model}")
    if system:
        print(f"  System: {system.strip()[:60]}...")
    if functions:
        # Extract function names
        fn_names = [line.split("def ")[1].split("(")[0] for line in functions.split("\n") if line.strip().startswith("def ")]
        print(f"  Functions: {', '.join(fn_names)}")
    print(f"{'=' * 60}")

    if prompt_text:
        print(f"\n  INPUT: {prompt_text}\n")
    print(f"  RESPONSE:\n")

    if any(fn in functions for fn in ["add", "multiply"]):
        response = CALC_MOCK
    else:
        response = find_mock_response(prompt_text or system)

    for line in response.split("\n"):
        print(f"  {line}")
    print()


def simulate(filepath: str, extra_args: list[str] | None = None) -> None:
    """Parse and simulate any LLM shebang script."""
    extra_args = extra_args or []

    with open(filepath) as f:
        first_line = f.readline().strip()

    if not first_line.startswith("#!"):
        print(f"Error: {filepath} has no shebang line", file=sys.stderr)
        sys.exit(1)

    parts = first_line.split()

    if "-f" in parts:
        simulate_fragment(filepath, parts)
    elif "-t" in parts:
        simulate_template(filepath, extra_args)
    else:
        print(f"Error: shebang must contain -f or -t flag", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python shebang_simulator.py <script> [args...]")
        print("Simulates running an LLM shebang script with mock responses.")
        sys.exit(1)

    filepath = sys.argv[1]
    extra_args = sys.argv[2:]
    simulate(filepath, extra_args)


if __name__ == "__main__":
    main()
