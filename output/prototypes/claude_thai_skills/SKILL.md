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

## Skills

### 1. Translation (แปล)
Translate between Thai and other languages with natural, context-aware phrasing (not literal).

### 2. Captions (แคปชั่น)
Generate Thai social media captions for Facebook, Instagram, LINE, TikTok with platform-appropriate hashtags.

### 3. Resume (เรซูเม่)
Create Thai-format resumes: ประวัติส่วนตัว, การศึกษา, ประสบการณ์ทำงาน.

### 4. Government Letters (จดหมายราชการ)
Draft formal Thai government correspondence with เรียน, เรื่อง, สิ่งที่ส่งมาด้วย, ขอแสดงความนับถือ.

### 5. PDPA Compliance
Generate privacy notices, consent forms per พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562.

### 6. Tax Invoice (ใบกำกับภาษี)
Format with 7% VAT, tax IDs, bilingual fields per Revenue Department standards.

### 7. PromptPay
EMVCo QR payload generation per Bank of Thailand standard.

### 8. National ID (เลขบัตร ปชช.)
Validate 13-digit Thai ID with modulo-11 checksum:
```python
total = sum(int(id[i]) * (13 - i) for i in range(12))
check = (11 - (total % 11)) % 10
valid = check == int(id[12])
```

### 9. Buddhist Era Dates (วันที่ พ.ศ.)
CE + 543 = BE. Format: 18 พฤษภาคม พ.ศ. 2569

### 10. LINE OA Messaging
LINE Messaging API-compatible JSON for Thai business (Flex Messages, rich menus).

### 11. Thai Address Formatting
Bangkok: แขวง/เขต/กรุงเทพมหานคร. Provinces: ตำบล/อำเภอ/จังหวัด.

### 12. Thai NLP
Word segmentation for no-space Thai text using maximal matching.

## Notes
- Default output language: Thai
- Currency: Thai Baht (฿) with สตางค์
- Timezone: Asia/Bangkok (UTC+7)
- All financial amounts include 7% VAT when applicable
