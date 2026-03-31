"""
Shapeshifters Healthcare — Surgical Checklist
Pre-op and post-op checklists for common surgeries at Eesha Hospital.
"""

SURGICAL_CHECKLISTS = {
    "general_surgery": {
        "name":     "General Surgery",
        "examples": ["hernia", "appendix", "gallbladder", "laparoscopy"],
        "pre_op": {
            "7_days_before": [
                "Inform your surgeon of ALL medications you take",
                "Stop blood thinners (aspirin, warfarin) — only if surgeon advises",
                "Arrange for someone to drive you home after surgery",
                "Arrange for help at home for 3-5 days post surgery",
                "Complete all pre-operative blood tests and ECG",
                "Get physician clearance if you have diabetes or heart disease",
            ],
            "night_before": [
                "Do NOT eat or drink anything after midnight",
                "Shower with antiseptic soap if provided",
                "Remove nail polish and nail extensions",
                "Do not apply any creams, lotions, or perfumes",
                "Keep overnight bag ready",
                "Sleep early — rest is important",
            ],
            "day_of_surgery": [
                "Do NOT eat or drink anything — strict nil by mouth",
                "Take only approved medications with a small sip of water",
                "Wear loose, comfortable clothing",
                "Remove all jewellery and piercings before leaving home",
                "Carry: Aadhaar card, insurance card, hospital documents",
                "Arrive at hospital 2 hours before scheduled surgery time",
                "Inform nursing staff of any fever, cold, or new symptoms",
            ],
            "documents_needed": [
                "Hospital admission form",
                "Previous medical records",
                "Blood test reports",
                "ECG report",
                "Physician clearance letter",
                "Insurance pre-authorisation letter",
                "Photo ID (Aadhaar/PAN)",
            ],
        },
        "post_op": {
            "in_hospital": [
                "Do not get up without nursing assistance for first 6 hours",
                "Pain is normal — inform nurse immediately if severe",
                "Deep breathing exercises every 2 hours",
                "Start walking with support as advised by physiotherapist",
                "Take all medications as prescribed",
                "Keep wound area clean and dry",
            ],
            "week_1_at_home": [
                "Rest completely — no heavy lifting over 2 kg",
                "Keep surgical wound dry — no bathing until stitches removed",
                "Take all prescribed antibiotics — complete the full course",
                "Take pain medications as prescribed — do not skip",
                "Watch for warning signs: fever above 38°C, redness, swelling",
                "Eat light, easily digestible food — dal, khichdi, rice",
                "No spicy, oily, or heavy food",
                "Drink 8-10 glasses of water daily",
            ],
            "week_2_3": [
                "Gradually increase activity — short walks inside home",
                "Continue wound care as instructed",
                "Attend follow-up appointment — do not miss",
                "You may shower gently — avoid soaking wound",
                "Light diet can progress to normal food",
            ],
            "when_to_call_doctor": [
                "Fever above 38°C (100.4°F)",
                "Increasing redness, swelling, or warmth at wound site",
                "Pus or foul-smelling discharge from wound",
                "Severe pain not controlled by prescribed medication",
                "Nausea, vomiting, or inability to keep food down",
                "No bowel movement for more than 3 days",
                "Difficulty breathing or chest pain — go to emergency immediately",
            ],
            "follow_up_schedule": [
                "Day 3: Wound check and dressing change",
                "Day 7: Suture removal (if applicable)",
                "Day 14: Post-op review with surgeon",
                "Day 30: Final clearance appointment",
            ],
        },
    },

    "orthopaedic_surgery": {
        "name":     "Orthopaedic Surgery",
        "examples": ["knee replacement", "hip replacement", "fracture fixation", "arthroscopy"],
        "pre_op": {
            "7_days_before": [
                "Physiotherapy assessment — start pre-op exercises",
                "Stop blood thinners as advised by orthopaedic surgeon",
                "Dental check — any dental work must be done BEFORE surgery",
                "Arrange elevated toilet seat and grab bars at home",
                "Arrange ground floor sleeping area if possible",
                "Complete blood tests, X-rays, and MRI as ordered",
                "Lose weight if advised — even 2-3 kg helps recovery",
            ],
            "night_before": [
                "Nil by mouth after midnight — strictly no food or water",
                "Shave surgical area if asked by nursing staff",
                "Antiseptic bath or shower",
                "Keep hospital bag ready with loose clothing",
                "Arrange walker or crutches at home before surgery",
            ],
            "day_of_surgery": [
                "Nil by mouth — absolutely no food or water",
                "Wear loose, comfortable clothing — shorts recommended for knee surgery",
                "Arrive 2 hours before scheduled time",
                "Bring all imaging: X-rays, MRI, CT scans (physical copies)",
                "Bring insurance pre-auth letter",
                "Inform anaesthetist of any allergies",
            ],
            "documents_needed": [
                "All X-rays and MRI films",
                "Blood test reports",
                "Physician clearance",
                "Insurance pre-authorisation",
                "Photo ID",
            ],
        },
        "post_op": {
            "in_hospital": [
                "Physiotherapy starts Day 1 post surgery",
                "Ankle pumping exercises to prevent blood clots",
                "Ice packs as advised for swelling",
                "Compression stockings to be worn as instructed",
                "Blood thinners will be given to prevent DVT — take as prescribed",
                "Do not bear weight until physiotherapist approves",
            ],
            "week_1_at_home": [
                "Continue all physiotherapy exercises exactly as taught",
                "Ice pack 20 minutes every 3-4 hours for swelling",
                "Keep leg elevated when resting",
                "Do not cross legs or sit on low chairs",
                "Use walker or crutches — do not walk unsupported",
                "Blood thinners must be continued as prescribed — critical",
                "Wound must be kept clean and dry",
            ],
            "week_2_6": [
                "Increase physiotherapy intensity as advised",
                "Gradually reduce walker dependence",
                "Swimming and cycling allowed after surgeon clearance",
                "No running or jumping for 3 months",
                "Weight loss important for joint longevity",
            ],
            "when_to_call_doctor": [
                "Calf pain, swelling, or redness — possible blood clot",
                "Fever above 38°C",
                "Wound opening or discharge",
                "Severe increase in joint pain",
                "Numbness or tingling in operated limb",
                "Difficulty breathing — emergency — go to hospital immediately",
            ],
            "follow_up_schedule": [
                "Day 2: Physiotherapy assessment",
                "Day 7: Wound check and suture removal",
                "Day 14: First post-op X-ray",
                "Week 6: Weight bearing assessment",
                "Month 3: Full activity clearance",
            ],
        },
    },

    "laparoscopic_surgery": {
        "name":     "Laparoscopic Surgery",
        "examples": ["laparoscopic cholecystectomy", "laparoscopic hernia", "laparoscopic appendectomy"],
        "pre_op": {
            "7_days_before": [
                "Stop smoking — significantly improves recovery",
                "Stop blood thinners if prescribed",
                "Liquid diet 2 days before surgery if advised by surgeon",
                "Bowel preparation if advised — follow instructions exactly",
                "All blood tests, ultrasound, and ECG must be complete",
            ],
            "night_before": [
                "Nil by mouth after midnight — no food, no water, no chewing gum",
                "Antiseptic shower",
                "Remove all piercings and jewellery",
                "Trim body hair at surgical site if asked",
            ],
            "day_of_surgery": [
                "Nil by mouth — strict",
                "Arrive 2 hours early",
                "Wear loose clothing — you will change into hospital gown",
                "Bring all reports and insurance documents",
                "Empty bowel if possible before leaving home",
            ],
            "documents_needed": [
                "Ultrasound/CT scan reports",
                "Blood test reports",
                "ECG",
                "Insurance pre-auth",
                "Photo ID",
            ],
        },
        "post_op": {
            "in_hospital": [
                "You may feel shoulder or back pain — this is gas pain, normal",
                "Start sips of water after 4 hours if no nausea",
                "Most patients go home same day or next day",
                "Walk gently as soon as you feel able",
                "Mild abdominal bloating is normal for 2-3 days",
            ],
            "week_1_at_home": [
                "Light diet only — dal, rice, khichdi, soups, fruits",
                "No spicy, oily, or heavy food for 2 weeks",
                "Small frequent meals better than large meals",
                "No heavy lifting — nothing over 2 kg",
                "Walking encouraged — 10-15 minutes 3 times daily",
                "Keep port sites clean and dry",
                "Mild pain at port sites is normal — take prescribed painkillers",
            ],
            "week_2_3": [
                "Gradually return to normal diet",
                "Light exercise — walking, gentle stretching",
                "Most patients return to desk work by Day 7-10",
                "Driving allowed after 2 weeks if no pain",
                "No gym or heavy exercise for 4-6 weeks",
            ],
            "when_to_call_doctor": [
                "Fever above 38°C",
                "Increasing abdominal pain",
                "Jaundice — yellow skin or eyes",
                "Port site redness, swelling, or discharge",
                "Inability to pass urine for more than 8 hours",
                "Persistent nausea and vomiting",
            ],
            "follow_up_schedule": [
                "Day 3: Wound check",
                "Day 7: Suture or clip removal",
                "Day 14: Post-op review with surgeon",
            ],
        },
    },

    "cardiac_surgery": {
        "name":     "Cardiac Surgery / Intervention",
        "examples": ["angioplasty", "bypass surgery", "valve replacement", "pacemaker"],
        "pre_op": {
            "7_days_before": [
                "Stop all blood thinners as per cardiologist instruction — critical",
                "Stop smoking immediately — minimum 2 weeks before",
                "Complete cardiac workup: ECG, Echo, angiogram as ordered",
                "Dental clearance mandatory — infection risk to heart valves",
                "Diabetics: strict blood sugar control — target HbA1c < 7.5",
                "Optimise blood pressure — target below 130/80",
                "Psychological preparation — discuss fears with doctor",
            ],
            "night_before": [
                "Nil by mouth after midnight",
                "Antiseptic bath",
                "Take only blood pressure and cardiac medications with sip of water — confirm with cardiologist",
                "Do NOT stop cardiac medications without specific instruction",
            ],
            "day_of_surgery": [
                "Take approved medications only with minimal water",
                "Arrive 3 hours before — cardiac cases need longer preparation",
                "Bring all cardiac reports: ECG, Echo, angiogram reports and CDs",
                "Bring insurance pre-auth — cardiac surgeries are high value claims",
                "Family member must be present throughout",
            ],
            "documents_needed": [
                "All ECG strips",
                "Echocardiogram report and CD",
                "Angiogram report and CD",
                "Blood test reports including coagulation profile",
                "Dental clearance certificate",
                "Diabetic HbA1c report",
                "Insurance pre-authorisation — must be in hand before surgery",
            ],
        },
        "post_op": {
            "in_hospital": [
                "ICU stay expected — typically 1-3 days post cardiac surgery",
                "Multiple lines and monitors — do not pull or adjust",
                "Breathing exercises are critical — start as soon as advised",
                "Cardiac rehabilitation begins in hospital",
                "Strict medication compliance from day 1",
                "Blood thinners started immediately — never miss a dose",
            ],
            "week_1_at_home": [
                "Complete bed rest with short supervised walks",
                "Cardiac medications must be taken on exact schedule — set alarms",
                "Monitor pulse daily — report if below 50 or above 100",
                "Monitor BP daily — report if above 150/90",
                "No driving, no lifting, no exertion",
                "Low sodium diet — avoid salt, pickles, papad, processed food",
                "Heart-healthy diet: fruits, vegetables, whole grains, fish",
                "Wound inspection daily — sternal wound must be kept dry",
            ],
            "month_1_3": [
                "Cardiac rehabilitation programme — attend all sessions",
                "Gradually increase walking: start 5 mins, build to 30 mins daily",
                "Monitor weight daily — gain of 2 kg in 2 days means fluid retention",
                "Strict diet compliance — no compromise",
                "No return to work before 6-8 weeks — desk job only initially",
                "No driving for 4-6 weeks minimum",
                "Sexual activity: typically safe after 6-8 weeks — confirm with cardiologist",
            ],
            "when_to_call_doctor": [
                "Chest pain — emergency — call ambulance immediately",
                "Difficulty breathing or shortness of breath",
                "Sudden weight gain of 2 kg in 2 days",
                "Fever above 38°C",
                "Sternal wound opening or discharge",
                "Palpitations or irregular heartbeat",
                "Swelling of legs",
                "Dizziness or fainting — emergency",
            ],
            "follow_up_schedule": [
                "Week 1: Wound check and blood tests",
                "Week 2: ECG and medication review",
                "Month 1: Full cardiac assessment",
                "Month 3: Stress test and echo",
                "Month 6: Annual cardiac review starts",
            ],
        },
    },
}

