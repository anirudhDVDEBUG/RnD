# Content Provenance Verifier

**Verify whether images carry C2PA Content Credentials and detect AI-generation signals — from the command line or as a Claude Code skill.**

Run `bash run.sh` to see a full verification report on sample images, showing Content Credentials extraction, digital-source-type classification, and a trust summary — no API keys required.

---

| What | Where |
|------|-------|
| How to install & use | [HOW_TO_USE.md](HOW_TO_USE.md) |
| Architecture & technical details | [TECH_DETAILS.md](TECH_DETAILS.md) |
| Quick demo | `bash run.sh` |

### Headline result

```
$ bash run.sh
┌─────────────────────────────────────────────────────┐
│  Content Provenance Report                          │
├──────────────┬──────────────────────────────────────┤
│ File         │ sample_ai_generated.jpg              │
│ C2PA Status  │ SIGNED — Content Credentials found   │
│ Source Type  │ trainedAlgorithmicMedia (AI-generated)│
│ Generator    │ DALL-E 3 / OpenAI                    │
│ Trust        │ VERIFIED — signature chain valid      │
└──────────────┴──────────────────────────────────────┘
```
