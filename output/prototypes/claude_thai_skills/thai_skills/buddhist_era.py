"""Buddhist Era (พ.ศ.) date conversion and Thai date formatting."""

from datetime import date, datetime

THAI_MONTHS = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

THAI_DAYS = [
    "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี",
    "วันศุกร์", "วันเสาร์", "วันอาทิตย์"
]

THAI_MONTHS_ABBR = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.",
    "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.",
    "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]


def to_buddhist_era(ce_year: int) -> int:
    """Convert Christian Era year to Buddhist Era (พ.ศ.)."""
    return ce_year + 543


def to_christian_era(be_year: int) -> int:
    """Convert Buddhist Era (พ.ศ.) year to Christian Era."""
    return be_year - 543


def format_thai_date(d: date, abbreviated: bool = False) -> str:
    """Format a date in Thai with Buddhist Era year.

    Example: 18 พฤษภาคม พ.ศ. 2569 (วันจันทร์)
    """
    be_year = to_buddhist_era(d.year)
    month_name = THAI_MONTHS_ABBR[d.month - 1] if abbreviated else THAI_MONTHS[d.month - 1]
    day_name = THAI_DAYS[d.weekday()]

    return f"{d.day} {month_name} พ.ศ. {be_year} ({day_name})"


def parse_thai_date_string(date_str: str) -> dict:
    """Parse a date string and return both CE and BE representations."""
    if isinstance(date_str, str):
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        d = date_str

    return {
        "ce_date": d.isoformat(),
        "be_year": to_buddhist_era(d.year),
        "thai_formatted": format_thai_date(d),
        "thai_abbreviated": format_thai_date(d, abbreviated=True),
    }
