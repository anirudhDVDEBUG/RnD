#!/usr/bin/env python3
"""
Demo simulator for web-researcher-mcp.

Exercises all six MCP tools with mock data so you can see the response
shapes without needing a Brave API key or SearXNG instance.
"""

import json
import textwrap
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_WEB_RESULTS = [
    {
        "title": "QuantumScape Ships First Solid-State Cells to Volkswagen",
        "url": "https://quantumscape.com/press/first-commercial-cells",
        "snippet": "QuantumScape announced shipment of its first commercial solid-state "
                   "lithium-metal battery cells to Volkswagen, marking a milestone in EV "
                   "battery technology after years of development.",
        "source": "brave",
    },
    {
        "title": "Toyota Reveals 900-Mile Solid-State EV Battery Prototype",
        "url": "https://toyota.com/news/solid-state-battery-2026",
        "snippet": "Toyota's prototype solid-state battery achieves 900 miles on a single "
                   "charge with 10-minute fast charging, targeting mass production by 2028.",
        "source": "brave",
    },
    {
        "title": "Samsung SDI Demonstrates Solid-State Cell with 1000-Cycle Durability",
        "url": "https://samsungsdi.com/solid-state-update",
        "snippet": "Samsung SDI's latest solid-state prototype exceeds 1000 charge cycles "
                   "with less than 5% capacity degradation, addressing a key barrier to "
                   "commercialization.",
        "source": "brave",
    },
]

MOCK_EXTRACTED_CONTENT = {
    "url": "https://quantumscape.com/press/first-commercial-cells",
    "title": "QuantumScape Ships First Solid-State Cells to Volkswagen",
    "extraction_tier": 1,
    "extraction_method": "raw_http_get",
    "content": textwrap.dedent("""\
        SAN JOSE, CA -- QuantumScape Corporation (NYSE: QS) today announced the
        shipment of its first commercially-formatted solid-state lithium-metal
        battery cells to Volkswagen Group.

        The QSE-5 cells feature an energy density of 800 Wh/L, roughly double
        that of conventional lithium-ion cells. Key specifications:

        - Energy density: 800 Wh/L
        - Fast charge: 0-80% in under 15 minutes
        - Operating temperature: -30C to 60C
        - Cycle life: >800 cycles to 80% capacity

        "This shipment marks the transition from laboratory to production," said
        CEO Siva Sivaram. "Solid-state technology is no longer a science project."

        Volkswagen plans to integrate the cells into its SSP platform starting
        with the 2028 model year. Financial terms were not disclosed.
    """),
    "word_count": 112,
    "language": "en",
}

MOCK_ACADEMIC_RESULTS = [
    {
        "title": "Interfacial Engineering of Sulfide Solid Electrolytes for All-Solid-State Batteries",
        "authors": ["Chen, Y.", "Wang, L.", "Zhang, H."],
        "year": 2025,
        "journal": "Nature Energy",
        "doi": "10.1038/s41560-025-01678-3",
        "citation_count": 47,
        "abstract": "We demonstrate a scalable interfacial coating strategy that reduces "
                     "charge-transfer resistance at the cathode-electrolyte interface by 85%, "
                     "enabling stable cycling at 5C rates for over 2000 cycles.",
    },
    {
        "title": "Machine-Learning-Guided Discovery of Novel Lithium Superionic Conductors",
        "authors": ["Park, J.", "Kim, S.", "Ceder, G."],
        "year": 2025,
        "journal": "Science",
        "doi": "10.1126/science.adp9012",
        "citation_count": 92,
        "abstract": "Using a graph neural network trained on 48,000 crystal structures, we "
                     "identify 12 new lithium superionic conductors with room-temperature "
                     "ionic conductivity exceeding 10 mS/cm.",
    },
]

MOCK_PATENT_RESULTS = [
    {
        "title": "Lithium Metal Anode Protection Layer for Solid-State Batteries",
        "patent_number": "US-2025-0312456-A1",
        "assignee": "QuantumScape Corporation",
        "filing_date": "2024-06-15",
        "status": "Published",
        "abstract": "A protective interlayer comprising a ceramic-polymer composite is "
                     "disposed between the lithium metal anode and the solid electrolyte, "
                     "suppressing dendrite formation during high-rate charging.",
    },
    {
        "title": "Method for Manufacturing Thin-Film Solid Electrolyte Membranes",
        "patent_number": "US-2025-0298711-A1",
        "assignee": "Samsung SDI Co., Ltd.",
        "filing_date": "2024-03-22",
        "status": "Published",
        "abstract": "A roll-to-roll manufacturing process for producing sulfide-based "
                     "solid electrolyte membranes with thickness below 30 micrometers "
                     "and ionic conductivity above 5 mS/cm.",
    },
]

