#!/usr/bin/env bash
# Claude Thai Skills — End-to-end demo (no API keys needed)
set -e

cd "$(dirname "$0")"

echo "=============================================="
echo "  Claude Thai Skills — Demo"
echo "  12 Thai Localization Skills for Claude Code"
echo "=============================================="
echo ""

python3 -c "
import sys
sys.path.insert(0, '.')
from thai_skills import (
    validate_thai_id, format_thai_id,
    to_buddhist_era, format_thai_date, parse_thai_date_string,
    generate_promptpay_payload,
    generate_tax_invoice,
    format_thai_address,
    segment_thai_text,
    generate_pdpa_notice,
)
from datetime import date

print('=' * 50)
print('1. NATIONAL ID VALIDATION (เลขบัตรประชาชน)')
print('=' * 50)
# Test with a sample ID (valid checksum)
test_ids = ['1100600255911', '3100500123456', '1234567890123']
for tid in test_ids:
    result = validate_thai_id(tid)
    status = 'VALID' if result['valid'] else 'INVALID'
    print(f'  ID: {tid} => {status} | Formatted: {result[\"formatted\"]}')
print()

print('=' * 50)
print('2. BUDDHIST ERA DATES (วันที่ พ.ศ.)')
print('=' * 50)
test_dates = ['2026-05-18', '2024-01-01', '2000-12-31']
for d in test_dates:
    result = parse_thai_date_string(d)
    print(f'  {d} => {result[\"thai_formatted\"]}')
    print(f'           {result[\"thai_abbreviated\"]}')
print()

print('=' * 50)
print('3. PROMPTPAY QR PAYLOAD (พร้อมเพย์)')
print('=' * 50)
# Phone number example
result = generate_promptpay_payload('0812345678', amount=150.50)
print(f'  Target: {result[\"target\"]} ({result[\"target_type\"]})')
print(f'  Amount: {result[\"amount\"]} THB')
print(f'  CRC:    {result[\"crc\"]}')
print(f'  Payload: {result[\"payload\"][:60]}...')
print()
# National ID example
result2 = generate_promptpay_payload('1100600255911')
print(f'  Target: {result2[\"target\"]} ({result2[\"target_type\"]})')
print(f'  Amount: Open (no amount specified)')
print(f'  Payload: {result2[\"payload\"][:60]}...')
print()

print('=' * 50)
print('4. TAX INVOICE (ใบกำกับภาษี)')
print('=' * 50)
invoice = generate_tax_invoice(
    seller_name='บริษัท เอบีซี จำกัด',
    seller_tax_id='0105556123456',
    buyer_name='บริษัท XYZ จำกัด (มหาชน)',
    buyer_tax_id='0107558000123',
    items=[
        {'description': 'คอมพิวเตอร์โน้ตบุ๊ก', 'quantity': 5, 'unit_price': 25000.0},
        {'description': 'เมาส์ไร้สาย', 'quantity': 5, 'unit_price': 590.0},
        {'description': 'แป้นพิมพ์', 'quantity': 5, 'unit_price': 1200.0},
    ],
    invoice_number='INV-2569-001',
    invoice_date=date(2026, 5, 18),
)
print(f'  {invoice[\"title\"]}')
print(f'  เลขที่: {invoice[\"invoice_number\"]}')
print(f'  วันที่: {invoice[\"date_thai\"]}')
print(f'  ผู้ขาย: {invoice[\"seller\"][\"name\"]} (TIN: {invoice[\"seller\"][\"tax_id\"]})')
print(f'  ผู้ซื้อ: {invoice[\"buyer\"][\"name\"]} (TIN: {invoice[\"buyer\"][\"tax_id\"]})')
print(f'  รายการ:')
for item in invoice['items']:
    print(f'    - {item[\"description\"]} x{item[\"quantity\"]} = {item[\"total_formatted\"]}')
print(f'  ราคาสินค้า:  {invoice[\"subtotal\"]}')
print(f'  ภาษีมูลค่าเพิ่ม {invoice[\"vat_rate\"]}: {invoice[\"vat_amount\"]}')
print(f'  รวมทั้งสิ้น: {invoice[\"grand_total\"]}')
print(f'  ({invoice[\"grand_total_text\"]})')
print()

print('=' * 50)
print('5. THAI ADDRESS FORMATTING (ที่อยู่)')
print('=' * 50)
# Bangkok address
addr1 = format_thai_address(
    house_number='123/45',
    soi='สุขุมวิท 55',
    road='สุขุมวิท',
    sub_district='คลองตันเหนือ',
    district='วัฒนา',
    postal_code='10110',
    is_bangkok=True,
)
print('  [กรุงเทพฯ]:')
for line in addr1['lines']:
    print(f'    {line}')
print()

# Provincial address
addr2 = format_thai_address(
    house_number='99/1',
    village='พฤกษาวิลล์',
    road='มิตรภาพ',
    sub_district='ในเมือง',
    district='เมืองนครราชสีมา',
    province='นครราชสีมา',
    postal_code='30000',
    is_bangkok=False,
)
print('  [ต่างจังหวัด]:')
for line in addr2['lines']:
    print(f'    {line}')
print()

print('=' * 50)
print('6. THAI NLP WORD SEGMENTATION (ตัดคำ)')
print('=' * 50)
test_texts = [
    'สวัสดีครับวันนี้อากาศดีมาก',
    'ประเทศไทยภาษาไทย',
    'ขอบคุณมากที่สุดครับ',
]
for text in test_texts:
    words = segment_thai_text(text)
    print(f'  Input:  {text}')
    print(f'  Output: {\"|\".join(words)}')
    print()

print('=' * 50)
print('7. PDPA PRIVACY NOTICE (ประกาศ PDPA)')
print('=' * 50)
pdpa = generate_pdpa_notice(
    company_name='บริษัท สมาร์ทเทค จำกัด',
    data_categories=['ชื่อ-นามสกุล', 'อีเมล', 'เบอร์โทรศัพท์', 'ที่อยู่จัดส่ง'],
    purposes=['จัดส่งสินค้า', 'แจ้งโปรโมชัน', 'ปรับปรุงบริการ'],
    contact_email='dpo@smarttech.co.th',
)
# Print first 15 lines of notice
notice_lines = pdpa['privacy_notice'].split('\n')
for line in notice_lines[:20]:
    print(f'  {line}')
print('  ...')
print()

print('=' * 50)
print('DEMO COMPLETE')
print('=' * 50)
print()
print('All 7 algorithmic skills demonstrated successfully.')
print('The remaining 5 skills (Translation, Captions, Resume,')
print('Government Letters, LINE OA) are generative — they work')
print('through Claude Code\\'s skill system with Thai prompts.')
"
