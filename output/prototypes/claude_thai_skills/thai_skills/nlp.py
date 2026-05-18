"""Basic Thai word segmentation using dictionary-based maximal matching."""

# Common Thai words dictionary (subset for demo)
THAI_DICT = set([
    "กรุณา", "ตรวจ", "สอบ", "ข้อมูล", "ส่วน", "บุคคล", "ของ", "คุณ",
    "สวัสดี", "ครับ", "ค่ะ", "ขอบคุณ", "มาก", "ที่", "สุด",
    "ประเทศ", "ไทย", "ภาษา", "การ", "เรียน", "รู้", "ใหม่",
    "วัน", "นี้", "พรุ่ง", "เมื่อ", "วาน", "อาทิตย์", "จันทร์",
    "บ้าน", "เมือง", "ถนน", "ซอย", "จังหวัด", "อำเภอ",
    "เงิน", "บาท", "สตางค์", "ราคา", "ซื้อ", "ขาย",
    "คน", "ผู้", "ชาย", "หญิง", "เด็ก", "ใหญ่", "เล็ก",
    "ดี", "ไม่", "ใช่", "ได้", "ไป", "มา", "กิน", "ข้าว",
    "น้ำ", "อาหาร", "ร้าน", "โรง", "เรียน", "พยาบาล",
    "รัก", "ชอบ", "อยาก", "ต้อง", "การ", "ทำ", "งาน",
    "บริษัท", "จำกัด", "มหาชน", "หุ้น", "ลงทุน",
    "โทรศัพท์", "มือ", "ถือ", "คอม", "พิว", "เตอร์",
    "อินเทอร์เน็ต", "เว็บ", "ไซต์", "แอป", "พลิ", "เค", "ชัน",
    "สุข", "ภาพ", "แข็ง", "แรง", "ออก", "กำลัง", "กาย",
    "อากาศ", "ร้อน", "หนาว", "ฝน", "ตก", "แดด",
    "เรา", "เขา", "พวก", "ทุก", "ทั้ง", "หมด", "แต่ละ",
    "จะ", "แล้ว", "ยัง", "กำลัง", "เคย", "อยู่",
    "และ", "หรือ", "แต่", "เพราะ", "ถ้า", "เมื่อ",
    "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า", "สิบ",
    "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน",
    "คุ้มครอง", "ข้อมูล", "ส่วนบุคคล", "ความ", "ยินยอม",
    "สิทธิ์", "เจ้าของ", "ประมวล", "ผล",
])

MAX_WORD_LEN = max(len(w) for w in THAI_DICT)


def segment_thai_text(text: str) -> list:
    """Segment Thai text into words using greedy maximal matching.

    This is a basic implementation. For production, use PyThaiNLP.
    """
    words = []
    pos = 0

    while pos < len(text):
        # Skip spaces and ASCII
        if text[pos] == ' ':
            pos += 1
            continue

        # Try ASCII/number sequences
        if ord(text[pos]) < 0x0E00 or ord(text[pos]) > 0x0E7F:
            ascii_word = ""
            while pos < len(text) and (ord(text[pos]) < 0x0E00 or ord(text[pos]) > 0x0E7F) and text[pos] != ' ':
                ascii_word += text[pos]
                pos += 1
            if ascii_word:
                words.append(ascii_word)
            continue

        # Maximal matching for Thai characters
        matched = False
        for length in range(min(MAX_WORD_LEN, len(text) - pos), 0, -1):
            candidate = text[pos:pos + length]
            if candidate in THAI_DICT:
                words.append(candidate)
                pos += length
                matched = True
                break

        if not matched:
            # Single character fallback
            words.append(text[pos])
            pos += 1

    return words
