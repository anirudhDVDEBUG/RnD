"""PromptPay EMVCo QR payload generator per Bank of Thailand spec."""

import binascii
import struct


def _crc16_ccitt(data: bytes) -> str:
    """CRC-16/CCITT-FALSE used by EMVCo."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')


def _tlv(tag: str, value: str) -> str:
    """Create a TLV (Tag-Length-Value) field."""
    return f"{tag}{len(value):02d}{value}"


def _format_phone(phone: str) -> str:
    """Convert Thai phone (08x, 09x, 06x) to international format."""
    clean = phone.replace("-", "").replace(" ", "")
    if clean.startswith("0") and len(clean) == 10:
        return "0066" + clean[1:]  # Country code 66, prepend 00
    return clean


def generate_promptpay_payload(target: str, amount: float = None) -> dict:
    """Generate PromptPay EMVCo QR payload.

    Args:
        target: Phone number (10 digits) or National ID (13 digits)
        amount: Payment amount in Baht (None for open amount)

    Returns:
        Dict with payload string and field breakdown.
    """
    clean_target = target.replace("-", "").replace(" ", "")

    # Determine if phone or national ID
    if len(clean_target) == 13:
        aid_tag = "02"  # National ID
        formatted_id = clean_target
    else:
        aid_tag = "01"  # Phone number
        formatted_id = _format_phone(clean_target)

    # Build payload
    fields = []

    # Tag 00: Payload Format Indicator
    fields.append(_tlv("00", "01"))

    # Tag 01: Point of Initiation (11=static, 12=dynamic)
    fields.append(_tlv("01", "12" if amount else "11"))

    # Tag 29: Merchant Account Info (PromptPay)
    promptpay_aid = "A000000677010111"  # PromptPay AID
    merchant_data = _tlv("00", promptpay_aid) + _tlv(aid_tag, formatted_id)
    fields.append(_tlv("29", merchant_data))

    # Tag 53: Transaction Currency (764 = THB)
    fields.append(_tlv("53", "764"))

    # Tag 54: Transaction Amount (if specified)
    if amount is not None:
        amount_str = f"{amount:.2f}"
        fields.append(_tlv("54", amount_str))

    # Tag 58: Country Code
    fields.append(_tlv("58", "TH"))

    # Tag 63: CRC (placeholder, will be calculated)
    payload_without_crc = "".join(fields) + "6304"
    crc = _crc16_ccitt(payload_without_crc.encode('ascii'))

    full_payload = payload_without_crc + crc

    return {
        "payload": full_payload,
        "target": clean_target,
        "target_type": "National ID" if len(clean_target) == 13 else "Phone",
        "amount": amount,
        "currency": "THB",
        "crc": crc,
    }
