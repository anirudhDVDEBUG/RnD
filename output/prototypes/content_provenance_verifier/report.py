"""Pretty-print provenance verification reports."""

from models import VerificationResult
from source_types import classify_source_type


def format_report(result: VerificationResult) -> str:
    """Format a single verification result as a bordered table."""
    import os
    filename = os.path.basename(result.file_path)

    if result.error:
        return _box([
            ("File", filename),
            ("Error", result.error),
        ])

    if not result.has_credentials:
        return _box([
            ("File", filename),
            ("C2PA Status", "UNSIGNED — No Content Credentials found"),
            ("Source Type", "Unknown"),
            ("Trust", "NONE — Cannot verify provenance"),
        ])

    # Build source type label
    st_label = "Unknown"
    if result.source_type:
        info = classify_source_type(result.source_type)
        ai_tag = " (AI-generated)" if info["is_ai"] else ""
        st_label = f"{result.source_type}{ai_tag}"

    trust_labels = {
        "VERIFIED": "VERIFIED — signature chain valid",
        "INVALID": "INVALID — signature mismatch",
        "NONE": "NONE — no signature present",
    }

    return _box([
        ("File", filename),
        ("C2PA Status", "SIGNED — Content Credentials found"),
        ("Source Type", st_label),
        ("Generator", result.generator or "Unknown"),
        ("Trust", trust_labels.get(result.trust_status, result.trust_status)),
    ])


def format_summary(results: list[VerificationResult]) -> str:
    """Format a summary of multiple verification results."""
    total = len(results)
    signed = sum(1 for r in results if r.has_credentials)
    ai = sum(1 for r in results if r.is_ai_generated)
    verified = sum(1 for r in results if r.trust_status == "VERIFIED")

    lines = [
        "",
        "=== PROVENANCE SUMMARY ===",
        f"  Files scanned:    {total}",
        f"  With credentials: {signed}/{total}",
        f"  AI-generated:     {ai}/{total}",
        f"  Verified sigs:    {verified}/{total}",
        "=" * 27,
    ]
    return "\n".join(lines)


def _box(rows: list[tuple[str, str]]) -> str:
    """Draw a simple bordered table."""
    key_width = max(len(k) for k, _ in rows)
    val_width = max(len(v) for _, v in rows)
    inner = key_width + 3 + val_width
    top = f"\u250c{'─' * (inner + 2)}\u2510"
    bot = f"\u2514{'─' * (inner + 2)}\u2518"
    sep = f"\u251c{'─' * (key_width + 2)}\u252c{'─' * (val_width + 2)}\u2524"

    lines = [top]
    lines.append(f"\u2502 {'Content Provenance Report':^{inner}} \u2502")
    lines.append(sep)
    for key, val in rows:
        lines.append(f"\u2502 {key:<{key_width}} \u2502 {val:<{val_width}} \u2502")
    lines.append(bot)
    return "\n".join(lines)
