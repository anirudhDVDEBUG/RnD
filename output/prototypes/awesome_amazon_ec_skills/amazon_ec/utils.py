"""Shared scoring and formatting utilities."""


def score_title(title: str) -> dict:
    score = 100
    issues = []
    fixes = []
    length = len(title)

    if length < 80:
        penalty = min(30, (80 - length))
        score -= penalty
        issues.append(f"Too short ({length} chars, target 150-200)")
        fixes.append("Add primary keywords and product attributes")
    elif length > 200:
        penalty = min(20, (length - 200) // 5)
        score -= penalty
        issues.append(f"Too long ({length} chars, target 150-200)")
        fixes.append("Trim redundant words, keep top keywords")

    words = title.lower().split()
    if words and not words[0][0].isupper() and not title[0].isupper():
        score -= 5
        issues.append("Title doesn't start with capital letter")

    if title == title.upper():
        score -= 15
        issues.append("All caps — violates Amazon style guide")
        fixes.append("Use title case")

    if title == title.lower():
        score -= 10
        issues.append("All lowercase — poor visibility")
        fixes.append("Use title case for main words")

    keyword_indicators = ["for", "with", "-", "|", ","]
    has_structure = any(ind in title for ind in keyword_indicators)
    if not has_structure:
        score -= 10
        issues.append("No keyword separators (-, |, commas)")
        fixes.append("Add separators between keyword groups")

    return {"score": max(0, score), "issues": issues, "fixes": fixes}


def score_bullets(bullets: list) -> dict:
    score = 100
    issues = []
    fixes = []

    if len(bullets) < 5:
        score -= (5 - len(bullets)) * 10
        issues.append(f"Only {len(bullets)} bullets (use all 5)")
        fixes.append("Add bullets to fill all 5 slots")

    for i, bullet in enumerate(bullets):
        if len(bullet) < 50:
            score -= 5
            issues.append(f"Bullet {i+1} too short ({len(bullet)} chars)")

        words = bullet.lower().split()
        benefit_words = {"keeps", "protects", "prevents", "ensures", "delivers",
                         "provides", "designed", "perfect", "ideal", "premium",
                         "guaranteed", "never", "always", "enjoy"}
        if not benefit_words.intersection(words):
            score -= 3

    short_bullets = sum(1 for b in bullets if len(b) < 100)
    if short_bullets >= 3:
        fixes.append("Expand bullets with benefits, use cases, and keywords")

    return {"score": max(0, score), "issues": issues, "fixes": fixes}


def format_currency(value: float, currency: str = "USD") -> str:
    symbols = {"USD": "$", "RMB": "\u00a5", "EUR": "\u20ac", "GBP": "\u00a3"}
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{value:,.2f}"


def format_pct(value: float) -> str:
    return f"{value:.1f}%"
