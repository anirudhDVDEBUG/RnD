# Claude Thai Skills — 12 Thai Localization Skills for Claude Code

**TL;DR:** Drop-in Claude Code skill pack that gives Claude native fluency in Thai workflows — from PDPA compliance docs and tax invoices to PromptPay QR generation and Buddhist Era date conversion. 12 skills, zero API keys, works offline.

## Headline Result

```
Input:  "Validate Thai ID 1100600255911"
Output: Valid: true | Checksum verified (mod-11) | Province prefix: Bangkok
        Formatted: 1-1006-00255-91-1

Input:  "Convert 2026-05-18 to Thai date"
Output: 18 พฤษภาคม พ.ศ. 2569 (วันจันทร์)
```

## Quick Links

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Install in 30 seconds, trigger phrases, first 60 seconds walkthrough
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture, data flow, limitations, business relevance
- [run.sh](./run.sh) — Run `bash run.sh` for a full demo (no API keys needed)

## What's Inside

| Skill | Use Case |
|-------|----------|
| Translation | Context-aware Thai/English translation |
| Captions | Thai social media posts with hashtags |
| Resume | Thai-format CV generation |
| Government Letters | Formal Thai correspondence |
| PDPA Compliance | Privacy notices per Thai law |
| Tax Invoice | VAT invoices per Revenue Dept standards |
| PromptPay | QR payment payload generation |
| National ID | 13-digit ID validation (mod-11) |
| Buddhist Era Dates | CE/BE conversion + Thai formatting |
| LINE OA | Flex Messages for Thai business |
| Address Formatting | Thai postal address structure |
| Thai NLP | Word segmentation (no-space language) |

## Source

[Boom-Vitt/claude-thai-skills](https://github.com/Boom-Vitt/claude-thai-skills) — MIT License
