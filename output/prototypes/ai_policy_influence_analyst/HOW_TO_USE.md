# How To Use

## This is a Claude Code SKILL

### Installation

1. Create the skill directory:

```bash
mkdir -p ~/.claude/skills/ai_policy_influence_analyst
```

2. Copy the skill file:

```bash
cp SKILL.md ~/.claude/skills/ai_policy_influence_analyst/SKILL.md
```

That's it. No pip install, no npm, no API keys.

### Trigger Phrases

The skill activates when you ask Claude Code things like:

- "How is Anthropic influencing AI regulation?"
- "Analyze the lobbying strategy behind this AI policy document"
- "What vendor interests are embedded in this AI ethics framework?"
- "Compare how AI companies position their technical limitations as ethical principles"
- "Identify corporate influence in this AI governance proposal"
- "Who benefits from the safety framing in the EU AI Act?"

### First 60 Seconds

**Step 1:** Install the skill (above).

**Step 2:** Open Claude Code in any project.

**Step 3:** Ask:

```
Analyze Anthropic's influence on the papal encyclical Magnifica Humanitas (May 2026)
```

**Expected output:**

```
## Policy Influence Analysis

### Document: Magnifica Humanitas (Papal Encyclical, May 2026)

### Influencing Party
- **Company:** Anthropic
- **Agent:** Christopher Olah (co-founder)
- **Channel:** Direct advisory relationship with Vatican

### Commercial Interest Mapping
| Encyclical Principle | Technical Reality | Beneficiary |
|---------------------|-------------------|-------------|
| "AI must have intrinsic value alignment" | Constitutional AI architecture | Anthropic |
| "Bounded autonomy as moral imperative" | Context window limitations | Anthropic |
| "Transparency of reasoning" | Chain-of-thought logging | Anthropic |

### Strategy Classification
- **Primary:** Institutional Blessing
- **Secondary:** Limitation Laundering
- **Effectiveness:** Unprecedented — religious authority endorsing vendor architecture

### Assessment
This represents regulatory capture via moral authority rather than legislative
channels. By embedding technical constraints into spiritual doctrine, the
approach bypasses traditional lobbying scrutiny entirely.
```

## Standalone Demo (no Claude Code needed)

To see the analysis engine in action with mock data:

```bash
pip install -r requirements.txt
bash run.sh
```

This runs `analyst.py` against sample policy documents and prints structured influence analyses.