# Keyword mapping for surgery type detection
SURGERY_KEYWORDS = {
    "general_surgery":      ["hernia", "appendix", "appendicitis", "gallbladder", "cholecystectomy",
                             "abscess", "general surgery", "colostomy", "bowel", "intestine"],
    "orthopaedic_surgery":  ["knee", "hip", "joint", "bone", "fracture", "ortho", "arthroscopy",
                             "replacement", "spine", "disc", "shoulder", "ankle", "ligament"],
    "laparoscopic_surgery": ["laparoscopic", "laparoscopy", "keyhole", "minimally invasive",
                             "lap chole", "lap hernia", "lap appendix"],
    "cardiac_surgery":      ["heart", "cardiac", "bypass", "angioplasty", "valve", "pacemaker",
                             "stent", "coronary", "open heart", "cabg"],
}


def detect_surgery_type(description: str) -> str:
    desc_lower = description.lower()
    for surgery_type, keywords in SURGERY_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            return surgery_type
    return "general_surgery"


async def get_surgery_checklist(args: dict) -> dict:
    surgery_type = args.get("surgery_type", "general_surgery")
    phase        = args.get("phase", "pre_op")

    checklist_data = SURGICAL_CHECKLISTS.get(surgery_type, SURGICAL_CHECKLISTS["general_surgery"])

    if phase == "both":
        return {
            "status":       "success",
            "surgery_type": surgery_type,
            "surgery_name": checklist_data["name"],
            "pre_op":       checklist_data["pre_op"],
            "post_op":      checklist_data["post_op"],
        }

    section = checklist_data.get(phase)
    if not section:
        return {"status": "error", "message": f"Phase '{phase}' not found. Use pre_op, post_op, or both."}

    return {
        "status":       "success",
        "surgery_type": surgery_type,
        "surgery_name": checklist_data["name"],
        "phase":        phase,
        "checklist":    section,
    }


