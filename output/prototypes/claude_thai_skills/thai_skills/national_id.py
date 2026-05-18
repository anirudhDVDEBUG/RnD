"""Thai National ID validation using modulo-11 checksum."""


def validate_thai_id(id_number: str) -> dict:
    """Validate a 13-digit Thai National ID number.

    Returns dict with validity status and details.
    """
    clean = id_number.replace("-", "").replace(" ", "")

    if len(clean) != 13 or not clean.isdigit():
        return {"valid": False, "error": "Must be exactly 13 digits"}

    # Modulo-11 checksum (Ministry of Interior algorithm)
    total = sum(int(clean[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10

    valid = check == int(clean[12])

    return {
        "valid": valid,
        "formatted": format_thai_id(clean),
        "checksum_expected": check,
        "checksum_actual": int(clean[12]),
    }


def format_thai_id(id_number: str) -> str:
    """Format as X-XXXX-XXXXX-XX-X."""
    clean = id_number.replace("-", "").replace(" ", "")
    if len(clean) != 13:
        return id_number
    return f"{clean[0]}-{clean[1:5]}-{clean[5:10]}-{clean[10:12]}-{clean[12]}"
