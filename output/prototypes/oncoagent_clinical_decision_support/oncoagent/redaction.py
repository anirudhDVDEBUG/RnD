"""Zero-PHI redaction layer — strips protected health information before processing."""

import re

# Patterns for common PHI elements
PHI_PATTERNS = [
    (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[REDACTED_NAME]"),       # Full names
    (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),               # SSN
    (r"\b\d{2}/\d{2}/\d{4}\b", "[REDACTED_DATE]"),              # Dates MM/DD/YYYY
    (r"\b\d{4}-\d{2}-\d{2}\b", "[REDACTED_DATE]"),              # Dates YYYY-MM-DD
    (r"\bMRN[:\s]*\d+\b", "[REDACTED_MRN]"),                    # Medical Record Numbers
    (r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]"), # Phone numbers
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]"),
]

# Medical terms to preserve (not redact even if they match name patterns)
PRESERVE_TERMS = {
    "Non Small", "Small Cell", "Stage IV", "Stage III", "Stage II", "Stage I",
    "Phase II", "Phase III", "First Line", "Second Line", "Third Line",
    "Eastern Cooperative", "World Health", "National Comprehensive",
}


def redact_phi(text: str) -> str:
    """Remove PHI from clinical text while preserving medical terminology."""
    result = text
    for pattern, replacement in PHI_PATTERNS:
        matches = list(re.finditer(pattern, result))
        for match in reversed(matches):
            matched_text = match.group()
            if matched_text in PRESERVE_TERMS:
                continue
            result = result[:match.start()] + replacement + result[match.end():]
    return result
