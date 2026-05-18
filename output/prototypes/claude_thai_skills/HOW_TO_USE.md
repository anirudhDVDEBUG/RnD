# How to Use: Claude Thai Skills

## Installation (Claude Code Skill)

This is a **Claude Code skill** — no pip install or npm needed. Just drop the skill file:

```bash
# Clone the source
git clone https://github.com/Boom-Vitt/claude-thai-skills.git

# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills/claude_thai_skills

# Copy all skill markdown files
cp claude-thai-skills/skills/*.md ~/.claude/skills/claude_thai_skills/
```

Or manually create `~/.claude/skills/claude_thai_skills/SKILL.md` with the skill definition from the source repo.

## Trigger Phrases

Claude Code activates these skills when you mention:

- **Translation:** "Translate to Thai", "แปลเป็นอังกฤษ", "Thai translation"
- **PDPA:** "PDPA compliance", "Thai privacy notice", "พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล"
- **Tax Invoice:** "Thai tax invoice", "ใบกำกับภาษี", "VAT invoice Thailand"
- **PromptPay:** "PromptPay QR", "generate PromptPay", "พร้อมเพย์"
- **National ID:** "Thai National ID", "เลขบัตรประชาชน", "validate Thai ID"
- **Buddhist Era:** "พ.ศ.", "Buddhist Era", "convert to Thai date"
- **Government Letter:** "Thai government letter", "จดหมายราชการ", "หนังสือราชการ"
- **LINE OA:** "LINE Official Account", "LINE Flex Message", "LINE OA Thailand"
- **Address:** "Thai address", "format Thai address", "จังหวัด อำเภอ ตำบล"
- **Resume:** "Thai resume", "เรซูเม่ภาษาไทย"
- **Captions:** "Thai caption", "แคปชั่นไทย", "Thai social media post"
- **NLP:** "Thai word segmentation", "Thai tokenization"

## First 60 Seconds

After installing the skill, open Claude Code and try:

### 1. Validate a Thai National ID
```
You: Validate this Thai ID: 1100600255911
Claude: Valid (checksum passes). Formatted: 1-1006-00255-91-1
```

### 2. Convert a date to Buddhist Era
```
You: Convert 2026-05-18 to Thai date format
Claude: 18 พฤษภาคม พ.ศ. 2569 (วันจันทร์)
```

### 3. Generate a PDPA notice
```
You: Generate a PDPA consent form for an e-commerce app collecting name, email, and shipping address
Claude: [Full Thai-language PDPA consent form with data subject rights]
```

### 4. Create a PromptPay payload
```
You: Generate PromptPay QR data for phone 0812345678, amount 150.50 baht
Claude: EMVCo payload string + breakdown of TLV fields
```

### 5. Format a Thai tax invoice
```
You: Create a tax invoice for ABC Co Ltd selling 10 laptops at 25,000 baht each
Claude: [Formatted ใบกำกับภาษี with 7% VAT calculation, totals in Thai baht]
```

## Standalone Demo (No Claude Code)

To see the utility functions in action without Claude Code:

```bash
pip install -r requirements.txt
bash run.sh
```

This runs the Python implementation of the core algorithmic skills (ID validation, date conversion, PromptPay payload, address formatting, NLP segmentation).

## File Layout

```
claude_thai_skills/
├── README.md
├── HOW_TO_USE.md
├── TECH_DETAILS.md
├── run.sh                  # End-to-end demo
├── requirements.txt        # Python deps
├── thai_skills/
│   ├── __init__.py
│   ├── national_id.py      # ID validation (mod-11)
│   ├── buddhist_era.py     # CE/BE date conversion
│   ├── promptpay.py        # EMVCo QR payload
│   ├── tax_invoice.py      # VAT invoice formatter
│   ├── address.py          # Thai address formatting
│   ├── nlp.py              # Basic Thai word segmentation
│   └── pdpa.py             # PDPA template generator
└── SKILL.md                # The actual Claude Code skill definition
```
