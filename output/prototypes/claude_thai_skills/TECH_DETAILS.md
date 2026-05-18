# Technical Details: Claude Thai Skills

## What It Actually Does

This is a Claude Code skill pack (prompt-based) paired with reference Python implementations of the algorithmic components. The skill definitions guide Claude's behavior when users ask Thailand-specific questions — translation, legal compliance, financial formatting, and identity validation. The Python code provides deterministic implementations for skills that require exact computation (ID checksums, date math, EMVCo payloads) rather than relying on LLM generation.

The 12 skills split into two categories: **generative** (translation, captions, resumes, government letters, PDPA docs, LINE messages) where Claude's language model does the work guided by Thai-specific prompts, and **algorithmic** (National ID validation, Buddhist Era dates, PromptPay QR, tax invoice math, address formatting, NLP segmentation) where deterministic code produces correct outputs.

## Architecture

### Skill Layer (Prompt-based)
- `SKILL.md` files in `~/.claude/skills/claude_thai_skills/` define trigger conditions and output formats
- Claude Code's skill system pattern-matches user input against trigger phrases
- Generative skills rely on Claude's Thai language capability + formatting constraints

### Implementation Layer (Python)
- `thai_skills/national_id.py` — Modulo-11 checksum per Ministry of Interior spec
- `thai_skills/buddhist_era.py` — CE+543=BE conversion, Thai month names, day-of-week lookup
- `thai_skills/promptpay.py` — EMVCo TLV encoding: merchant ID (tag 00), PromptPay AID (tag 29), amount (tag 54), CRC-16 (tag 63)
- `thai_skills/tax_invoice.py` — 7% VAT calculation, Thai Baht formatting with satang, bilingual field labels
- `thai_skills/address.py` — Hierarchical formatter: house number > soi > road > sub-district > district > province > postal code
- `thai_skills/nlp.py` — Dictionary-based maximal matching word segmentation (no ML model needed)
- `thai_skills/pdpa.py` — Template-based PDPA notice generation with configurable data categories

### Data Flow
```
User prompt → Claude Code skill trigger →
  If generative: Claude generates Thai text following skill constraints
  If algorithmic: Python function computes exact result → formatted output
```

### Dependencies
- Python 3.8+ (standard library only for core functions)
- No external API keys required
- No ML models to download
- Optional: `pythainlp` for production-grade NLP (demo uses built-in dictionary)

## Limitations

- **NLP segmentation** uses a basic dictionary (~3000 common words). Production use should swap in PyThaiNLP or similar.
- **PDPA templates** are informational — not legal advice. Must be reviewed by Thai legal counsel.
- **PromptPay QR** generates the payload string but not the actual QR image (use any QR library to render).
- **Translation** quality depends on Claude's Thai training data — handles formal/informal registers but may miss very regional dialects.
- **Tax invoice** formatting follows standard rules but doesn't handle all edge cases (e.g., partial credits, multi-branch scenarios).
- **No offline dictionary for all Thai words** — the bundled segmentation handles common text but not specialized jargon.

## Why This Matters

### For Claude-driven products:
- **Lead-gen / Marketing in Thailand:** Instant Thai caption generation, LINE OA message drafting, and address formatting for Thai CRM data.
- **Agent factories:** Drop-in Thai localization layer — any agent serving Thai users gets PDPA compliance, proper date formatting, and payment integration for free.
- **Ad creatives:** Thai social media captions with platform-appropriate hashtags and tone.
- **Voice AI:** Buddhist Era dates and Thai address formatting are critical for any voice assistant serving Thai users (dates spoken as "พ.ศ. 2569" not "2026").
- **Fintech:** PromptPay payload generation is table-stakes for any payment integration in Thailand (90%+ smartphone penetration, PromptPay is the national payment rail).

### Market context:
Thailand has 70M+ population, high smartphone adoption, and mandatory PDPA compliance since June 2022. Any AI product targeting Thai SMEs needs these capabilities.
