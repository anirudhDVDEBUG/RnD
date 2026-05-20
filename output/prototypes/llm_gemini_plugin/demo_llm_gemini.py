#!/usr/bin/env python3
"""
Demo: llm-gemini 0.32a0 — reasoning token streaming simulation.

Simulates what `llm -m gemini-2.0-flash-thinking` looks like when the
llm-gemini 0.32a0 plugin streams reasoning (thinking) tokens before the
final answer.  No API key required — uses mock data.
"""

import json
import sys
import textwrap
import time
from datetime import datetime

# ── Colour helpers (ANSI) ───────────────────────────────────────────
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def type_out(text, delay=0.010, color=""):
    """Simulate streaming token output."""
    for ch in text:
        sys.stdout.write(f"{color}{ch}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)


# ── Mock data ───────────────────────────────────────────────────────
GEMINI_MODELS = [
    {"model_id": "gemini-2.5-pro", "note": "1M ctx, thinking"},
    {"model_id": "gemini-2.5-flash", "note": "1M ctx, thinking"},
    {"model_id": "gemini-2.0-flash", "note": "1M ctx"},
    {"model_id": "gemini-2.0-flash-thinking", "note": "1M ctx, CoT streaming"},
    {"model_id": "gemini-2.0-flash-lite", "note": "1M ctx, fast"},
    {"model_id": "gemini-1.5-pro", "note": "2M ctx"},
    {"model_id": "gemini-1.5-flash", "note": "1M ctx"},
]

REASONING_TOKENS = [
    "I need to prove there are infinitely many primes.",
    "The classic proof is by Euclid -- a proof by contradiction.",
    "Assume there are finitely many primes: p1, p2, ..., pn.",
    "Consider N = p1 * p2 * ... * pn + 1.",
    "N is not divisible by any pi (remainder is always 1).",
    "So N is either prime itself, or has a prime factor not in our list.",
    "Either way, we have a prime not in {p1, ..., pn} -- contradiction.",
    "Therefore, there must be infinitely many primes. QED.",
]

FINAL_ANSWER = textwrap.dedent("""\
**Theorem.** There are infinitely many prime numbers.

**Proof (Euclid).** Suppose, for contradiction, that there are only
finitely many primes: p_1, p_2, ..., p_n.

Define N = p_1 * p_2 * ... * p_n + 1.

For every p_i in our list, N mod p_i = 1, so no p_i divides N.

Therefore N is either prime itself or has a prime factor not in our
list. In both cases a new prime exists -- contradicting our assumption.

Hence the set of primes is infinite.  QED.
""")


def header(text):
    print(f"\n{BOLD}{'=' * 64}{RESET}")
    print(f"  {BOLD}{text}{RESET}")
    print(f"{BOLD}{'=' * 64}{RESET}\n")


def cmd(command):
    print(f"  {DIM}$ {command}{RESET}\n")


# ── Demo sections ──────────────────────────────────────────────────

def demo_install():
    header("Step 1: Install llm + llm-gemini 0.32a0 (alpha)")
    cmd("pip install 'llm>=0.32a0'")
    print("  [mock] Successfully installed llm-0.32a0")
    cmd("llm install llm-gemini==0.32a0")
    print("  [mock] Successfully installed llm-gemini-0.32a0\n")


def demo_list_models():
    header("Step 2: Available Gemini models")
    cmd("llm models list | grep gemini")
    for m in GEMINI_MODELS:
        marker = f"  {GREEN}<-- reasoning streaming{RESET}" if "CoT" in m["note"] else ""
        print(f"  {GREEN}{m['model_id']:<35}{RESET} {DIM}{m['note']}{RESET}{marker}")
    print(f"\n  {len(GEMINI_MODELS)} Gemini models registered\n")


def demo_key_setup():
    header("Step 3: API key setup")
    cmd("llm keys set gemini")
    print(f"  {DIM}Enter key: ****************************{RESET}")
    print(f"  {GREEN}Key saved to ~/.llm/keys.json{RESET}\n")


def demo_reasoning_stream():
    header("Step 4: Reasoning token streaming (the headline feature)")
    prompt = "Prove that there are infinitely many primes"
    cmd(f'llm -m gemini-2.0-flash-thinking "{prompt}"')

    time.sleep(0.3)

    # Stream reasoning tokens
    print(f"  {YELLOW}{BOLD}[reasoning]{RESET}")
    for token in REASONING_TOKENS:
        type_out(f"    {token}\n", delay=0.006, color=DIM)
        time.sleep(0.1)
    print(f"  {YELLOW}{BOLD}[/reasoning]{RESET}\n")

    time.sleep(0.2)

    # Stream final answer
    print(f"  {GREEN}{BOLD}[answer]{RESET}")
    type_out(textwrap.indent(FINAL_ANSWER, "    "), delay=0.004, color=CYAN)
    print(f"  {GREEN}{BOLD}[/answer]{RESET}\n")

    meta = {
        "model": "gemini-2.0-flash-thinking",
        "reasoning_tokens": 89,
        "output_tokens": 112,
        "duration_ms": 3241,
    }
    print(f"  {DIM}[metadata] {json.dumps(meta)}{RESET}\n")


def demo_basic_prompt():
    header("Step 5: Basic prompt (no reasoning)")
    cmd('llm -m gemini-2.0-flash "Explain quantum computing in one sentence"')
    response = (
        "Quantum computing uses qubits that exploit superposition and "
        "entanglement to solve certain problems exponentially faster "
        "than classical computers."
    )
    for line in textwrap.wrap(response, width=68):
        print(f"  {line}")
    print()


def demo_plugin_info():
    header("Step 6: Plugin info")
    cmd("llm plugins")
    info = {
        "name": "llm-gemini",
        "version": "0.32a0",
        "hooks": ["register_models", "register_embedding_models"],
    }
    print(f"  {json.dumps(info, indent=4)}\n")


def main():
    print(f"\n  {BOLD}llm-gemini 0.32a0 -- Reasoning Token Streaming Demo{RESET}")
    print(f"  {DIM}Simulated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  (No API key required -- mock responses){RESET}")

    demo_install()
    demo_list_models()
    demo_key_setup()
    demo_reasoning_stream()
    demo_basic_prompt()
    demo_plugin_info()

    header("Done")
    print("  To use for real: pip install 'llm>=0.32a0' && llm install llm-gemini==0.32a0")
    print("  Then: llm keys set gemini")
    print("  See HOW_TO_USE.md for full instructions.\n")


if __name__ == "__main__":
    main()
