# Technical Details

## What it does

The Open Source Policy Advisor is a Claude Code skill that encodes the UK Government Digital Service (GDS) "open by default" policy framework into structured decision support. When a user describes a public-sector open source dilemma — typically triggered by vulnerability reports or political pressure to close repositories — the skill guides Claude to produce a proportionate recommendation with actionable policy language.

The companion CLI script (`advisor.py`) demonstrates the same decision logic as standalone Python, evaluating mock scenarios and producing advisory reports with risk scores, recommended actions, and draft policy clauses. It requires no API keys or external services.

## Architecture

```
SKILL.md            — Claude Code skill (markdown prompt + decision framework)
advisor.py          — CLI demo implementing the advisory logic in Python
  ├── Scenario      — Dataclass: org name, repo count, vulnerabilities, context flags
  ├── Vulnerability — Dataclass: name, severity, exploitation status, patch status
  ├── assess()      — Core scoring engine: severity weights + exploitation + context → risk score + action
  └── Recommendation— Dataclass: action, rationale, steps, policy clauses, risk score
```

**Data flow:** Scenario → `assess()` → Recommendation → formatted report (text or JSON).

**Scoring logic:**
- Each vulnerability contributes a severity-weighted score (Low=1, Med=2, High=4, Critical=7)
- Actively exploited vulnerabilities add +5
- Unpatched vulnerabilities add +2
- AI scanning and public pressure each add +1 (contextual, not decisive)
- Score capped at 10

**Decision rules:**
- If any vulnerability is both critical and actively exploited → temporary closure of affected repos only
- Otherwise → stay open, fix in place
- Permanent closure is never recommended (by design, matching GDS guidance)

**Dependencies:** Python 3.8+ standard library only (`json`, `sys`, `textwrap`, `dataclasses`, `enum`). Zero external packages.

## Limitations

- **Not a scanner.** This tool does not find vulnerabilities — it advises on policy responses to vulnerabilities found by other tools.
- **UK-centric framing.** The GDS framework and NHS/HMRC examples are UK-specific. The principles generalise, but the policy language references UK standards.
- **No LLM calls in the CLI.** The Python demo uses hardcoded logic. The actual skill relies on Claude interpreting the SKILL.md framework and applying it to user-described situations.
- **Mock data only.** The three scenarios are illustrative. Real advisory work would require actual vulnerability data and organisational context.
- **Binary action model.** The engine recommends stay-open or temporary-closure. Real policy may need more nuanced partial-closure strategies.

## Why it matters for Claude-driven products

- **Agent factories / consulting agents:** This pattern — encoding a domain policy framework into a skill that produces structured recommendations — transfers directly to compliance advisors, procurement evaluators, or risk assessors. The skill-as-policy-engine pattern is reusable.
- **Lead-gen / marketing:** Public-sector decision-makers searching for open source policy guidance are a defined audience. A demo like this positions a product as authoritative on a timely topic (GDS guidance was published May 14, 2026).
- **Security tooling:** Teams building AI-powered security scanners (like Project Glasswing) need the "what do we do after we find vulnerabilities?" layer. This skill fills that gap.
- **Policy automation:** The draft policy clauses output is directly usable in governance documents, reducing the gap between "AI found a problem" and "organisation has a policy response."
