# Technical Details — Content Provenance Verifier

## What it does

Content Provenance Verifier reads, validates, and reports on C2PA Content
Credentials embedded in media files. It extracts the cryptographic manifest
store, parses assertions (especially `c2pa.actions` with IPTC digital source
types), checks signature validity, and produces a structured trust verdict:
is this file AI-generated, camera-captured, or edited — and can you trust
that label?

This matters because OpenAI, Google, Adobe, and Microsoft now embed Content
Credentials in AI-generated images by default (DALL-E, Imagen, Firefly).
The C2PA standard is the dominant open format for this, backed by the
Coalition for Content Provenance and Authenticity (800+ members). SynthID
adds an invisible watermark layer on top. This tool handles the C2PA side.

## Architecture

```
verifier.py          — Core verification engine. Reads manifests, validates
                       signatures, classifies digital source type.
signer.py            — Signs files with Content Credentials (demo/mock mode).
models.py            — Data classes: VerificationResult, Manifest, Assertion.
source_types.py      — IPTC digital source type vocabulary + classification.
report.py            — Pretty-prints provenance reports to terminal.
samples/             — Mock C2PA manifest JSON files for demo purposes.
run.sh               — End-to-end demo script.
```

### Data flow

```
Input file → Read C2PA manifest (JUMBF box / XMP) → Parse assertions
→ Extract digitalSourceType → Validate signature chain → Classify
→ VerificationResult { has_credentials, source_type, is_ai_generated,
                        generator, trust_status, assertions[] }
→ Report (table or JSON)
```

### Dependencies

- Python 3.8+
- `dataclasses` (stdlib)
- `json` (stdlib)
- `hashlib` (stdlib for mock signature verification)
- Optional: `c2pa-python` for real manifest reading from actual image files

No external API keys. No network calls. The demo uses JSON manifest fixtures
that mirror real C2PA manifest store structures.

## Limitations

- **Demo mode only reads mock JSON manifests**, not actual JUMBF boxes from
  real JPEGs/PNGs. Install `c2pa-python` and use `Reader.from_file()` for
  real files.
- **SynthID detection is not implemented** — Google's SynthID is not publicly
  available as a detection library. This tool notes its existence but cannot
  read SynthID watermarks.
- **Signature verification is simulated** using SHA-256 hash checks against
  the mock manifest. Real verification requires the C2PA trust list and
  certificate chain validation.
- Does not handle video files (C2PA supports them, but the Python SDK
  support is limited).

## Why this matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Ad creatives** | Platforms increasingly require provenance labels on AI-generated ads. This tool lets you verify compliance before upload. |
| **Lead-gen / marketing** | AI-generated landing page images need Content Credentials to avoid platform penalties (Meta, Google Ads policies tightening in 2025-2026). |
| **Agent factories** | Agents that generate or process images should attach provenance metadata automatically — this skill teaches Claude how. |
| **Content moderation** | Verify whether user-uploaded media is AI-generated before publishing. |
| **Voice AI** | Audio C2PA credentials are emerging (SynthID for audio); the same verification patterns apply. |

## Key references

- [C2PA Specification v2.1](https://c2pa.org/specifications/)
- [c2pa-python SDK](https://github.com/contentauth/c2pa-python)
- [OpenAI: Advancing content provenance](https://openai.com/index/advancing-content-provenance)
- [IPTC Digital Source Type vocabulary](https://cv.iptc.org/newscodes/digitalsourcetype/)