async def get_preop_documents(args: dict) -> dict:
    surgery_type  = args.get("surgery_type", "general_surgery")
    checklist_data = SURGICAL_CHECKLISTS.get(surgery_type, SURGICAL_CHECKLISTS["general_surgery"])
    docs = checklist_data["pre_op"].get("documents_needed", [])
    return {
        "status":       "success",
        "surgery_type": surgery_type,
        "surgery_name": checklist_data["name"],
        "documents":    docs,
    }


async def get_postop_warnings(args: dict) -> dict:
    surgery_type  = args.get("surgery_type", "general_surgery")
    checklist_data = SURGICAL_CHECKLISTS.get(surgery_type, SURGICAL_CHECKLISTS["general_surgery"])
    warnings = checklist_data["post_op"].get("when_to_call_doctor", [])
    return {
        "status":       "success",
        "surgery_type": surgery_type,
        "surgery_name": checklist_data["name"],
        "warnings":     warnings,
    }


async def get_followup_schedule(args: dict) -> dict:
    surgery_type  = args.get("surgery_type", "general_surgery")
    checklist_data = SURGICAL_CHECKLISTS.get(surgery_type, SURGICAL_CHECKLISTS["general_surgery"])
    schedule = checklist_data["post_op"].get("follow_up_schedule", [])
    return {
        "status":       "success",
        "surgery_type": surgery_type,
        "surgery_name": checklist_data["name"],
        "schedule":     schedule,
    }
