"""
Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use

Demonstrates the Trace-Free+ principles for rewriting tool/API descriptions
so LLM agents select and invoke them more reliably at scale.

Uses TF-IDF cosine similarity to simulate agent tool selection and measure
improvement from rewritten descriptions.
"""

import json
import re
import math
from collections import Counter
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ToolDescription:
    name: str
    description: str
    parameters: list  # list of dicts with name, type, required, desc
    returns: str
    example_input: str = ""
    example_output: str = ""
    see_also: str = ""

    def to_text(self) -> str:
        """Flatten to a single text block for similarity matching."""
        parts = [self.name, self.description, self.returns]
        for p in self.parameters:
            parts.append(f"{p['name']} {p['type']} {p['desc']}")
        if self.see_also:
            parts.append(self.see_also)
        return " ".join(parts)

    def to_display(self) -> str:
        """Pretty-print using the template from the paper."""
        lines = [
            f"Name: {self.name}",
            f"Description: {self.description}",
            "Parameters:",
        ]
        for p in self.parameters:
            req = "required" if p.get("required") else "optional"
            lines.append(f"  - {p['name']} ({p['type']}, {req}): {p['desc']}")
        lines.append(f"Returns: {self.returns}")
        if self.example_input:
            lines.append("Example:")
            lines.append(f"  Input: {self.example_input}")
            lines.append(f"  Output: {self.example_output}")
        if self.see_also:
            lines.append(f"See also: {self.see_also}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Original (bad) tool catalog -- deliberately ambiguous
# ---------------------------------------------------------------------------

ORIGINAL_CATALOG = [
    ToolDescription(
        name="get_restaurants",
        description="Get data from the restaurant API.",
        parameters=[
            {"name": "q", "type": "str", "required": True, "desc": "query"},
        ],
        returns="JSON data",
    ),
    ToolDescription(
        name="restaurant_order",
        description="Use this to interact with restaurants for orders and stuff.",
        parameters=[
            {"name": "data", "type": "dict", "required": True, "desc": "order data"},
        ],
        returns="result",
    ),
    ToolDescription(
        name="get_reviews",
        description="Get data about reviews.",
        parameters=[
            {"name": "id", "type": "str", "required": True, "desc": "identifier"},
        ],
        returns="review data",
    ),
    ToolDescription(
        name="search_menu",
        description="Search for items.",
        parameters=[
            {"name": "text", "type": "str", "required": True, "desc": "search text"},
        ],
        returns="list of items",
    ),
    ToolDescription(
        name="get_location",
        description="Get location data.",
        parameters=[
            {"name": "input", "type": "str", "required": True, "desc": "location input"},
        ],
        returns="location info",
    ),
    ToolDescription(
        name="make_reservation",
        description="Make a reservation or booking.",
        parameters=[
            {"name": "info", "type": "dict", "required": True, "desc": "reservation info"},
        ],
        returns="confirmation",
    ),
    ToolDescription(
        name="cancel_booking",
        description="Cancel something that was booked.",
        parameters=[
            {"name": "id", "type": "str", "required": True, "desc": "booking id"},
        ],
        returns="status",
    ),
    ToolDescription(
        name="get_hours",
        description="Get hours.",
        parameters=[
            {"name": "id", "type": "str", "required": True, "desc": "id"},
        ],
        returns="hours data",
    ),
]

# ---------------------------------------------------------------------------
# Rewritten (good) tool catalog -- applying Trace-Free+ principles
# ---------------------------------------------------------------------------

REWRITTEN_CATALOG = [
    ToolDescription(
        name="get_restaurants",
        description="Search restaurant listings by location and cuisine type. Returns metadata (name, address, rating) for matching restaurants. Does NOT place orders or fetch menus.",
        parameters=[
            {"name": "location", "type": "string", "required": True, "desc": "City name or 'lat,lng' pair. Must not be empty."},
            {"name": "cuisine", "type": "string", "required": False, "desc": "Cuisine filter, e.g. 'italian', 'sushi'. Omit for all cuisines."},
        ],
        returns="JSON array of {name: string, rating: float 0-5, address: string, id: string}.",
        example_input='{"location": "San Francisco", "cuisine": "italian"}',
        example_output='[{"name": "Trattoria Roma", "rating": 4.5, "address": "123 Main St", "id": "r_001"}]',
        see_also="search_menu for browsing a specific restaurant's dishes.",
    ),
    ToolDescription(
        name="restaurant_order",
        description="Place a food delivery order at a specific restaurant. Submits selected menu items for delivery to a given address. Does NOT search restaurants or browse menus.",
        parameters=[
            {"name": "restaurant_id", "type": "string", "required": True, "desc": "Restaurant ID from get_restaurants results."},
            {"name": "items", "type": "array[string]", "required": True, "desc": "List of menu item IDs from search_menu results."},
            {"name": "delivery_address", "type": "string", "required": True, "desc": "Full delivery address including zip code."},
        ],
        returns="JSON object {order_id: string, estimated_minutes: int, total_price: float}.",
        example_input='{"restaurant_id": "r_001", "items": ["m_42"], "delivery_address": "456 Oak Ave 94110"}',
        example_output='{"order_id": "ord_789", "estimated_minutes": 35, "total_price": 24.99}',
        see_also="get_restaurants to find restaurant IDs; search_menu to find item IDs.",
    ),
    ToolDescription(
        name="get_reviews",
        description="Retrieve customer reviews for a specific restaurant. Returns text reviews with ratings. Does NOT search for restaurants or fetch menu items.",
        parameters=[
            {"name": "restaurant_id", "type": "string", "required": True, "desc": "Restaurant ID from get_restaurants results."},
            {"name": "limit", "type": "int", "required": False, "desc": "Max reviews to return (default 10, max 50)."},
        ],
        returns="JSON array of {author: string, rating: int 1-5, text: string, date: string}.",
        example_input='{"restaurant_id": "r_001", "limit": 2}',
        example_output='[{"author": "Jane", "rating": 5, "text": "Amazing pasta!", "date": "2025-12-01"}]',
        see_also="get_restaurants to find restaurant IDs first.",
    ),
    ToolDescription(
        name="search_menu",
        description="Browse menu items for a specific restaurant by keyword. Returns dish names, prices, and dietary tags. Does NOT place orders.",
        parameters=[
            {"name": "restaurant_id", "type": "string", "required": True, "desc": "Restaurant ID from get_restaurants."},
            {"name": "query", "type": "string", "required": False, "desc": "Keyword filter, e.g. 'vegan', 'pasta'. Omit for full menu."},
        ],
        returns="JSON array of {item_id: string, name: string, price: float, tags: string[]}.",
        example_input='{"restaurant_id": "r_001", "query": "pasta"}',
        example_output='[{"item_id": "m_42", "name": "Carbonara", "price": 18.50, "tags": ["pasta"]}]',
        see_also="restaurant_order to place an order with item IDs from this result.",
    ),
    ToolDescription(
        name="get_location",
        description="Geocode an address or place name into coordinates. Resolves free-text location strings to structured lat/lng. Does NOT search restaurants or return business listings.",
        parameters=[
            {"name": "address", "type": "string", "required": True, "desc": "Free-text address or place name, e.g. 'Times Square, NYC'."},
        ],
        returns="JSON object {lat: float, lng: float, formatted_address: string}.",
        example_input='{"address": "Times Square, NYC"}',
        example_output='{"lat": 40.758, "lng": -73.9855, "formatted_address": "Times Square, Manhattan, NY"}',
        see_also="get_restaurants accepts lat,lng as location input.",
    ),
    ToolDescription(
        name="make_reservation",
        description="Book a dine-in table at a restaurant for a specific date, time, and party size. Does NOT order food for delivery -- use restaurant_order for that.",
        parameters=[
            {"name": "restaurant_id", "type": "string", "required": True, "desc": "Restaurant ID from get_restaurants."},
            {"name": "date", "type": "string", "required": True, "desc": "ISO date, e.g. '2026-03-15'."},
            {"name": "time", "type": "string", "required": True, "desc": "24h time, e.g. '19:30'."},
            {"name": "party_size", "type": "int", "required": True, "desc": "Number of guests (1-20)."},
        ],
        returns="JSON object {reservation_id: string, confirmed: bool, table_number: int}.",
        example_input='{"restaurant_id": "r_001", "date": "2026-03-15", "time": "19:30", "party_size": 4}',
        example_output='{"reservation_id": "res_456", "confirmed": true, "table_number": 7}',
        see_also="cancel_booking to cancel this reservation later.",
    ),
    ToolDescription(
        name="cancel_booking",
        description="Cancel an existing dine-in reservation by its reservation ID. Does NOT cancel delivery orders -- delivery orders cannot be cancelled via API.",
        parameters=[
            {"name": "reservation_id", "type": "string", "required": True, "desc": "Reservation ID returned by make_reservation."},
        ],
        returns="JSON object {cancelled: bool, refund_eligible: bool}.",
        example_input='{"reservation_id": "res_456"}',
        example_output='{"cancelled": true, "refund_eligible": true}',
        see_also="make_reservation to create a reservation.",
    ),
    ToolDescription(
        name="get_hours",
        description="Fetch operating hours for a specific restaurant on each day of the week. Does NOT check real-time availability or reservation slots.",
        parameters=[
            {"name": "restaurant_id", "type": "string", "required": True, "desc": "Restaurant ID from get_restaurants."},
        ],
        returns="JSON object mapping day names to {open: string, close: string} in 24h format.",
        example_input='{"restaurant_id": "r_001"}',
        example_output='{"Monday": {"open": "11:00", "close": "22:00"}, ...}',
        see_also="make_reservation to book a table during open hours.",
    ),
]


# ---------------------------------------------------------------------------
# Simple TF-IDF based tool selector (no external deps)
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def build_idf(documents: list[str]) -> dict[str, float]:
    n = len(documents)
    df = Counter()
    for doc in documents:
        df.update(set(tokenize(doc)))
    return {term: math.log((n + 1) / (count + 1)) + 1 for term, count in df.items()}


def tfidf_vector(text: str, idf: dict[str, float]) -> dict[str, float]:
    tokens = tokenize(text)
    tf = Counter(tokens)
    total = len(tokens) or 1
    return {t: (c / total) * idf.get(t, 1.0) for t, c in tf.items()}


def cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in keys)
    mag_a = math.sqrt(sum(v * v for v in a.values())) or 1e-9
    mag_b = math.sqrt(sum(v * v for v in b.values())) or 1e-9
    return dot / (mag_a * mag_b)


