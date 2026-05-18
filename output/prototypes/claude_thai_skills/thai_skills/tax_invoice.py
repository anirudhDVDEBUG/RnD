"""Thai tax invoice (ใบกำกับภาษี) formatter per Revenue Department standards."""

from datetime import date
from .buddhist_era import format_thai_date


VAT_RATE = 0.07  # 7% standard Thai VAT


def format_baht(amount: float) -> str:
    """Format amount in Thai Baht with satang."""
    whole = int(amount)
    satang = round((amount - whole) * 100)
    if satang == 0:
        return f"฿{whole:,.0f}.00"
    return f"฿{whole:,.0f}.{satang:02d}"


def baht_text(amount: float) -> str:
    """Convert amount to Thai text representation (simplified)."""
    thai_digits = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    thai_units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

    whole = int(amount)
    satang = round((amount - whole) * 100)

    if whole == 0:
        result = "ศูนย์บาท"
    else:
        result = ""
        digits = str(whole)
        length = len(digits)
        for i, d in enumerate(digits):
            pos = length - i - 1
            d_int = int(d)
            if d_int == 0:
                continue
            if pos == 1 and d_int == 1:
                result += "สิบ"
            elif pos == 1 and d_int == 2:
                result += "ยี่สิบ"
            elif pos == 0 and d_int == 1 and length > 1:
                result += "เอ็ด"
            else:
                result += thai_digits[d_int] + thai_units[pos]
        result += "บาท"

    if satang == 0:
        result += "ถ้วน"
    else:
        s_digits = str(satang).zfill(2)
        for i, d in enumerate(s_digits):
            pos = 1 - i
            d_int = int(d)
            if d_int == 0:
                continue
            if pos == 1 and d_int == 1:
                result += "สิบ"
            elif pos == 1 and d_int == 2:
                result += "ยี่สิบ"
            elif pos == 0 and d_int == 1 and int(s_digits[0]) > 0:
                result += "เอ็ด"
            else:
                result += thai_digits[d_int] + thai_units[pos]
        result += "สตางค์"

    return result


def generate_tax_invoice(
    seller_name: str,
    seller_tax_id: str,
    buyer_name: str,
    buyer_tax_id: str,
    items: list,
    invoice_number: str = "INV-001",
    invoice_date: date = None,
) -> dict:
    """Generate a Thai tax invoice.

    Args:
        items: List of dicts with keys: description, quantity, unit_price
    """
    if invoice_date is None:
        invoice_date = date.today()

    # Calculate totals
    line_items = []
    subtotal = 0.0
    for item in items:
        line_total = item["quantity"] * item["unit_price"]
        subtotal += line_total
        line_items.append({
            "description": item["description"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "total": line_total,
            "total_formatted": format_baht(line_total),
        })

    vat_amount = subtotal * VAT_RATE
    grand_total = subtotal + vat_amount

    return {
        "title": "ใบกำกับภาษี / Tax Invoice",
        "invoice_number": invoice_number,
        "date_thai": format_thai_date(invoice_date),
        "date_ce": invoice_date.isoformat(),
        "seller": {"name": seller_name, "tax_id": seller_tax_id},
        "buyer": {"name": buyer_name, "tax_id": buyer_tax_id},
        "items": line_items,
        "subtotal": format_baht(subtotal),
        "vat_rate": "7%",
        "vat_amount": format_baht(vat_amount),
        "grand_total": format_baht(grand_total),
        "grand_total_text": baht_text(grand_total),
        "raw_totals": {
            "subtotal": subtotal,
            "vat": vat_amount,
            "grand_total": grand_total,
        }
    }
