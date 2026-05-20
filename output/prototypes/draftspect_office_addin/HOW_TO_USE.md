# How to Use Draftspect

## Install (this demo)

```bash
git clone <this-repo> && cd draftspect_office_addin
npm install
bash run.sh
```

Requires: Node.js 18+. No API keys needed — the demo uses mock responses.

## Install (full version from source)

```bash
git clone https://github.com/LeonardHope/Draftspect-Add-Ins-for-Word-and-Excel-Powered-by-Claude-Code.git
cd Draftspect-Add-Ins-for-Word-and-Excel-Powered-by-Claude-Code
npm install
```

Requires: Node.js 18+, Claude Code CLI (`claude`) installed and authenticated, Microsoft Office (Word and/or Excel) desktop app.

## As a Claude Code Skill

Drop the skill definition into your skills directory:

```bash
mkdir -p ~/.claude/skills/draftspect_office_addin
# Copy the SKILL.md file into that directory
cp SKILL.md ~/.claude/skills/draftspect_office_addin/SKILL.md
```

**Trigger phrases:**
- "Create a Word add-in that uses Claude to edit documents"
- "Build an Excel sidebar that chats with Claude Code"
- "I want an Office add-in powered by Claude Code"
- "How do I integrate Claude Code into Microsoft Office?"

## Sideloading into Office

1. Generate HTTPS certs: `npx office-addin-dev-certs install`
2. Start the local server: `npm start` (serves on `https://localhost:3000`)
3. In Word or Excel: **Insert > My Add-ins > Upload My Add-in**
4. Select the `manifest.xml` file
5. The Draftspect sidebar panel appears — start chatting

## First 60 Seconds

**Input:** Open Word with any document, launch the Draftspect sidebar, type:
```
Summarize this document
```

**Output:**
```
Here's a summary of your document:

Q1 2026 Business Review Highlights:
- Revenue grew 12% YoY to $4.2M ARR
- Net Revenue Retention at 118%, CAC payback improved to 14 months
- 3 major features shipped (analytics dashboard, API v2, mobile redesign)
- Key challenge: enterprise deal cycles lengthened ~2 weeks
```

**Input:** Switch to the Excel tab, type:
```
Analyze the revenue data
```

**Output:**
```
Revenue Analysis (Q1 2026):
- ARR Growth (Jan→Mar): +9.1%, Accelerating
- Avg New Customers/mo: 52.7, Growing
- Churn Rate Trend: 1.8% → 1.2%, Improving
- Budget variance net positive at +$18,500
```

**Input:** Ask for an edit:
```
Rewrite the executive summary
```

**Output:** Claude drafts improved text and offers to apply it directly to the document. In the real add-in, clicking "Apply" writes through Office.js.
