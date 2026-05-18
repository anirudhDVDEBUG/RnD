"""Thai address formatting per postal conventions."""


def format_thai_address(
    house_number: str = "",
    village: str = "",
    soi: str = "",
    road: str = "",
    sub_district: str = "",
    district: str = "",
    province: str = "",
    postal_code: str = "",
    is_bangkok: bool = False,
) -> dict:
    """Format a Thai address following postal conventions.

    Bangkok uses แขวง/เขต/กรุงเทพมหานคร.
    Other provinces use ตำบล/อำเภอ/จังหวัด.
    """
    lines = []

    # Line 1: House number, village, soi, road
    line1_parts = []
    if house_number:
        line1_parts.append(house_number)
    if village:
        line1_parts.append(f"หมู่บ้าน{village}")
    if soi:
        line1_parts.append(f"ซอย{soi}")
    if road:
        line1_parts.append(f"ถนน{road}")
    if line1_parts:
        lines.append(" ".join(line1_parts))

    # Line 2: Sub-district, district
    line2_parts = []
    if is_bangkok:
        if sub_district:
            line2_parts.append(f"แขวง{sub_district}")
        if district:
            line2_parts.append(f"เขต{district}")
    else:
        if sub_district:
            line2_parts.append(f"ตำบล{sub_district}")
        if district:
            line2_parts.append(f"อำเภอ{district}")
    if line2_parts:
        lines.append(" ".join(line2_parts))

    # Line 3: Province and postal code
    line3_parts = []
    if is_bangkok:
        line3_parts.append("กรุงเทพมหานคร")
    elif province:
        line3_parts.append(f"จังหวัด{province}")
    if postal_code:
        line3_parts.append(postal_code)
    if line3_parts:
        lines.append(" ".join(line3_parts))

    formatted = "\n".join(lines)

    return {
        "formatted": formatted,
        "lines": lines,
        "is_bangkok": is_bangkok,
    }
