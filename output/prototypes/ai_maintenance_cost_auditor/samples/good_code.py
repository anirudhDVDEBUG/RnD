"""Order processing module — clean AI-generated example."""


def calculate_order_total(items: list[dict], tax_rate: float = 0.08) -> float:
    """Calculate the total cost of an order including tax."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * tax_rate
    return round(subtotal + tax, 2)


def apply_discount(total: float, discount_pct: float) -> float:
    """Apply a percentage discount, clamped to [0, 100]."""
    discount_pct = max(0.0, min(discount_pct, 100.0))
    return round(total * (1 - discount_pct / 100), 2)


def format_receipt(items: list[dict], tax_rate: float = 0.08,
                   discount_pct: float = 0.0) -> str:
    """Return a human-readable receipt string."""
    lines = ["--- RECEIPT ---"]
    for item in items:
        line_total = item["price"] * item["quantity"]
        lines.append(f"  {item['name']:20s}  x{item['quantity']}  ${line_total:.2f}")

    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    if discount_pct > 0:
        total = apply_discount(total, discount_pct)
        lines.append(f"  {'Discount':20s}         -{discount_pct}%")

    lines.append(f"  {'Subtotal':20s}         ${subtotal:.2f}")
    lines.append(f"  {'Tax':20s}         ${tax:.2f}")
    lines.append(f"  {'TOTAL':20s}         ${total:.2f}")
    lines.append("--- END ---")
    return "\n".join(lines)