MOCK_NEWS_RESULTS = [
    {
        "title": "Solid-State Battery Startup Raises $500M Series D",
        "url": "https://techcrunch.com/2026/05/solid-state-startup-series-d",
        "source": "TechCrunch",
        "published": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "snippet": "Solid Power has raised $500M in a Series D round led by BMW i Ventures "
                   "and Ford Motor Company, bringing its total funding to $1.2B.",
    },
    {
        "title": "US DOE Awards $200M for Solid-State Battery Manufacturing Hub",
        "url": "https://energy.gov/articles/solid-state-hub-2026",
        "source": "Department of Energy",
        "published": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "snippet": "The Department of Energy announced a $200M investment to establish a "
                   "national manufacturing hub for solid-state battery technologies in "
                   "Michigan.",
    },
]

MOCK_LENSES = [
    {"name": "academic", "description": "Scholarly papers, preprints, and citations"},
    {"name": "patents", "description": "US/EU/WIPO patent filings and grants"},
    {"name": "news", "description": "Recent news articles (last 30 days)"},
    {"name": "technical", "description": "Technical documentation and specifications"},
    {"name": "regulatory", "description": "Government and regulatory filings"},
]


# ---------------------------------------------------------------------------
# Tool simulators
# ---------------------------------------------------------------------------

def sim_web_search(query: str, provider: str = "brave", max_results: int = 5):
    """Simulate the web_search MCP tool."""
    return {
        "tool": "web_search",
        "query": query,
        "provider": provider,
        "result_count": len(MOCK_WEB_RESULTS),
        "results": MOCK_WEB_RESULTS[:max_results],
    }


def sim_extract_content(url: str):
    """Simulate the extract_content MCP tool."""
    return {
        "tool": "extract_content",
        **MOCK_EXTRACTED_CONTENT,
    }


def sim_academic_search(query: str):
    """Simulate the academic_search MCP tool."""
    return {
        "tool": "academic_search",
        "query": query,
        "result_count": len(MOCK_ACADEMIC_RESULTS),
        "results": MOCK_ACADEMIC_RESULTS,
    }


def sim_patent_search(query: str):
    """Simulate the patent_search MCP tool."""
    return {
        "tool": "patent_search",
        "query": query,
        "result_count": len(MOCK_PATENT_RESULTS),
        "results": MOCK_PATENT_RESULTS,
    }


def sim_news_search(query: str):
    """Simulate the news_search MCP tool."""
    return {
        "tool": "news_search",
        "query": query,
        "result_count": len(MOCK_NEWS_RESULTS),
        "results": MOCK_NEWS_RESULTS,
    }


def sim_search_lenses():
    """Simulate the search_lenses MCP tool."""
    return {
        "tool": "search_lenses",
        "available_lenses": MOCK_LENSES,
    }


# ---------------------------------------------------------------------------
# Pretty printer
# ---------------------------------------------------------------------------

def print_section(title: str):
    width = 70
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_json(data: dict):
    print(json.dumps(data, indent=2, default=str))


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main():
    query = "solid-state battery breakthroughs 2026"

    print_section("web-researcher-mcp  --  Mock Demo")
    print(f"Simulating all 6 MCP tools with query: \"{query}\"")
    print("(No API keys required -- using mock data)\n")

    # 1. web_search
    print_section("1/6  web_search")
    print(f">>> web_search(query=\"{query}\", provider=\"brave\")")
    result = sim_web_search(query)
    print_json(result)

    # 2. extract_content
    url = MOCK_WEB_RESULTS[0]["url"]
    print_section("2/6  extract_content")
    print(f">>> extract_content(url=\"{url}\")")
    result = sim_extract_content(url)
    print_json(result)

    # 3. academic_search
    print_section("3/6  academic_search")
    print(f">>> academic_search(query=\"solid-state electrolyte interfaces\")")
    result = sim_academic_search("solid-state electrolyte interfaces")
    print_json(result)

    # 4. patent_search
    print_section("4/6  patent_search")
    print(f">>> patent_search(query=\"lithium metal anode protection\")")
    result = sim_patent_search("lithium metal anode protection")
    print_json(result)

    # 5. news_search
    print_section("5/6  news_search")
    print(f">>> news_search(query=\"battery technology startups\")")
    result = sim_news_search("battery technology startups")
    print_json(result)

    # 6. search_lenses
    print_section("6/6  search_lenses")
    print(">>> search_lenses()")
    result = sim_search_lenses()
    print_json(result)

    # Summary
    print_section("Demo Complete")
    print("All 6 MCP tools exercised successfully.")
    print()
    print("To use with real data:")
    print("  1. Get a Brave Search API key: https://brave.com/search/api/")
    print("  2. Build the Docker image:  docker build -t web-researcher-mcp .")
    print("  3. Add to Claude:  claude mcp add web-researcher -- \\")
    print("       docker run -i --rm -e BRAVE_API_KEY=<key> web-researcher-mcp")
    print()


if __name__ == "__main__":
    main()
