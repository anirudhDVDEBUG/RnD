"""Mock clinical encounter data for demonstration purposes.
All data is fictional — no real PHI is used."""


ENCOUNTERS = [
    {
        "workflow_type": "progress_note",
        "clinician_id": "DR-CHEN-4421",
        "role": "physician",
        "context": {
            "patient_name": "Jane Doe",
            "mrn": "MRN-00112233",
            "provider": "Dr. Lisa Chen",
            "date": "2026-05-22",
            "chief_complaint": "persistent lower back pain, worsening over 3 weeks",
            "symptom_duration": "3-week",
            "additional_history": "Denies radiculopathy, no bowel/bladder changes. "
                                 "Tried OTC ibuprofen with partial relief.",
            "bp": "128/82", "hr": "74", "temp": "98.4F", "spo2": "99%",
            "exam_findings": "Tenderness over L4-L5 paraspinal muscles. "
                             "Negative straight-leg raise bilaterally. "
                             "Full ROM in hips. Gait normal.",
            "assessment": "1. Mechanical low back pain, likely musculoskeletal\n"
                          "2. No red-flag features for urgent imaging",
            "plan": "1. Start physical therapy 2x/week for 6 weeks\n"
                    "2. Naproxen 500mg BID with food x 14 days\n"
                    "3. Ergonomic workstation assessment\n"
                    "4. Return in 4 weeks; MRI if no improvement",
        },
    },
    {
        "workflow_type": "discharge_summary",
        "clinician_id": "DR-PATEL-7783",
        "role": "physician",
        "context": {
            "patient_name": "Robert Smith",
            "mrn": "MRN-00445566",
            "provider": "Dr. Anil Patel",
            "admit_date": "2026-05-15",
            "discharge_date": "2026-05-20",
            "reason_for_admission": "Community-acquired pneumonia with hypoxia "
                                    "(SpO2 88% on room air at presentation)",
            "hospital_course": "Admitted to medical floor. Started on IV ceftriaxone "
                               "and azithromycin. Oxygen via nasal cannula titrated "
                               "from 4L to 2L over 48 hours. Blood cultures negative. "
                               "Sputum culture grew Streptococcus pneumoniae. "
                               "Transitioned to oral antibiotics on day 3. "
                               "SpO2 stable at 96% on room air by day 5.",
            "discharge_diagnosis": "Community-acquired pneumonia (S. pneumoniae)",
            "medications": "1. Amoxicillin 875mg BID x 5 more days\n"
                           "2. Guaifenesin 600mg q12h PRN cough\n"
                           "3. Resume home medications (lisinopril 10mg, atorvastatin 20mg)",
            "follow_up": "1. PCP follow-up in 7 days\n"
                         "2. Repeat chest X-ray in 6 weeks\n"
                         "3. Return to ED if fever > 101.5, worsening dyspnea, or chest pain",
        },
    },
    {
        "workflow_type": "patient_message",
        "clinician_id": "RN-GARCIA-1192",
        "role": "nurse",
        "context": {
            "patient_name": "Maria",
            "visit_date": "May 19, 2026",
            "provider": "Dr. James Wright",
            "message_body": "Your lab results from last week are back. Your blood sugar "
                            "(A1C) level is 6.8%, which is slightly above the normal range. "
                            "Dr. Wright would like you to:\n\n"
                            "- Continue your current medication (metformin 500mg twice daily)\n"
                            "- Try to walk for 30 minutes at least 5 days a week\n"
                            "- Cut back on sugary drinks and white bread\n\n"
                            "We have scheduled a follow-up visit in 3 months to recheck "
                            "your levels. You are doing a great job managing your health!",
            "office_phone": "(555) 123-4567",
            "department": "Internal Medicine",
        },
    },
    {
        "workflow_type": "referral_letter",
        "clinician_id": "DR-CHEN-4421",
        "role": "physician",
        "context": {
            "patient_name": "Thomas Anderson",
            "dob": "1978-03-15",
            "mrn": "MRN-00778899",
            "provider": "Dr. Lisa Chen",
            "department": "Primary Care",
            "date": "2026-05-22",
            "referral_to": "Dr. Sarah Kim, Cardiology",
            "referral_reason": "new-onset atrial fibrillation detected on routine ECG",
            "relevant_history": "48yo male, no prior cardiac history. Presented for annual "
                                "physical. ECG showed irregularly irregular rhythm consistent "
                                "with AFib, ventricular rate 92. CHA2DS2-VASc score = 1. "
                                "Echocardiogram pending. Patient reports occasional palpitations "
                                "over past 2 months, no syncope or chest pain.",
            "medications": "1. Atorvastatin 20mg daily\n2. Metoprolol 25mg BID (started today)",
        },
    },
    {
        "workflow_type": "care_plan",
        "clinician_id": "CC-NGUYEN-3305",
        "role": "care_coordinator",
        "context": {
            "patient_name": "Eleanor Williams",
            "provider": "Care Team (Lead: Dr. Patel)",
            "date": "2026-05-22",
            "problems": "1. Type 2 Diabetes (A1C 8.2%)\n"
                        "2. Hypertension (poorly controlled)\n"
                        "3. Obesity (BMI 34)\n"
                        "4. Depression (PHQ-9 score 14)",
            "goals": "1. Reduce A1C to < 7.5% within 6 months\n"
                     "2. Blood pressure < 140/90 consistently\n"
                     "3. Lose 5% body weight (target: 8 lbs) in 3 months\n"
                     "4. PHQ-9 score < 10 within 3 months",
            "interventions": "1. Endocrinology consult for insulin optimization\n"
                             "2. Home BP monitoring with weekly telehealth check-ins\n"
                             "3. Nutritionist referral + structured meal plan\n"
                             "4. Behavioral health intake scheduled\n"
                             "5. Community health worker for social support assessment",
            "follow_up_schedule": "- Weekly telehealth BP check (RN)\n"
                                  "- Monthly in-person visit (PCP)\n"
                                  "- Quarterly A1C recheck\n"
                                  "- Behavioral health: biweekly sessions",
            "care_team": "- PCP: Dr. Anil Patel\n"
                         "- Care Coordinator: Tina Nguyen\n"
                         "- Endocrinology: Dr. Reyes\n"
                         "- Nutrition: Jamie Collins, RD\n"
                         "- Behavioral Health: Dr. Okafor",
        },
    },
    {
        "workflow_type": "after_visit_summary",
        "clinician_id": "DR-PATEL-7783",
        "role": "physician",
        "context": {
            "patient_name": "David",
            "visit_date": "May 22, 2026",
            "provider": "Dr. Anil Patel",
            "discussion_summary": "We talked about your knee pain that has been bothering "
                                  "you for the past month. After examining your knee, I believe "
                                  "this is early osteoarthritis. We discussed treatment options "
                                  "including exercise, weight management, and medication.",
            "patient_instructions": "1. Take acetaminophen (Tylenol) 500mg up to 3 times "
                                    "daily as needed for pain\n"
                                    "2. Do the knee-strengthening exercises shown today — "
                                    "15 minutes, twice daily\n"
                                    "3. Apply ice for 15 minutes after activity if swollen\n"
                                    "4. Avoid high-impact activities (running, jumping) for now",
            "medications": "- Acetaminophen 500mg as needed (new)\n"
                           "- All other medications remain the same",
            "next_appointment": "6 weeks from today — we will recheck your knee and "
                                "discuss imaging if not improving",
            "office_phone": "(555) 123-4567",
        },
    },
]


# Scenario for role-based access denial demo
ACCESS_DENIED_SCENARIO = {
    "workflow_type": "discharge_summary",
    "clinician_id": "ADMIN-JONES-5501",
    "role": "admin",
    "context": {
        "patient_name": "Test Patient",
        "mrn": "MRN-TEST",
    },
}
