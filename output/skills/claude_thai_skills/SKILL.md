---
name: claude_thai_skills
description: |
  Thai localization toolkit for Claude Code — 12 skills covering translation, social media captions, resume generation, government letters, PDPA compliance, tax invoices, PromptPay QR, Thai National ID validation, Buddhist Era dates, LINE OA messaging, Thai address formatting, and Thai NLP text processing.
  TRIGGER: user mentions Thai language, Thailand, พ.ศ., Buddhist Era, PDPA, PromptPay, Thai tax invoice, Thai National ID, Thai government letter, Thai resume, Thai caption, LINE OA Thailand, or any Thai localization task.
---

# Thai Localization Skills for Claude Code

A comprehensive set of 12 Thai-specific skills for Claude Code, covering language, compliance, finance, identity, and formatting needs for Thai users and Thailand-based projects.

## When to use

- "Translate this text to Thai" or "แปลข้อความนี้เป็นภาษาอังกฤษ"
- "Generate a PDPA-compliant privacy notice for my Thai app"
- "Create a Thai tax invoice (ใบกำกับภาษี) for this transaction"
- "Validate this Thai National ID number (เลขบัตรประชาชน)"
- "Convert this date to Buddhist Era (พ.ศ.) format"

## Skills Overview

This toolkit provides 12 skills:

| # | Skill | Description |
|---|-------|-------------|
| 1 | **Translation (แปล)** | Translate between Thai and other languages with natural, context-aware phrasing |
| 2 | **Captions (แคปชั่น)** | Generate Thai social media captions for Facebook, Instagram, LINE, TikTok |
| 3 | **Resume (เรซูเม่)** | Create Thai-format resumes following local conventions |
| 4 | **Government Letters (จดหมายราชการ)** | Draft formal Thai government correspondence with proper formatting and honorifics |
| 5 | **PDPA Compliance** | Generate Thailand Personal Data Protection Act (PDPA) notices, consent forms, and policies |
| 6 | **Tax Invoice (ใบกำกับภาษี)** | Format Thai tax invoices with VAT calculation per Revenue Department standards |
| 7 | **PromptPay** | Generate PromptPay payment details, QR payload strings, and integration helpers |
| 8 | **National ID (เลขบัตร ปชช.)** | Validate and format 13-digit Thai National ID numbers with checksum verification |
| 9 | **Buddhist Era Dates (วันที่ พ.ศ.)** | Convert between CE and BE dates, format Thai date strings (e.g., 18 พฤษภาคม พ.ศ. 2569) |
| 10 | **LINE OA Messaging** | Draft LINE Official Account messages, rich menus, and Flex Messages for Thai audiences |
| 11 | **Thai Address Formatting** | Format Thai addresses with province (จังหวัด), district (อำเภอ), sub-district (ตำบล), and postal code |
| 12 | **Thai NLP Text Processing** | Thai word segmentation, tokenization, and text normalization helpers |

## How to use

### 1. Translation (แปล)
Provide source text and target language. The skill uses natural Thai phrasing (not literal translation).
```
User: Translate "Please review the pull request" to Thai
Result: กรุณาตรวจสอบ Pull Request
```

### 2. Captions (แคปชั่น)
Specify the platform, product/topic, and desired tone. The skill generates platform-appropriate Thai captions with hashtags.
```
User: Write a Thai Instagram caption for a new coffee shop launch
```

### 3. Resume (เรซูเม่)
Provide personal details, education, and experience. Outputs a Thai-format resume with proper structure (ประวัติส่วนตัว, การศึกษา, ประสบการณ์ทำงาน).

### 4. Government Letters (จดหมายราชการ)
Specify sender, recipient, subject, and body. Formats with correct Thai formal letter structure: เรียน, เรื่อง, สิ่งที่ส่งมาด้วย, proper closing (ขอแสดงความนับถือ).

### 5. PDPA Compliance
Specify data types collected and processing purposes. Generates legally-structured Thai privacy notices, consent forms, and data subject rights sections per Thailand's PDPA (พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562).

### 6. Tax Invoice (ใบกำกับภาษี)
Provide seller/buyer info, items, and amounts. Formats per Thai Revenue Department requirements with 7% VAT calculation, tax ID numbers, and bilingual fields.

### 7. PromptPay
Provide phone number or National ID. Generates PromptPay payload data for QR code generation following Bank of Thailand EMVCo standard.
```
User: Generate PromptPay QR data for phone 0812345678, amount 500 baht
```

### 8. National ID Validation (เลขบัตร ปชช.)
Provide a 13-digit number. Validates using the official checksum algorithm (modulo 11) and returns validity status.
```python
def validate_thai_id(id_number: str) -> bool:
    if len(id_number) != 13 or not id_number.isdigit():
        return False
    total = sum(int(id_number[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == int(id_number[12])
```

### 9. Buddhist Era Dates (วันที่ พ.ศ.)
Convert between CE (ค.ศ.) and BE (พ.ศ.) by adding/subtracting 543. Format dates in Thai locale.
```
User: Convert 2026-05-18 to Thai date format
Result: 18 พฤษภาคม พ.ศ. 2569
```

### 10. LINE OA Messaging
Specify message type (text, Flex Message, rich menu) and content. Generates LINE Messaging API-compatible JSON for Thai business communication.

### 11. Thai Address Formatting
Provide address components. Formats following Thai postal conventions:
```
123/45 ซอยสุขุมวิท 55 ถนนสุขุมวิท
แขวงคลองตันเหนือ เขตวัฒนา
กรุงเทพมหานคร 10110
```

### 12. Thai NLP Text Processing
Process Thai text with word segmentation (since Thai has no spaces between words), basic tokenization, and text normalization.

## Notes

- All outputs default to Thai language unless otherwise specified
- Financial amounts use Thai Baht (฿) formatting with สตางค์ for decimals
- Date/time defaults to Bangkok timezone (Asia/Bangkok, UTC+7)
- Government and legal documents follow current Thai regulatory standards

## References

- Source: [Boom-Vitt/claude-thai-skills](https://github.com/Boom-Vitt/claude-thai-skills)
- PDPA Reference: Thailand Personal Data Protection Act B.E. 2562 (2019)
- PromptPay Standard: Bank of Thailand EMVCo QR Code specification
- Thai National ID: Ministry of Interior checksum algorithm
