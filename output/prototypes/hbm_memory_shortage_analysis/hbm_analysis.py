#!/usr/bin/env python3
"""
HBM Memory Shortage & Consumer Electronics Repricing Analysis

Models the wafer capacity tradeoff between HBM (for AI/GPUs) and
DDR/LPDDR (for consumer electronics), showing how HBM's explosive
growth reprices smartphones, laptops, and tablets worldwide.
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional  # noqa: F401


# ── Data Models ──────────────────────────────────────────────────────

@dataclass
class MemoryManufacturer:
    name: str
    total_wafer_capacity_kwpm: float  # thousand wafers per month
    hbm_share_pct: float
    ddr_share_pct: float
    lpddr_share_pct: float


@dataclass
class WaferScenario:
    label: str
    year: int
    hbm_share_pct: float
    ddr_share_pct: float
    lpddr_share_pct: float
    hbm_wafer_intensity: float = 3.2  # GB per wafer-unit vs DDR/LPDDR


@dataclass
class ConsumerImpact:
    segment: str
    baseline_memory_cost_usd: float
    memory_fraction_of_bom: float  # bill of materials
    regions_most_affected: list = field(default_factory=list)


# ── Mock/Reference Data ─────────────────────────────────────────────

MANUFACTURERS = [
    MemoryManufacturer("Samsung", 550, 18.0, 42.0, 40.0),
    MemoryManufacturer("SK Hynix", 420, 25.0, 38.0, 37.0),
    MemoryManufacturer("Micron", 380, 15.0, 45.0, 40.0),
]

SCENARIOS = [
    WaferScenario("Pre-AI Boom (2022)", 2022, 2.0, 50.0, 48.0),
    WaferScenario("Early AI Ramp (2024)", 2024, 8.0, 47.0, 45.0),
    WaferScenario("Current (2025)", 2025, 14.0, 44.0, 42.0),
    WaferScenario("Projected (End 2026)", 2026, 20.0, 40.0, 40.0),
    WaferScenario("High-Demand (2027)", 2027, 28.0, 37.0, 35.0),
]

CONSUMER_SEGMENTS = [
    ConsumerImpact("Sub-$100 Smartphone", 8.0, 0.35, ["Sub-Saharan Africa", "South Asia", "Southeast Asia"]),
    ConsumerImpact("Mid-range Smartphone ($200-400)", 22.0, 0.18, ["Latin America", "Eastern Europe", "India"]),
    ConsumerImpact("Budget Laptop", 35.0, 0.15, ["Global"]),
    ConsumerImpact("Flagship Smartphone ($800+)", 55.0, 0.08, ["Global"]),
    ConsumerImpact("Tablet", 18.0, 0.12, ["Global"]),
]


# ── Analysis Engine ──────────────────────────────────────────────────

def compute_effective_supply_index(scenario: WaferScenario, base: WaferScenario) -> dict:
    """
    Compute how much consumer memory supply shrinks relative to the base scenario.
    HBM consumes more wafer area per GB, so as HBM share grows, effective
    consumer-available memory drops disproportionately.
    """
    base_consumer = base.ddr_share_pct + base.lpddr_share_pct
    current_consumer = scenario.ddr_share_pct + scenario.lpddr_share_pct

    # Effective wafer loss: HBM takes 3.2x more wafer per GB
    hbm_delta = scenario.hbm_share_pct - base.hbm_share_pct
    effective_wafer_loss = hbm_delta * scenario.hbm_wafer_intensity

    supply_index = max(0, (current_consumer / base_consumer) * 100)
    effective_supply_index = max(0, supply_index - effective_wafer_loss)

    return {
        "scenario": scenario.label,
        "year": scenario.year,
        "hbm_share_pct": scenario.hbm_share_pct,
        "consumer_share_pct": round(current_consumer, 1),
        "supply_index": round(supply_index, 1),
        "effective_supply_index": round(effective_supply_index, 1),
        "estimated_price_increase_pct": round(100 - effective_supply_index, 1),
    }


def estimate_segment_impact(segment: ConsumerImpact, price_increase_pct: float) -> dict:
    """
    Estimate how a memory price increase flows through to device BOM and retail price.
    """
    memory_cost_increase = segment.baseline_memory_cost_usd * (price_increase_pct / 100)
    bom_increase = memory_cost_increase
    retail_increase = bom_increase * 1.4  # typical retail markup on BOM delta
    new_memory_cost = segment.baseline_memory_cost_usd + memory_cost_increase
    pct_of_device = segment.memory_fraction_of_bom * 100

    return {
        "segment": segment.segment,
        "baseline_memory_cost_usd": segment.baseline_memory_cost_usd,
        "new_memory_cost_usd": round(new_memory_cost, 2),
        "memory_cost_increase_usd": round(memory_cost_increase, 2),
        "retail_price_increase_usd": round(retail_increase, 2),
        "memory_pct_of_bom": round(pct_of_device, 1),
        "regions_most_affected": segment.regions_most_affected,
    }


def manufacturer_summary() -> list:
    """Summarize current manufacturer allocations."""
    results = []
    for m in MANUFACTURERS:
        total_consumer = m.ddr_share_pct + m.lpddr_share_pct
        results.append({
            "manufacturer": m.name,
            "capacity_kwpm": m.total_wafer_capacity_kwpm,
            "hbm_pct": m.hbm_share_pct,
            "ddr_pct": m.ddr_share_pct,
            "lpddr_pct": m.lpddr_share_pct,
            "consumer_total_pct": round(total_consumer, 1),
        })
    return results


def run_full_analysis(output_json: bool = False) -> dict:
    """Run the complete HBM shortage analysis."""
    base = SCENARIOS[0]  # Pre-AI Boom baseline

    supply_analysis = [compute_effective_supply_index(s, base) for s in SCENARIOS]

    # Use projected 2026 scenario for consumer impact
    projected_2026 = next(r for r in supply_analysis if r["year"] == 2026)
    price_increase = projected_2026["estimated_price_increase_pct"]

    segment_impacts = [estimate_segment_impact(seg, price_increase) for seg in CONSUMER_SEGMENTS]

    manufacturers = manufacturer_summary()

    result = {
        "title": "HBM Memory Shortage & Consumer Electronics Repricing Analysis",
        "source": "https://simonwillison.net/2026/May/22/memory-shortage/",
        "original_article": "https://davidoks.blog/p/ai-is-killing-the-cheap-smartphone",
        "key_finding": (
            f"By end of 2026, HBM is projected to consume ~20% of memory wafer capacity "
            f"(up from ~2% in 2022). Due to HBM's {base.hbm_wafer_intensity}x wafer intensity, "
            f"this effectively reduces consumer memory supply by ~{price_increase:.0f}%, "
            f"hitting sub-$100 smartphones in Africa and South Asia hardest."
        ),
        "manufacturers": manufacturers,
        "supply_trajectory": supply_analysis,
        "consumer_segment_impacts": segment_impacts,
        "equity_implications": {
            "most_vulnerable": "Sub-$100 smartphone market in Sub-Saharan Africa and South Asia",
            "mechanism": "Memory is ~35% of BOM for cheapest smartphones; price increases are not absorbable",
            "digital_divide_risk": "Rising device costs may slow smartphone adoption in emerging markets, "
                                   "widening the digital divide just as mobile internet becomes essential infrastructure",
        },
    }

    return result


# ── Display ──────────────────────────────────────────────────────────

def print_divider(title: str = ""):
    width = 72
    if title:
        padding = (width - len(title) - 2) // 2
        print(f"\n{'=' * padding} {title} {'=' * padding}")
    else:
        print("=" * width)


def display_results(result: dict):
    print_divider("HBM MEMORY SHORTAGE ANALYSIS")
    print(f"\n  {result['key_finding']}\n")

    # Manufacturer table
    print_divider("MANUFACTURER WAFER ALLOCATION (Current)")
    print(f"  {'Manufacturer':<12} {'Capacity':>10} {'HBM':>6} {'DDR':>6} {'LPDDR':>7} {'Consumer':>10}")
    print(f"  {'-'*12} {'-'*10} {'-'*6} {'-'*6} {'-'*7} {'-'*10}")
    for m in result["manufacturers"]:
        print(f"  {m['manufacturer']:<12} {m['capacity_kwpm']:>10.0f} {m['hbm_pct']:>5.1f}% {m['ddr_pct']:>5.1f}% {m['lpddr_pct']:>6.1f}% {m['consumer_total_pct']:>9.1f}%")

    # Supply trajectory
    print_divider("WAFER SUPPLY TRAJECTORY")
    print(f"  {'Scenario':<24} {'HBM%':>6} {'Consumer%':>10} {'Supply':>8} {'Eff.Supply':>11} {'Price+':>8}")
    print(f"  {'-'*24} {'-'*6} {'-'*10} {'-'*8} {'-'*11} {'-'*8}")
    for s in result["supply_trajectory"]:
        marker = " <--" if s["year"] == 2026 else ""
        print(f"  {s['scenario']:<24} {s['hbm_share_pct']:>5.1f}% {s['consumer_share_pct']:>9.1f}% {s['supply_index']:>7.1f} {s['effective_supply_index']:>10.1f} {s['estimated_price_increase_pct']:>7.1f}%{marker}")

    # Consumer segment impacts
    print_divider("CONSUMER SEGMENT IMPACT (Projected End 2026)")
    print(f"  {'Segment':<28} {'Mem Cost':>9} {'New Cost':>9} {'Increase':>9} {'Retail+':>8} {'Mem%BOM':>8}")
    print(f"  {'-'*28} {'-'*9} {'-'*9} {'-'*9} {'-'*8} {'-'*8}")
    for seg in result["consumer_segment_impacts"]:
        print(f"  {seg['segment']:<28} ${seg['baseline_memory_cost_usd']:>7.2f} ${seg['new_memory_cost_usd']:>7.2f} ${seg['memory_cost_increase_usd']:>7.2f} ${seg['retail_price_increase_usd']:>6.2f} {seg['memory_pct_of_bom']:>6.1f}%")
        if seg["regions_most_affected"]:
            print(f"  {'':28} Regions: {', '.join(seg['regions_most_affected'])}")

    # Equity implications
    print_divider("EQUITY & DIGITAL DIVIDE IMPLICATIONS")
    eq = result["equity_implications"]
    print(f"\n  Most vulnerable: {eq['most_vulnerable']}")
    print(f"  Mechanism:       {eq['mechanism']}")
    print(f"  Risk:            {eq['digital_divide_risk']}\n")

    print_divider()


def main():
    output_json = "--json" in sys.argv

    result = run_full_analysis()

    if output_json:
        print(json.dumps(result, indent=2))
    else:
        display_results(result)

    return result


if __name__ == "__main__":
    main()
