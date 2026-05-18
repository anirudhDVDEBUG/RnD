"""PDPA (Thai Personal Data Protection Act) notice generator."""


def generate_pdpa_notice(
    company_name: str,
    data_categories: list,
    purposes: list,
    contact_email: str = "",
) -> dict:
    """Generate a PDPA-compliant privacy notice template.

    Args:
        company_name: Name of the data controller
        data_categories: List of data types collected (e.g., ["ชื่อ-นามสกุล", "อีเมล"])
        purposes: List of processing purposes
        contact_email: DPO contact email
    """

    # Data category descriptions
    category_text = "\n".join(f"  - {cat}" for cat in data_categories)
    purpose_text = "\n".join(f"  - {p}" for p in purposes)

    notice = f"""ประกาศความเป็นส่วนตัว (Privacy Notice)
{'='*50}

ผู้ควบคุมข้อมูลส่วนบุคคล: {company_name}

ตามพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 (PDPA)
{company_name} ขอแจ้งให้ท่านทราบเกี่ยวกับการเก็บรวบรวม ใช้
และเปิดเผยข้อมูลส่วนบุคคลของท่าน ดังนี้

1. ข้อมูลส่วนบุคคลที่เก็บรวบรวม:
{category_text}

2. วัตถุประสงค์ในการประมวลผล:
{purpose_text}

3. สิทธิของเจ้าของข้อมูล:
  - สิทธิในการเข้าถึงข้อมูล
  - สิทธิในการแก้ไขข้อมูล
  - สิทธิในการลบข้อมูล
  - สิทธิในการระงับการใช้ข้อมูล
  - สิทธิในการโอนย้ายข้อมูล
  - สิทธิในการคัดค้านการประมวลผล
  - สิทธิในการถอนความยินยอม

4. ระยะเวลาการเก็บรักษา:
  เก็บรักษาตลอดระยะเวลาที่ท่านใช้บริการ และอีก 10 ปี
  หลังจากยุติการใช้บริการ หรือตามที่กฎหมายกำหนด

5. การติดต่อ:
  เจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO)
  อีเมล: {contact_email or f'dpo@{company_name.lower().replace(" ", "")}.co.th'}
"""

    consent_form = f"""แบบฟอร์มความยินยอม (Consent Form)
{'='*50}

ข้าพเจ้ายินยอมให้ {company_name} เก็บรวบรวม ใช้ และเปิดเผย
ข้อมูลส่วนบุคคลของข้าพเจ้าตามวัตถุประสงค์ที่ระบุไว้ในประกาศ
ความเป็นส่วนตัว

[ ] ข้าพเจ้ายินยอม (I consent)
[ ] ข้าพเจ้าไม่ยินยอม (I do not consent)

ลงชื่อ: ___________________
วันที่: ___________________
"""

    return {
        "privacy_notice": notice,
        "consent_form": consent_form,
        "company": company_name,
        "data_categories": data_categories,
        "purposes": purposes,
        "legal_basis": "พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562",
    }
