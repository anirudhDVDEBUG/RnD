"""
Pronounce Dev Jargon — local pronunciation database and lookup engine.
Subset of the full 540+ entry database for demonstration purposes.
"""

import json
import sys

TERMS_DB = [
    {"term": "kubectl", "spoken": "koob-control", "alt": ["koob-cuddle", "koob-C-T-L"], "confidence": "high", "source": "Kubernetes official documentation"},
    {"term": "nginx", "spoken": "engine-X", "alt": [], "confidence": "high", "source": "Igor Sysoev (creator)"},
    {"term": "JWT", "spoken": "jot", "alt": ["J-W-T"], "confidence": "medium", "source": "RFC 7519 authors"},
    {"term": "GIF", "spoken": "jif", "alt": ["gif (hard G)"], "confidence": "contested", "source": "Steve Wilhite (creator) vs popular usage"},
    {"term": "SQL", "spoken": "sequel", "alt": ["S-Q-L"], "confidence": "contested", "source": "IBM original vs ISO standard"},
    {"term": "char", "spoken": "kar", "alt": ["char (like charcoal)"], "confidence": "contested", "source": "Community split"},
    {"term": "sudo", "spoken": "soo-doo", "alt": ["soo-doe"], "confidence": "high", "source": "Unix tradition"},
    {"term": "Linux", "spoken": "lin-ucks", "alt": ["lie-nucks"], "confidence": "high", "source": "Linus Torvalds audio clip"},
    {"term": "Kubernetes", "spoken": "koo-ber-NET-eez", "alt": [], "confidence": "high", "source": "Greek origin, Google team"},
    {"term": "OAuth", "spoken": "oh-auth", "alt": ["O-auth"], "confidence": "high", "source": "IETF working group"},
    {"term": "JSON", "spoken": "jay-son", "alt": ["jay-sawn"], "confidence": "high", "source": "Douglas Crockford (creator)"},
    {"term": "YAML", "spoken": "yam-ul", "alt": [], "confidence": "high", "source": "Spec authors"},
    {"term": "wget", "spoken": "double-you-get", "alt": ["wuh-get"], "confidence": "medium", "source": "GNU project"},
    {"term": "PyPI", "spoken": "pie-P-eye", "alt": ["pie-pie", "pippy"], "confidence": "medium", "source": "Python Packaging Authority"},
    {"term": "Postgres", "spoken": "post-gres", "alt": ["post-gree-S-Q-L"], "confidence": "high", "source": "PostgreSQL project"},
    {"term": "Redis", "spoken": "RED-iss", "alt": [], "confidence": "high", "source": "Salvatore Sanfilippo (creator)"},
    {"term": "Apache", "spoken": "uh-PATCH-ee", "alt": [], "confidence": "high", "source": "ASF"},
    {"term": "Vercel", "spoken": "ver-SELL", "alt": [], "confidence": "high", "source": "Company branding"},
    {"term": "Supabase", "spoken": "SOO-puh-base", "alt": [], "confidence": "high", "source": "Company branding"},
    {"term": "Vite", "spoken": "veet", "alt": [], "confidence": "high", "source": "Evan You (creator), French word for 'fast'"},
    {"term": "Deno", "spoken": "DEE-no", "alt": [], "confidence": "high", "source": "Ryan Dahl (creator)"},
    {"term": "gRPC", "spoken": "gee-R-P-C", "alt": [], "confidence": "high", "source": "Google"},
    {"term": "Huawei", "spoken": "WAH-way", "alt": [], "confidence": "high", "source": "Company official"},
    {"term": "IEEE", "spoken": "eye-triple-E", "alt": [], "confidence": "high", "source": "IEEE organization"},
    {"term": "Pygame", "spoken": "pie-game", "alt": [], "confidence": "high", "source": "Project docs"},
    {"term": "LaTeX", "spoken": "lah-tek", "alt": ["lay-tek"], "confidence": "high", "source": "Leslie Lamport"},
    {"term": "GNOME", "spoken": "guh-NOME", "alt": ["nome"], "confidence": "medium", "source": "GNOME project"},
    {"term": "GUI", "spoken": "goo-ee", "alt": [], "confidence": "high", "source": "Industry standard"},
    {"term": "API", "spoken": "A-P-I", "alt": [], "confidence": "high", "source": "Industry standard"},
    {"term": "CLI", "spoken": "C-L-I", "alt": ["clee"], "confidence": "high", "source": "Industry standard"},
]


def lookup(term):
    """Exact case-insensitive lookup."""
    term_lower = term.lower().strip()
    for entry in TERMS_DB:
        if entry["term"].lower() == term_lower:
            return entry
    return None


def search(query):
    """Prefix/substring search."""
    query_lower = query.lower().strip()
    results = []
    for entry in TERMS_DB:
        if query_lower in entry["term"].lower():
            results.append(entry)
    return results


def format_entry(entry):
    """Format a single entry for display."""
    lines = []
    alt_str = f' (alt: "{", ".join(entry["alt"])}")' if entry["alt"] else ""
    lines.append(f'  Pronunciation: "{entry["spoken"]}"{alt_str}')
    lines.append(f'  Confidence: {entry["confidence"]}')
    lines.append(f'  Source: {entry["source"]}')
    return "\n".join(lines)


def demo_lookups():
    """Run demo lookups for common terms."""
    print("\n=== Pronounce Dev Jargon — Demo ===\n")
    demo_terms = ["kubectl", "GIF", "JWT", "nginx", "SQL", "Vite", "Linux", "sudo"]
    for term in demo_terms:
        entry = lookup(term)
        if entry:
            print(f"Looking up: {term}")
            print(format_entry(entry))
            print()


def interactive_mode():
    """Interactive lookup mode."""
    print("Interactive mode (type a term, or 'quit' to exit):")
    while True:
        try:
            term = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not term or term.lower() == "quit":
            break
        entry = lookup(term)
        if entry:
            print(format_entry(entry))
        else:
            results = search(term)
            if results:
                print(f"  No exact match. Did you mean: {', '.join(r['term'] for r in results)}?")
            else:
                print(f"  '{term}' not found in database ({len(TERMS_DB)} entries loaded).")
        print()


if __name__ == "__main__":
    demo_lookups()
    if sys.stdin.isatty():
        interactive_mode()
    print("Done. Full database: https://github.com/anzy-renlab-ai/pronounce")
