"""50-state fee data for OTD price calculations."""

# State sales tax rates (state-level only; local rates vary)
STATE_SALES_TAX = {
    "AL": 0.04, "AK": 0.00, "AZ": 0.056, "AR": 0.065, "CA": 0.0725,
    "CO": 0.029, "CT": 0.0635, "DE": 0.00, "FL": 0.06, "GA": 0.04,
    "HI": 0.04, "ID": 0.06, "IL": 0.0625, "IN": 0.07, "IA": 0.06,
    "KS": 0.065, "KY": 0.06, "LA": 0.0445, "ME": 0.055, "MD": 0.06,
    "MA": 0.0625, "MI": 0.06, "MN": 0.0688, "MS": 0.05, "MO": 0.04225,
    "MT": 0.00, "NE": 0.055, "NV": 0.0685, "NH": 0.00, "NJ": 0.06625,
    "NM": 0.05125, "NY": 0.04, "NC": 0.03, "ND": 0.05, "OH": 0.0575,
    "OK": 0.045, "OR": 0.00, "PA": 0.06, "RI": 0.07, "SC": 0.06,
    "SD": 0.045, "TN": 0.07, "TX": 0.0625, "UT": 0.0610, "VT": 0.06,
    "VA": 0.043, "WA": 0.065, "WV": 0.06, "WI": 0.05, "WY": 0.04,
}

# Title + registration fees (approximate flat amounts)
STATE_TITLE_REG = {
    "AL": 23 + 15, "AK": 15 + 100, "AZ": 4 + 32, "AR": 10 + 25, "CA": 23 + 65,
    "CO": 7 + 50, "CT": 25 + 120, "DE": 55 + 40, "FL": 75 + 28, "GA": 18 + 20,
    "HI": 5 + 45, "ID": 14 + 69, "IL": 150 + 151, "IN": 15 + 22, "IA": 25 + 36,
    "KS": 10 + 39, "KY": 9 + 21, "LA": 68 + 20, "ME": 33 + 35, "MD": 100 + 135,
    "MA": 75 + 60, "MI": 15 + 20, "MN": 8 + 35, "MS": 9 + 14, "MO": 8 + 12,
    "MT": 12 + 87, "NE": 10 + 15, "NV": 28 + 33, "NH": 25 + 32, "NJ": 60 + 35,
    "NM": 5 + 27, "NY": 50 + 26, "NC": 56 + 28, "ND": 5 + 49, "OH": 15 + 31,
    "OK": 11 + 96, "OR": 98 + 122, "PA": 53 + 42, "RI": 50 + 30, "SC": 15 + 40,
    "SD": 10 + 36, "TN": 11 + 26, "TX": 33 + 51, "UT": 6 + 44, "VT": 35 + 76,
    "VA": 15 + 40, "WA": 15 + 30, "WV": 15 + 51, "WI": 165 + 85, "WY": 15 + 30,
}

# Doc fee caps (None = no state cap)
STATE_DOC_FEE_CAP = {
    "CA": 85, "CO": 699, "FL": 995, "IL": 324, "MD": 500,
    "NY": 175, "OH": 250, "OR": 150, "TX": 150, "WA": 200,
}

# Common dealer add-ons to watch for
COMMON_ADDONS = [
    ("Nitrogen tire fill", 99, 199, "Decline - air is 78% nitrogen already"),
    ("VIN etching", 150, 400, "Decline - DIY kits cost $25"),
    ("Fabric/paint protection", 299, 999, "Decline - aftermarket products are $30-50"),
    ("Market adjustment/ADM", 500, 5000, "Decline - negotiate or walk away"),
    ("Dealer prep fee", 100, 500, "Decline - this is the dealer's cost of business"),
    ("Window tint", 199, 599, "Decline or negotiate - aftermarket is $150-300"),
    ("LoJack/GPS tracking", 500, 1500, "Decline - your phone does this for free"),
]


def calc_otd(negotiated_price: float, state: str, local_tax_rate: float = 0.0, doc_fee: float = 0.0) -> dict:
    """Calculate out-the-door price for a given state."""
    state = state.upper()
    tax_rate = STATE_SALES_TAX.get(state, 0.06) + local_tax_rate
    sales_tax = negotiated_price * tax_rate
    title_reg = STATE_TITLE_REG.get(state, 100)

    # Cap doc fee if state has a cap
    cap = STATE_DOC_FEE_CAP.get(state)
    if cap and doc_fee > cap:
        doc_fee = cap

    total = negotiated_price + sales_tax + title_reg + doc_fee

    return {
        "negotiated_price": negotiated_price,
        "sales_tax_rate": tax_rate,
        "sales_tax": round(sales_tax, 2),
        "title_reg_fees": title_reg,
        "doc_fee": doc_fee,
        "otd_total": round(total, 2),
        "state": state,
    }