def select_tool(query: str, catalog: list[ToolDescription], idf: dict[str, float]) -> tuple[str, float]:
    """Select the best-matching tool for a query using TF-IDF cosine similarity."""
    q_vec = tfidf_vector(query, idf)
    best_name, best_score = "", -1.0
    for tool in catalog:
        t_vec = tfidf_vector(tool.to_text(), idf)
        score = cosine_sim(q_vec, t_vec)
        if score > best_score:
            best_score = score
            best_name = tool.name
    return best_name, best_score


# ---------------------------------------------------------------------------
# Contrastive test queries
# ---------------------------------------------------------------------------

TEST_QUERIES = [
    ("Find Italian restaurants near downtown Seattle", "get_restaurants"),
    ("Place an order for delivery from restaurant r_001", "restaurant_order"),
    ("Show me the reviews for this restaurant", "get_reviews"),
    ("What pasta dishes does this restaurant have?", "search_menu"),
    ("Convert '123 Main St' to latitude and longitude", "get_location"),
    ("Book a table for 4 people on Friday at 7pm", "make_reservation"),
    ("Cancel my dinner reservation res_456", "cancel_booking"),
    ("What time does this restaurant open on Monday?", "get_hours"),
    ("I want to see the menu for a sushi place", "search_menu"),
    ("Get coordinates for Times Square New York", "get_location"),
    ("Order two pizzas delivered to my apartment", "restaurant_order"),
    ("Reserve a spot for brunch this Saturday", "make_reservation"),
    ("I need to undo my booking", "cancel_booking"),
    ("What do other customers say about this place?", "get_reviews"),
    ("Is the restaurant open on Sunday evening?", "get_hours"),
    ("Search for Thai food restaurants in Chicago", "get_restaurants"),
]


