"""1688 sourcing evaluator — compares suppliers, calculates landed costs and margins."""

import argparse
import sys

from . import mock_data
from .utils import format_currency

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def evaluate_sourcing(product: str) -> None:
    suppliers = mock_data.SUPPLIERS_1688.get(product)
    if not suppliers:
        print(f"No supplier data for '{product}'. Available: {', '.join(mock_data.SUPPLIERS_1688.keys())}")
        sys.exit(1)

    rates = mock_data.SHIPPING_RATES
    sell_price = mock_data.LISTINGS["B0EXAMPLE01"]["price"]

    print(f"\n{'='*60}")
    print(f"  1688 SOURCING EVALUATOR")
    print(f"{'='*60}")
    print(f"\n  Product: {product}")
    print(f"  Amazon sell price: ${sell_price}")
    print(f"  Exchange rate: 1 RMB = ${rates['rmb_to_usd']}")

    # Score and rank suppliers
    scored = []
    for s in suppliers:
        supplier_score = calculate_supplier_score(s)
        landed = calculate_landed_cost(s, rates)
        referral_fee = sell_price * rates["referral_pct"]
        fba_fee = rates["fba_fee_standard"]
        total_cost = landed + referral_fee + fba_fee
        margin = sell_price - total_cost
        margin_pct = margin / sell_price * 100

        scored.append({
            **s,
            "score": supplier_score,
            "landed_cost": landed,
            "total_cost": total_cost,
            "margin": margin,
            "margin_pct": margin_pct,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    # Supplier comparison table
    print(f"\n--- SUPPLIER COMPARISON ---")
    if tabulate:
        table = []
        for i, s in enumerate(scored, 1):
            table.append([
                f"{'>>>' if i == 1 else '   '} {i}",
                s["name"],
                f"\u00a5{s['price_rmb']}",
                s["moq"],
                f"{s['rating']}\u2605",
                f"{s['years']}yr",
                f"${s['landed_cost']:.2f}",
                f"{s['margin_pct']:.1f}%",
                f"{s['score']:.0f}/100",
            ])
        print(tabulate(table,
                       headers=["", "Supplier", "Price", "MOQ", "Rating", "Exp", "Landed", "Margin", "Score"],
                       tablefmt="simple"))
    else:
        for i, s in enumerate(scored, 1):
            marker = ">>>" if i == 1 else "   "
            print(f"  {marker} {i}. {s['name']} ({s['name_en']})")
            print(f"       Price: \u00a5{s['price_rmb']}  MOQ: {s['moq']}  Rating: {s['rating']}\u2605  Exp: {s['years']}yr")
            print(f"       Landed: ${s['landed_cost']:.2f}  Margin: {s['margin_pct']:.1f}%  Score: {s['score']:.0f}/100")

    # Detailed cost breakdown for top supplier
    top = scored[0]
    print(f"\n--- COST BREAKDOWN (Top Supplier: {top['name_en']}) ---")
    unit_cost_usd = top["price_rmb"] * rates["rmb_to_usd"]
    shipping_cost = rates["sea_freight_per_kg"] * rates["product_weight_kg"]
    duty = unit_cost_usd * rates["import_duty_pct"]
    referral = sell_price * rates["referral_pct"]
    fba = rates["fba_fee_standard"]

    print(f"  Product cost:    \u00a5{top['price_rmb']:<8} = ${unit_cost_usd:.2f}")
    print(f"  Sea freight:     {rates['product_weight_kg']}kg x ${rates['sea_freight_per_kg']}/kg = ${shipping_cost:.2f}")
    print(f"  Import duty:     {rates['import_duty_pct']*100:.1f}% = ${duty:.2f}")
    print(f"  ---")
    print(f"  Landed cost:                    ${top['landed_cost']:.2f}")
    print(f"  Amazon referral: {rates['referral_pct']*100:.0f}%            = ${referral:.2f}")
    print(f"  FBA fulfillment:                ${fba:.2f}")
    print(f"  ---")
    print(f"  Total cost:                     ${top['total_cost']:.2f}")
    print(f"  Sell price:                     ${sell_price:.2f}")
    print(f"  NET MARGIN:                     ${top['margin']:.2f} ({top['margin_pct']:.1f}%)")

    # Recommendations
    print(f"\n--- SOURCING RECOMMENDATIONS ---")
    print(f"  1. Top pick: {top['name_en']} — best overall score ({top['score']:.0f}/100)")
    print(f"  2. MOQ: {top['moq']} units  |  First order cost: ${top['price_rmb'] * top['moq'] * rates['rmb_to_usd']:,.2f}")
    print(f"  3. Production lead time: {top['production_days']} days + ~25 days sea freight")
    print(f"  4. Certifications: {', '.join(top['certifications'])}")
    if top["customization"]:
        print(f"  5. Custom branding/packaging available — request samples before bulk order")
    print()


def calculate_supplier_score(supplier: dict) -> float:
    score = 0.0
    score += supplier["rating"] * 10           # max 50
    score += min(supplier["years"], 10) * 2    # max 20
    score += supplier["response_rate"] * 15    # max 15
    score += len(supplier["certifications"]) * 3  # variable
    if supplier["customization"]:
        score += 5
    if supplier["moq"] <= 500:
        score += 5
    elif supplier["moq"] <= 1000:
        score += 2
    return min(100, score)


def calculate_landed_cost(supplier: dict, rates: dict) -> float:
    unit_cost_usd = supplier["price_rmb"] * rates["rmb_to_usd"]
    shipping = rates["sea_freight_per_kg"] * rates["product_weight_kg"]
    duty = unit_cost_usd * rates["import_duty_pct"]
    return unit_cost_usd + shipping + duty


def main():
    parser = argparse.ArgumentParser(description="1688 Sourcing Evaluator")
    parser.add_argument("--product", default="stainless steel bottle", help="Product to source")
    args = parser.parse_args()
    evaluate_sourcing(args.product)


if __name__ == "__main__":
    main()
