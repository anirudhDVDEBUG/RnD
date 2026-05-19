#!/usr/bin/env python3
"""
Agent Design Patterns — Interactive Demo
=========================================
Demonstrates the 7x6 framework: grid view, pattern search, architecture
recommendations, and composition analysis. No API keys required.
"""

from agent_patterns import PatternFramework, LAYERS, CONCERNS

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def hr(char="─", width=80):
    print(f"{DIM}{char * width}{RESET}")

def section(title):
    print()
    hr("═")
    print(f"{BOLD}{CYAN}{title}{RESET}")
    hr("═")

def main():
    fw = PatternFramework()

    # --- 1. Full grid ---
    section("1. THE 7x6 AGENT DESIGN PATTERN GRID")
    print(f"\n{DIM}28 patterns across 7 layers x 6 concerns:{RESET}\n")
    print(fw.grid())

    # --- 2. Layer drill-down ---
    section("2. DRILL DOWN: Single Agent Layer")
    for p in fw.by_layer("Single Agent"):
        print(f"\n  {GREEN}{p.short()}{RESET}")
        print(f"    {p.summary}")
        print(f"    {DIM}Use when: {p.when_to_use}{RESET}")

    # --- 3. Concern drill-down ---
    section("3. DRILL DOWN: Error Recovery Concern")
    for p in fw.by_concern("Error Recovery"):
        print(f"\n  {GREEN}{p.short()}{RESET}")
        print(f"    {p.summary}")

    # --- 4. Pattern search ---
    section("4. SEARCH: 'tool routing retry'")
    results = fw.search("tool routing retry")
    for i, p in enumerate(results[:5], 1):
        print(f"  {i}. {YELLOW}{p.name}{RESET} ({p.layer} / {p.concern})")
        print(f"     {p.summary}")

    # --- 5. Architecture presets ---
    section("5. ARCHITECTURE PRESETS")
    for archetype in ["autonomous_agent", "research_agent", "agent_swarm", "production_pipeline"]:
        arch = fw.architecture_for(archetype)
        print(f"\n  {BOLD}{arch['name']}{RESET}: {arch['description']}")
        for p in arch["pattern_details"]:
            print(f"    • {p.name} {DIM}{p.coordinate}{RESET}")

    # --- 6. Composition analysis ---
    section("6. COMPOSITION ANALYSIS: ReAct Loop")
    react = fw.get("ReAct Loop")
    print(f"\n  {fw.detail(react)}\n")
    print(f"  {BOLD}Composition chain (2 hops):{RESET}")
    seen = {react.name}
    for name in react.composable_with:
        p = fw.get(name)
        if p:
            print(f"    → {GREEN}{p.name}{RESET} {p.coordinate}")
            for name2 in p.composable_with:
                if name2 not in seen:
                    p2 = fw.get(name2)
                    if p2:
                        print(f"        → {DIM}{p2.name} {p2.coordinate}{RESET}")
                        seen.add(name2)

    # --- 7. Use-case recommendation ---
    section("7. RECOMMEND PATTERNS FOR A USE CASE")
    use_case = "I'm building a customer support agent that retrieves docs, uses tools, and needs human approval for refunds"
    print(f"\n  {DIM}Use case: \"{use_case}\"{RESET}\n")
    recs = fw.recommend(use_case, top_n=6)
    for i, p in enumerate(recs, 1):
        print(f"  {i}. {YELLOW}{p.name}{RESET}  {p.coordinate}")
        print(f"     {p.summary}")
        print(f"     {DIM}Frameworks: {', '.join(p.example_frameworks)}{RESET}")

    # --- 8. Stats ---
    section("8. FRAMEWORK STATS")
    print(f"\n  Total patterns:  {len(fw.patterns)}")
    print(f"  Layers:          {len(LAYERS)}")
    print(f"  Concerns:        {len(CONCERNS)}")
    filled = len(fw.patterns)
    total = len(LAYERS) * len(CONCERNS)
    print(f"  Grid coverage:   {filled}/{total} cells ({100*filled//total}%)")
    fw_counts = {}
    for p in fw.patterns:
        for f in p.example_frameworks:
            fw_counts[f] = fw_counts.get(f, 0) + 1
    print(f"  Framework refs:  {', '.join(f'{k}: {v}' for k, v in sorted(fw_counts.items(), key=lambda x: -x[1]))}")

    print(f"\n{GREEN}Done. All 28 patterns loaded and queryable.{RESET}\n")


if __name__ == "__main__":
    main()