# ---------------------------------------------------------------------------
# Audit report generation
# ---------------------------------------------------------------------------

def audit_catalog(catalog: list[ToolDescription]) -> list[str]:
    """Identify issues in tool descriptions following Step 1 of the framework."""
    issues = []
    # Check for ambiguous leading phrases
    leading_phrases = []
    for tool in catalog:
        words = tool.description.split()[:4]
        phrase = " ".join(words).lower().rstrip(".")
        for prev_name, prev_phrase in leading_phrases:
            overlap = set(phrase.split()) & set(prev_phrase.split())
            if len(overlap) >= 2:
                issues.append(
                    f"AMBIGUOUS: '{tool.name}' and '{prev_name}' share similar leading phrase "
                    f"('{phrase}' vs '{prev_phrase}')"
                )
        leading_phrases.append((tool.name, phrase))

    # Check for vague parameter names/descriptions
    vague_terms = {"data", "info", "input", "query", "result", "stuff", "something", "id", "text"}
    for tool in catalog:
        for p in tool.parameters:
            if p["name"] in vague_terms and len(p["desc"].split()) < 4:
                issues.append(
                    f"VAGUE PARAM: '{tool.name}.{p['name']}' has a generic name with minimal description: '{p['desc']}'"
                )

    # Check for missing return schema
    for tool in catalog:
        if len(tool.returns.split()) < 3:
            issues.append(
                f"MISSING SCHEMA: '{tool.name}' return description is too vague: '{tool.returns}'"
            )

    # Check description length (too short = likely ambiguous)
    for tool in catalog:
        wc = len(tool.description.split())
        if wc < 5:
            issues.append(
                f"TOO SHORT: '{tool.name}' description is only {wc} words -- likely ambiguous for an agent"
            )

    return issues


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def run_demo():
    print("=" * 72)
    print("  TOOL DESCRIPTION REWRITER DEMO")
    print("  Based on: Trace-Free+ Framework (arXiv:2602.20426)")
    print("=" * 72)

    # --- Step 1: Audit ---
    print("\n" + "-" * 72)
    print("STEP 1: AUDIT ORIGINAL CATALOG")
    print("-" * 72)
    issues = audit_catalog(ORIGINAL_CATALOG)
    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"  [{i}] {issue}")
    print(f"\n  Total issues found: {len(issues)}")

    # --- Step 2: Show before/after for a sample tool ---
    print("\n" + "-" * 72)
    print("STEP 2: REWRITE EXAMPLE (get_restaurants)")
    print("-" * 72)
    print("\n  BEFORE:")
    for line in ORIGINAL_CATALOG[0].to_display().split("\n"):
        print(f"    {line}")
    print("\n  AFTER:")
    for line in REWRITTEN_CATALOG[0].to_display().split("\n"):
        print(f"    {line}")

    # --- Step 3: Show full rewritten catalog ---
    print("\n" + "-" * 72)
    print("STEP 3: FULL REWRITTEN CATALOG")
    print("-" * 72)
    for tool in REWRITTEN_CATALOG:
        print(f"\n  {tool.to_display()}")
        # Word count check
        wc = len(tool.description.split())
        print(f"  [Word count: {wc}/200]")

    # --- Step 4: Validate with contrastive queries ---
    print("\n" + "-" * 72)
    print("STEP 4: CONTRASTIVE QUERY VALIDATION")
    print("-" * 72)

    # Build IDF for both catalogs
    orig_docs = [t.to_text() for t in ORIGINAL_CATALOG]
    rewr_docs = [t.to_text() for t in REWRITTEN_CATALOG]
    orig_idf = build_idf(orig_docs + [q for q, _ in TEST_QUERIES])
    rewr_idf = build_idf(rewr_docs + [q for q, _ in TEST_QUERIES])

    orig_correct = 0
    rewr_correct = 0

    print(f"\n  {'Query':<52} {'Expected':<18} {'Original':<18} {'Rewritten':<18}")
    print(f"  {'─' * 52} {'─' * 18} {'─' * 18} {'─' * 18}")

    for query, expected in TEST_QUERIES:
        orig_pick, _ = select_tool(query, ORIGINAL_CATALOG, orig_idf)
        rewr_pick, _ = select_tool(query, REWRITTEN_CATALOG, rewr_idf)

        orig_ok = orig_pick == expected
        rewr_ok = rewr_pick == expected
        orig_correct += int(orig_ok)
        rewr_correct += int(rewr_ok)

        orig_mark = "OK" if orig_ok else "MISS"
        rewr_mark = "OK" if rewr_ok else "MISS"

        q_short = query[:50] + ".." if len(query) > 50 else query
        print(f"  {q_short:<52} {expected:<18} {orig_mark:<18} {rewr_mark:<18}")

    total = len(TEST_QUERIES)
    print(f"\n  ACCURACY:")
    print(f"    Original catalog:  {orig_correct}/{total} ({100 * orig_correct / total:.0f}%)")
    print(f"    Rewritten catalog: {rewr_correct}/{total} ({100 * rewr_correct / total:.0f}%)")
    improvement = rewr_correct - orig_correct
    if improvement > 0:
        print(f"    Improvement:       +{improvement} correct selections ({100 * improvement / total:.0f}% points)")
    elif improvement == 0:
        print(f"    (No change in accuracy with this query set)")
    else:
        print(f"    Delta: {improvement} (unexpected regression)")

    # --- Summary ---
    print("\n" + "-" * 72)
    print("KEY PRINCIPLES APPLIED (from Trace-Free+ / arXiv:2602.20426)")
    print("-" * 72)
    principles = [
        "Lead with a unique, discriminative verb-object phrase",
        "State what each tool does NOT do (boundary clarity)",
        "Enumerate parameters with types, defaults, and constraints inline",
        "Specify return schema concisely",
        "Include a single canonical example per tool",
        "Keep descriptions under 200 words",
        "Cross-reference commonly confused tools",
        "Validate with contrastive queries",
    ]
    for i, p in enumerate(principles, 1):
        print(f"  {i}. {p}")

    print("\n" + "=" * 72)
    print("  Demo complete.")
    print("=" * 72)


if __name__ == "__main__":
    run_demo()
