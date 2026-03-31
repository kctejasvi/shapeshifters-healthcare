"""
Shapeshifters Healthcare — Educational Tool
Medical myth busting, health tips, clinical guidelines, and Q&A.

All content is educational only. The bot must never give personalised advice.
Always redirect complex questions to Shapeshifters Consult.
"""

import os
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")

# ──────────────────────────────────────────────────────────────
# 1. MEDICAL TERMS — 20 terms across all 5 specialties
# ──────────────────────────────────────────────────────────────

MEDICAL_TERMS: dict[str, dict] = {
    # Diabetes
    "hba1c": {
        "simple": "HbA1c is a blood test that shows your average blood sugar level over the past 2–3 months. Think of it as your sugar 'report card'. A normal result is below 5.7%.",
        "who_needs_to_know": "Anyone with diabetes or at risk of diabetes.",
        "article_link": f"{BASE_URL}/thyroid-test-india",
        "specialty": "diabetes",
    },
    "insulin resistance": {
        "simple": "When your body's cells stop responding properly to insulin, the hormone that controls blood sugar. It's like a lock (cell) that ignores the key (insulin). This leads to higher blood sugar and is the root cause of Type 2 Diabetes.",
        "who_needs_to_know": "Patients with Type 2 Diabetes, PCOS, or obesity.",
        "article_link": f"{BASE_URL}/diabetes-diet-plan-india",
        "specialty": "diabetes",
    },
    "glucometer": {
        "simple": "A small handheld device that measures your blood sugar level from a drop of blood taken from your fingertip. Results come in under 10 seconds.",
        "who_needs_to_know": "All diabetes patients who monitor blood sugar at home.",
        "article_link": f"{BASE_URL}/diabetes-diet-plan-india",
        "specialty": "diabetes",
    },
    "glycaemic index": {
        "simple": "A score (0–100) that shows how quickly a food raises your blood sugar. White rice = 73 (high). Lentils = 32 (low). Low GI foods are better for diabetics.",
        "who_needs_to_know": "Diabetic patients and those following a weight-loss diet.",
        "article_link": f"{BASE_URL}/diabetes-diet-plan-india",
        "specialty": "diabetes",
    },
    # Oncology
    "biopsy": {
        "simple": "A procedure where a doctor takes a small piece of tissue from your body to examine under a microscope. It's the only definitive way to diagnose cancer.",
        "who_needs_to_know": "Anyone who has been told they may have cancer, or has a suspicious lump.",
        "article_link": f"{BASE_URL}/second-opinion-cancer-diagnosis-india",
        "specialty": "oncology",
    },
    "metastasis": {
        "simple": "When cancer spreads from its original location to other parts of the body — for example, breast cancer spreading to the lungs or liver. This is called Stage 4 cancer.",
        "who_needs_to_know": "Cancer patients and their families.",
        "article_link": f"{BASE_URL}/second-opinion-cancer-diagnosis-india",
        "specialty": "oncology",
    },
    "chemotherapy": {
        "simple": "A treatment that uses strong medicines to kill cancer cells. It works throughout the whole body (not just one area) and is often given as an intravenous drip at a hospital.",
        "who_needs_to_know": "Cancer patients who are about to start or considering chemotherapy.",
        "article_link": f"{BASE_URL}/best-oncologist-bangalore",
        "specialty": "oncology",
    },
    "remission": {
        "simple": "When cancer is no longer detectable in the body after treatment. 'Complete remission' means no cancer found. It doesn't always mean the cancer is cured permanently.",
        "who_needs_to_know": "Cancer patients and families.",
        "article_link": f"{BASE_URL}/cancer-screening-india",
        "specialty": "oncology",
    },
    # Surgery
    "laparoscopy": {
        "simple": "A type of surgery where the surgeon makes small cuts (instead of one large cut) and uses a tiny camera to see inside. Recovery is faster, with less pain and scarring than open surgery.",
        "who_needs_to_know": "Anyone scheduled for abdominal surgery.",
        "article_link": f"{BASE_URL}/laparoscopic-surgery-recovery",
        "specialty": "surgery",
    },
    "general anaesthesia": {
        "simple": "A medication that puts you into a deep, controlled sleep during surgery so you feel no pain and have no awareness of the procedure.",
        "who_needs_to_know": "Any patient undergoing surgery.",
        "article_link": f"{BASE_URL}/laparoscopic-surgery-recovery",
        "specialty": "surgery",
    },
    # Dermatology
    "retinoid": {
        "simple": "A family of compounds derived from Vitamin A that speed up skin cell turnover. They treat acne and reduce wrinkles. Tretinoin is the prescription-strength retinoid; retinol is the OTC version.",
        "who_needs_to_know": "Anyone using prescription or OTC skincare for acne or anti-ageing.",
        "article_link": f"{BASE_URL}/tretinoin-india-guide",
        "specialty": "dermatology",
    },
    "hyperpigmentation": {
        "simple": "Dark patches on skin caused by excess melanin (skin pigment). Common triggers: sun exposure, hormones (melasma), post-acne marks.",
        "who_needs_to_know": "Anyone with uneven skin tone, dark spots, or melasma.",
        "article_link": f"{BASE_URL}/dermatologist-acne-treatment-india",
        "specialty": "dermatology",
    },
    "niacinamide": {
        "simple": "A form of Vitamin B3 used in skincare that reduces redness, controls oil, and fades dark spots. It's gentle and suitable for all skin types, including sensitive skin.",
        "who_needs_to_know": "Anyone building a skincare routine for acne, oily skin, or pigmentation.",
        "article_link": f"{BASE_URL}/dermatologist-acne-treatment-india",
        "specialty": "dermatology",
    },
    # General Medicine
    "tsh": {
        "simple": "TSH (Thyroid Stimulating Hormone) is a blood test that checks how well your thyroid gland is working. High TSH = underactive thyroid (hypothyroidism). Low TSH = overactive thyroid (hyperthyroidism).",
        "who_needs_to_know": "Anyone with unexplained fatigue, weight changes, or a family history of thyroid disease.",
        "article_link": f"{BASE_URL}/thyroid-test-india",
        "specialty": "general",
    },
    "systolic vs diastolic": {
        "simple": "Blood pressure has two numbers: 120/80. The top number (systolic) is pressure when the heart beats. The bottom (diastolic) is pressure when it rests. Normal is below 120/80 mmHg.",
        "who_needs_to_know": "Anyone monitoring blood pressure at home.",
        "article_link": f"{BASE_URL}/blood-pressure-management-india",
        "specialty": "general",
    },
    "egfr": {
        "simple": "eGFR (estimated Glomerular Filtration Rate) is a blood test that measures how well your kidneys are filtering waste. A normal value is above 60. Below 30 means significant kidney disease.",
        "who_needs_to_know": "Diabetics, hypertension patients, anyone taking medications that affect the kidneys (like Metformin).",
        "article_link": f"{BASE_URL}/metformin-side-effects-india",
        "specialty": "general",
    },
    "creatinine": {
        "simple": "A waste product your kidneys filter from the blood. When kidneys aren't working well, creatinine builds up. Normal serum creatinine: 0.6–1.2 mg/dL (men), 0.5–1.1 mg/dL (women).",
        "who_needs_to_know": "Patients with diabetes, hypertension, or kidney disease.",
        "article_link": f"{BASE_URL}/metformin-side-effects-india",
        "specialty": "general",
    },
    "ecg": {
        "simple": "An ECG (Electrocardiogram) records the electrical activity of your heart via stickers placed on your chest, arms, and legs. It checks heart rhythm and detects heart attacks. The test takes under 5 minutes.",
        "who_needs_to_know": "Anyone with chest pain, palpitations, or undergoing surgery.",
        "article_link": f"{BASE_URL}/health-insurance-india-guide",
        "specialty": "general",
    },
    "cbc": {
        "simple": "CBC (Complete Blood Count) is a blood test that counts all types of blood cells — red cells (oxygen carriers), white cells (infection fighters), and platelets (clotting). It's the most commonly ordered blood test in India.",
        "who_needs_to_know": "Everyone — it's part of most health checkup panels.",
        "article_link": f"{BASE_URL}/thyroid-test-india",
        "specialty": "general",
    },
    "bmi": {
        "simple": "BMI (Body Mass Index) = weight (kg) ÷ height² (m²). For Indians, overweight is BMI ≥23 (lower than the international cut-off of 25) because Indians carry more abdominal fat at lower BMIs.",
        "who_needs_to_know": "Anyone assessing their weight and disease risk.",
        "article_link": f"{BASE_URL}/diabetes-diet-plan-india",
        "specialty": "general",
    },
}


def explain_medical_term(term: str) -> dict:
    """
    Explains a medical term in simple language.

    Args:
        term: Medical term string

    Returns:
        Dict with simple explanation, who needs to know, and article link
    """
    term_lower = term.lower().strip()

    # Exact match
    if term_lower in MEDICAL_TERMS:
        data = MEDICAL_TERMS[term_lower]
        return {
            "term": term,
            "found": True,
            **data,
            "disclaimer": "This explanation is educational only. Consult your doctor for clinical decisions.",
        }

    # Partial match
    for key, data in MEDICAL_TERMS.items():
        if term_lower in key or key in term_lower:
            return {
                "term": term,
                "found": True,
                **data,
                "disclaimer": "This explanation is educational only. Consult your doctor for clinical decisions.",
            }

    return {
        "term": term,
        "found": False,
        "message": f"Term '{term}' not in our database yet.",
        "suggestion": "Ask a specialist via Shapeshifters Consult.",
        "consult_url": f"{BASE_URL}/consult",
    }


# ──────────────────────────────────────────────────────────────
# 2. MYTH OR FACT — 15 health myths
# ──────────────────────────────────────────────────────────────

MYTHS: list[dict] = [
    {
        "statement": "Diabetes is caused by eating too much sugar",
        "verdict": "partial",
        "explanation": (
            "Sugar alone doesn't cause diabetes, but a sugar-heavy diet that leads to obesity does increase risk. "
            "Type 1 Diabetes is autoimmune — unrelated to diet. Type 2 Diabetes is driven by insulin resistance from "
            "excess body fat, poor diet, sedentary lifestyle, and genetics."
        ),
        "source": "ICMR, ADA 2023",
        "specialty": "diabetes",
    },
    {
        "statement": "Once you start insulin, you can never stop",
        "verdict": "myth",
        "explanation": (
            "Many Type 2 Diabetes patients who start insulin can later switch back to oral medications — or even achieve "
            "remission — through significant weight loss, diet changes, and exercise. Insulin is a tool, not a life sentence."
        ),
        "source": "RSSDI 2024, DiRECT Trial",
        "specialty": "diabetes",
    },
    {
        "statement": "Diabetics cannot eat rice",
        "verdict": "myth",
        "explanation": (
            "Rice can be part of a diabetic diet in moderate portions — especially if paired with dal, vegetables, and protein "
            "to reduce glycaemic impact. Switching to brown rice or small-grain varieties helps. Total carbohydrate portion "
            "control matters more than avoiding rice completely."
        ),
        "source": "RSSDI Dietary Guidelines",
        "specialty": "diabetes",
    },
    {
        "statement": "You can tell if someone has cancer just by looking at them",
        "verdict": "myth",
        "explanation": (
            "Most cancers show no external signs in early stages. Early-stage breast cancer, cervical cancer, and colon "
            "cancer often have no visible symptoms. This is why regular screening is essential — 'looking healthy' "
            "does not mean cancer-free."
        ),
        "source": "IARC / ICMR Cancer Report 2024",
        "specialty": "oncology",
    },
    {
        "statement": "Cancer is always fatal",
        "verdict": "myth",
        "explanation": (
            "Many cancers are highly curable when detected early. Stage 1 breast cancer has a 5-year survival rate >90%. "
            "Thyroid cancer has near 100% survival if caught early. Even some Stage 4 cancers are now managed as chronic "
            "conditions thanks to targeted therapies."
        ),
        "source": "ICMR Cancer Statistics 2024",
        "specialty": "oncology",
    },
    {
        "statement": "Laparoscopic surgery is riskier than open surgery",
        "verdict": "myth",
        "explanation": (
            "For most procedures (gallbladder removal, hernia repair, appendectomy), laparoscopic surgery is actually "
            "safer — with lower infection rates, less blood loss, shorter hospital stays, and faster recovery. "
            "Open surgery is still preferred for complex or emergency cases."
        ),
        "source": "Cochrane Review 2023, SAGES Guidelines",
        "specialty": "surgery",
    },
    {
        "statement": "You should avoid all fats if you have high cholesterol",
        "verdict": "myth",
        "explanation": (
            "Healthy fats (olive oil, nuts, avocado, fish) actually improve your cholesterol profile by raising HDL "
            "(good cholesterol). It's saturated fats (ghee in excess, red meat) and trans fats (vanaspati, fried snacks) "
            "that should be limited."
        ),
        "source": "AHA/ACC Dietary Guidelines",
        "specialty": "general",
    },
    {
        "statement": "Higher SPF sunscreen is always better",
        "verdict": "partial",
        "explanation": (
            "SPF 30 blocks ~97% of UVB; SPF 50 blocks ~98%; SPF 100 blocks ~99%. The difference above SPF 30 is marginal, "
            "but for Indian skin (which is prone to hyperpigmentation), SPF 50 with PA++++ is generally recommended. "
            "Re-application every 2–3 hours matters more than very high SPF."
        ),
        "source": "AAD Sunscreen Guidelines, Indian Dermatology Consensus",
        "specialty": "dermatology",
    },
    {
        "statement": "Moisturiser causes acne",
        "verdict": "myth",
        "explanation": (
            "The right moisturiser does not cause acne. In fact, skipping moisturiser can worsen acne by triggering excess "
            "oil production. Use non-comedogenic, oil-free moisturisers labelled suitable for oily/acne-prone skin."
        ),
        "source": "AAD Acne Guidelines",
        "specialty": "dermatology",
    },
    {
        "statement": "Thyroid disease only affects women",
        "verdict": "myth",
        "explanation": (
            "While thyroid disorders are 5–8x more common in women, men are also affected. Men with hypothyroidism often "
            "go undiagnosed because symptoms like fatigue and weight gain are attributed to other causes. "
            "Men with a family history or symptoms should get a TSH test."
        ),
        "source": "AACE Thyroid Guidelines",
        "specialty": "general",
    },
    {
        "statement": "Normal blood pressure is 120/80 for Indians too",
        "verdict": "partial",
        "explanation": (
            "While 120/80 mmHg is the international benchmark, Indian hypertension guidelines recommend treating at "
            ">130/80 mmHg in high-risk patients (diabetes, kidney disease, prior heart attack). "
            "Indians also develop cardiovascular risk at lower BMIs than Western populations."
        ),
        "source": "CSI Hypertension Guidelines 2023",
        "specialty": "general",
    },
    {
        "statement": "Antibiotics are effective against viral infections like the common cold",
        "verdict": "myth",
        "explanation": (
            "Antibiotics kill bacteria — they have zero effect on viruses. Taking antibiotics for a cold or flu "
            "does not help and contributes to antibiotic resistance, a major health crisis in India. "
            "Viral infections resolve on their own with rest and hydration."
        ),
        "source": "WHO Antimicrobial Resistance Report",
        "specialty": "general",
    },
    {
        "statement": "You don't need to see a doctor if you feel fine",
        "verdict": "myth",
        "explanation": (
            "Many serious conditions — hypertension, Type 2 Diabetes, early-stage cancer, chronic kidney disease — "
            "have no symptoms for years. Annual health checkups can detect these 'silent' conditions early when "
            "they are much easier to treat."
        ),
        "source": "ICMR Preventive Health Guidelines",
        "specialty": "general",
    },
    {
        "statement": "Vitamin C can prevent or cure COVID-19",
        "verdict": "myth",
        "explanation": (
            "There is no scientific evidence that Vitamin C prevents or treats COVID-19 or most other viral infections. "
            "While Vitamin C supports immune function, megadoses have not shown clinical benefit and can cause "
            "kidney stones at very high doses."
        ),
        "source": "Cochrane Review on Vitamin C and COVID-19",
        "specialty": "general",
    },
    {
        "statement": "Eating ghee is bad for heart health",
        "verdict": "partial",
        "explanation": (
            "Ghee in small amounts (1–2 teaspoons/day) is not harmful for most people. It contains butyric acid "
            "which may benefit gut health. However, ghee is high in saturated fat and should be limited for those "
            "with high LDL cholesterol or cardiovascular disease. Moderation is key."
        ),
        "source": "Indian Heart Journal, Dietary Guidelines ICMR",
        "specialty": "general",
    },
]


def myth_or_fact(statement: str) -> dict:
    """
    Takes a health myth statement and returns verdict, explanation, and source.

    Args:
        statement: The health claim to evaluate

    Returns:
        Dict with verdict ('myth'/'fact'/'partial'), explanation, source
    """
    stmt_lower = statement.lower().strip()

    # Search by keywords in the statement
    best_match = None
    best_score = 0

    for myth in MYTHS:
        myth_words = set(myth["statement"].lower().split())
        query_words = set(stmt_lower.split())
        overlap = len(myth_words & query_words)
        if overlap > best_score:
            best_score = overlap
            best_match = myth

    if best_match and best_score >= 2:
        verdict_emoji = {"myth": "❌", "fact": "✅", "partial": "⚠️"}.get(best_match["verdict"], "ℹ️")
        return {
            "found": True,
            "statement": best_match["statement"],
            "verdict": best_match["verdict"],
            "verdict_display": f"{verdict_emoji} {best_match['verdict'].upper()}",
            "explanation": best_match["explanation"],
            "source": best_match["source"],
            "specialty": best_match["specialty"],
            "disclaimer": "Always verify health information with a qualified doctor.",
        }

    return {
        "found": False,
        "statement": statement,
        "message": "We couldn't find a match for this statement in our myth database.",
        "suggestion": "Ask a Shapeshifters specialist for an evidence-based answer.",
        "consult_url": f"{BASE_URL}/consult",
    }


# ──────────────────────────────────────────────────────────────
# 3. DAILY HEALTH TIPS — 30 tips across 5 specialties
# ──────────────────────────────────────────────────────────────

HEALTH_TIPS: list[dict] = [
    # Diabetes (6 tips)
    {"specialty": "diabetes", "audience": "patient", "tip": "Check your blood sugar 2 hours after meals, not just fasting — post-meal spikes are a key driver of HbA1c.", "affiliate_product": "glucometer", "affiliate_copy": "Dr. Morepen Glucometer — monitor post-meal glucose at home"},
    {"specialty": "diabetes", "audience": "patient", "tip": "Walking for just 10 minutes after each meal can reduce your post-meal blood sugar by 20–30%. No gym required.", "affiliate_product": "lab_tests_thyrocare", "affiliate_copy": "Track your HbA1c every 3 months — Thyrocare ₹249"},
    {"specialty": "diabetes", "audience": "patient", "tip": "Eat protein and vegetables before rice or roti. The sequence of eating reduces the glycaemic impact of your meal.", "affiliate_product": "lab_tests_thyrocare", "affiliate_copy": "Full Diabetes Panel at home — Thyrocare ₹499"},
    {"specialty": "diabetes", "audience": "patient", "tip": "Metformin is best taken with the first bite of food — not after — to reduce nausea and GI side effects.", "affiliate_product": "pharmacy_1mg", "affiliate_copy": "Get your diabetes medications delivered home — 1mg pharmacy"},
    {"specialty": "diabetes", "audience": "doctor", "tip": "For patients with Type 2 DM + CKD (eGFR 30–45), empagliflozin is preferred over SGLT-2 alternatives for cardio-renal protection (RSSDI 2024).", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Shapeshifters Academy — Diabetes & CKD CME module, 2 credits"},
    {"specialty": "diabetes", "audience": "doctor", "tip": "Time-in-Range (TIR) >70% on CGM correlates with lower HbA1c and complication risk. Target TIR >70% for Type 1, >50% for frail elderly Type 2.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "CGM Interpretation Course — Shapeshifters Academy"},
    # Oncology (6 tips)
    {"specialty": "oncology", "audience": "patient", "tip": "Women aged 40–69 should get a mammogram every 1–2 years. Early-stage breast cancer has >90% survival. Don't delay your screening.", "affiliate_product": "lab_tests_thyrocare", "affiliate_copy": "Cancer Screening Panel at home — Thyrocare ₹1499"},
    {"specialty": "oncology", "audience": "patient", "tip": "The HPV vaccine is recommended for women up to age 45 who haven't received it yet. It prevents cervical cancer — India's 2nd most common cancer in women.", "affiliate_product": "health_insurance_niva_bupa", "affiliate_copy": "Cover cancer treatment — Niva Bupa Critical Illness Plan"},
    {"specialty": "oncology", "audience": "patient", "tip": "If you're diagnosed with cancer, always get a second opinion before starting treatment. Studies show 30% of diagnoses change with a second pathology review.", "affiliate_product": "second_opinion", "affiliate_copy": "Get a second oncology opinion online — Shapeshifters Consult"},
    {"specialty": "oncology", "audience": "patient", "tip": "Avoid tobacco in all forms — it accounts for 30% of all cancers in India. Oral tobacco (gutka, paan masala) is the leading cause of oral cancer.", "affiliate_product": "health_insurance_niva_bupa", "affiliate_copy": "Protect yourself with health insurance — Niva Bupa"},
    {"specialty": "oncology", "audience": "doctor", "tip": "For suspected pancreatic adenocarcinoma, CA 19-9 alone has poor specificity. Always combine with CT/MRI. Only useful for monitoring — not diagnosis.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Shapeshifters Academy — Oncology Fundamentals CME"},
    {"specialty": "oncology", "audience": "doctor", "tip": "Febrile neutropenia (ANC <500, temp >38.3°C) in a chemo patient is an oncological emergency. Start empiric IV antibiotics within 1 hour — don't wait for culture results.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Oncology Emergencies CME — Shapeshifters Studios"},
    # Surgery (6 tips)
    {"specialty": "surgery", "audience": "patient", "tip": "After laparoscopic surgery, walk for 5 minutes every 2–3 hours from Day 1. Early movement prevents blood clots and speeds recovery.", "affiliate_product": "health_insurance_niva_bupa", "affiliate_copy": "Cashless surgery at 10,000+ hospitals — Niva Bupa"},
    {"specialty": "surgery", "audience": "patient", "tip": "If you have a hernia that's not causing symptoms, watchful waiting is a safe option. Elective repair is best before it becomes an emergency.", "affiliate_product": "second_opinion", "affiliate_copy": "Get a surgical second opinion online — Shapeshifters Consult"},
    {"specialty": "surgery", "audience": "patient", "tip": "Stop iron supplements at least a week before elective surgery. They can interfere with anaesthesia and cause GI issues post-op.", "affiliate_product": "pharmacy_1mg", "affiliate_copy": "Pre-surgery medication review — 1mg pharmacy"},
    {"specialty": "surgery", "audience": "patient", "tip": "Ask your surgeon specifically: 'Is this surgery keyhole (laparoscopic) or open? Why?' The answer should be explained clearly before you consent.", "affiliate_product": "second_opinion", "affiliate_copy": "Talk to a surgeon online before deciding — Shapeshifters Consult"},
    {"specialty": "surgery", "audience": "doctor", "tip": "For emergency appendicectomy in pregnant patients, laparoscopy is safe up to 28 weeks and preferred over open surgery due to lower complication rates.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "NEET PG Surgery — High-Yield Module, Shapeshifters Academy"},
    {"specialty": "surgery", "audience": "doctor", "tip": "Enhanced Recovery After Surgery (ERAS) protocol: allow water up to 2 hours pre-op (not 6 hours fasting for liquids). Reduces dehydration, nausea, and LOS.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Surgery CME — Shapeshifters Academy"},
    # Dermatology (6 tips)
    {"specialty": "dermatology", "audience": "patient", "tip": "Apply sunscreen as the LAST step of your morning routine — after moisturiser, before makeup. Reapply every 2–3 hours outdoors.", "affiliate_product": "skincare", "affiliate_copy": "Minimalist SPF 50 PA++++ — lightweight, non-greasy, ₹399"},
    {"specialty": "dermatology", "audience": "patient", "tip": "If you're starting tretinoin, begin 2–3 nights per week. Going daily immediately causes severe dryness. Build up over 4–6 weeks.", "affiliate_product": "pharmacy_1mg", "affiliate_copy": "Get prescription tretinoin delivered — 1mg pharmacy"},
    {"specialty": "dermatology", "audience": "patient", "tip": "For acne scars and pigmentation, vitamin C serum in the morning + niacinamide at night is a budget-friendly evidence-based combo.", "affiliate_product": "skincare", "affiliate_copy": "Minimalist Vitamin C 10% + Niacinamide 10% — from ₹299"},
    {"specialty": "dermatology", "audience": "patient", "tip": "Never pop or pick at pimples. It pushes bacteria deeper, worsens inflammation, and creates post-inflammatory hyperpigmentation that takes months to fade.", "affiliate_product": "skincare", "affiliate_copy": "Minimalist Salicylic Acid 2% — spot treatment for active acne, ₹299"},
    {"specialty": "dermatology", "audience": "doctor", "tip": "For seborrhoeic dermatitis, ketoconazole 2% shampoo used as a face wash 3x/week is highly effective and often under-prescribed in primary care.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Dermatology for Primary Care — Shapeshifters Academy"},
    {"specialty": "dermatology", "audience": "doctor", "tip": "In Indian skin (Fitzpatrick IV–VI), the ABCDE rule for melanoma is less sensitive. Look for 'ugly duckling' lesions — any lesion that looks different from surrounding moles.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Dermoscopy for Generalists — Shapeshifters Studios CME"},
    # General Medicine (6 tips)
    {"specialty": "general", "audience": "patient", "tip": "Get a blood pressure reading at least once a year if you're over 30. Hypertension has no symptoms — 50% of Indians with high BP don't know they have it.", "affiliate_product": "glucometer", "affiliate_copy": "Dr. Morepen BP Monitor — automatic, validated, ₹899"},
    {"specialty": "general", "audience": "patient", "tip": "Take levothyroxine (thyroid medicine) on an empty stomach, 30–60 minutes before breakfast — NEVER with milk, tea, or calcium tablets. Absorption drops by 40% otherwise.", "affiliate_product": "pharmacy_1mg", "affiliate_copy": "Thyroid medications — Thyronorm / Eltroxin on 1mg"},
    {"specialty": "general", "audience": "patient", "tip": "A full health checkup after age 30 should include: CBC, fasting glucose, HbA1c, lipid profile, thyroid (TSH), kidney function (creatinine, eGFR), and blood pressure.", "affiliate_product": "lab_tests_thyrocare", "affiliate_copy": "Comprehensive health package — Thyrocare, at-home collection ₹999"},
    {"specialty": "general", "audience": "patient", "tip": "Drink water first thing in the morning — before tea or coffee. Even mild dehydration raises cortisol and makes you feel more tired and anxious.", "affiliate_product": "lab_tests_thyrocare", "affiliate_copy": "Check your kidney health — Thyrocare KFT at home ₹299"},
    {"specialty": "general", "audience": "doctor", "tip": "For a patient starting a new ACE inhibitor, recheck potassium and creatinine at 1–2 weeks. A creatinine rise of up to 30% is acceptable — above that, reduce dose or switch.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Hypertension Management CME — Shapeshifters Academy"},
    {"specialty": "general", "audience": "doctor", "tip": "Metformin should be held 48 hours before and after any iodinated contrast procedure (CT with contrast). Restart only after confirming renal function is stable.", "affiliate_product": "shapeshifters_academy", "affiliate_copy": "Diabetes & Contrast Safety — Shapeshifters Academy CME"},
]


def get_daily_health_tip(specialty: str | None = None, audience: str | None = None) -> dict:
    """
    Returns one health tip, rotating daily based on the current date.

    Args:
        specialty: Filter by specialty
        audience: 'patient' or 'doctor'

    Returns:
        Dict with tip, specialty, affiliate suggestion
    """
    tips = HEALTH_TIPS.copy()

    if specialty:
        tips = [t for t in tips if t["specialty"] == specialty.lower()]
    if audience:
        tips = [t for t in tips if t["audience"] == audience.lower()]

    if not tips:
        tips = HEALTH_TIPS  # fallback to all

    # Rotate by day of year
    day_of_year = datetime.now().timetuple().tm_yday
    tip = tips[day_of_year % len(tips)]

    from .affiliate import get_affiliate_link
    affiliate_link = get_affiliate_link(tip["affiliate_product"])

    return {
        "tip": tip["tip"],
        "specialty": tip["specialty"],
        "audience": tip["audience"],
        "affiliate_copy": tip["affiliate_copy"],
        "affiliate_link": affiliate_link,
        "date": datetime.now().strftime("%d %B %Y"),
    }


# ──────────────────────────────────────────────────────────────
# 4. CLINICAL GUIDELINES — 10 guidelines
# ──────────────────────────────────────────────────────────────

CLINICAL_GUIDELINES: dict[str, dict] = {
    "diabetes_type2": {
        "specialty": "diabetes",
        "title": "Type 2 Diabetes Management — RSSDI/ICMR 2024 Summary",
        "audience": "doctor",
        "key_points": [
            "First-line: Metformin (unless eGFR <30 or contrast procedure planned)",
            "HbA1c target: <7% for most; <8% for elderly/frail; <6.5% for young low-risk",
            "Add GLP-1 (semaglutide/liraglutide) if obesity + high CV risk",
            "Add SGLT-2 (empagliflozin/dapagliflozin) if HF or CKD present",
            "Insulin: start if HbA1c >10% or symptomatic hyperglycaemia",
            "Screening: retina annually, foot monthly, nephropathy annually, lipids annually",
        ],
        "full_guideline_url": "https://rssdi.in/guidelines",
        "academy_cta": f"{BASE_URL}/academy/diabetes-management",
    },
    "hypertension": {
        "specialty": "general",
        "title": "Hypertension Management — CSI 2023 Summary",
        "audience": "doctor",
        "key_points": [
            "Target BP: <130/80 mmHg for most; <140/90 for elderly (>65)",
            "First-line: ACE inhibitor OR ARB (not both); CCB; thiazide diuretic",
            "In diabetics + proteinuria: ACE/ARB is mandatory",
            "Check electrolytes and creatinine 1–2 weeks after starting ACE/ARB",
            "Resistant hypertension: add spironolactone as 4th agent",
            "Lifestyle: reduce sodium (<2g/day), DASH diet, exercise 150 min/week",
        ],
        "full_guideline_url": "https://cardiologysocietyofindia.org",
        "academy_cta": f"{BASE_URL}/academy",
    },
    "acne": {
        "specialty": "dermatology",
        "title": "Acne Vulgaris Management — IADVL 2023 Summary",
        "audience": "doctor",
        "key_points": [
            "Mild acne: topical retinoid + benzoyl peroxide OR topical clindamycin",
            "Moderate acne: add oral doxycycline (100 mg BD) for 3 months max",
            "Severe / nodulocystic: oral isotretinoin (0.5–1 mg/kg/day)",
            "Isotretinoin: mandatory pregnancy test (2 negative), monthly liver and lipids",
            "Never use oral antibiotics as monotherapy — always combine with topical",
            "Maintenance after treatment: retinoid + azelaic acid",
        ],
        "full_guideline_url": "https://iadvl.org",
        "academy_cta": f"{BASE_URL}/academy/dermatology-primary-care",
    },
    "thyroid_hypothyroidism": {
        "specialty": "general",
        "title": "Hypothyroidism Management — AACE/ETA 2023 Summary",
        "audience": "doctor",
        "key_points": [
            "Start levothyroxine at 1.6 mcg/kg/day (lower in elderly, cardiac patients)",
            "Recheck TSH 6–8 weeks after any dose change",
            "Target TSH: 0.5–2.5 mIU/L for most; 0.5–1.5 in symptomatic patients",
            "Always take on empty stomach; avoid co-administration with iron, calcium",
            "Subclinical hypothyroidism (TSH 4–10): treat if symptomatic, pregnant, or atherogenic risk",
            "In pregnancy: start immediately if TSH >2.5; target TSH <2.5 in T1",
        ],
        "full_guideline_url": "https://aace.com/thyroid",
        "academy_cta": f"{BASE_URL}/academy",
    },
    "cancer_screening": {
        "specialty": "oncology",
        "title": "Cancer Screening Recommendations for India — ICMR 2023",
        "audience": "doctor",
        "key_points": [
            "Cervical: VIA screening every 5 years from age 30 (or HPV DNA test every 5 years)",
            "Breast: Clinical breast exam annually >40; mammogram every 2 years 40–69",
            "Oral: Annual oral cavity exam for all tobacco users",
            "Colorectal: FOBT annually or colonoscopy every 10 years from age 45",
            "Prostate: Discuss PSA with patient from age 50 (shared decision making)",
            "Lung: LDCT for 50+ with 20 pack-year smoking history (high-risk only)",
        ],
        "full_guideline_url": "https://icmr.gov.in",
        "academy_cta": f"{BASE_URL}/academy/oncology-fundamentals",
    },
    "surgery_antibiotic_prophylaxis": {
        "specialty": "surgery",
        "title": "Surgical Antibiotic Prophylaxis — WHO/Indian Guidelines",
        "audience": "doctor",
        "key_points": [
            "Give prophylactic antibiotic within 60 minutes before incision (not earlier)",
            "Cefazolin 2g IV is first-line for most clean and clean-contaminated cases",
            "Single dose is sufficient for most procedures <3 hours",
            "Redose if surgery >4 hours or blood loss >1500 mL",
            "Beta-lactam allergy: clindamycin + gentamicin OR vancomycin",
            "Do NOT continue prophylaxis beyond 24 hours post-op",
        ],
        "full_guideline_url": "https://who.int/publications/surgical-site-infections",
        "academy_cta": f"{BASE_URL}/academy",
    },
    "diabetes_feet": {
        "specialty": "diabetes",
        "title": "Diabetic Foot Care — IDF / RSSDI Guidelines",
        "audience": "doctor",
        "key_points": [
            "Examine feet at every clinic visit: neuropathy (monofilament), vascularity (dorsalis pedis)",
            "Annual foot risk stratification: Low (normal exam) / Moderate / High / Ulcer present",
            "Educate: daily foot inspection, no barefoot walking, proper footwear",
            "Wagner Grade 1–2 ulcer: offloading (TCC or CROW boot) + wound care + antibiotics if infected",
            "Wagner Grade 3+: vascular assessment; consider revascularisation before amputation",
            "Refer to multidisciplinary foot team if any ulcer or Charcot foot",
        ],
        "full_guideline_url": "https://idf.org/diabetic-foot",
        "academy_cta": f"{BASE_URL}/academy/diabetes-management",
    },
    "dermatology_steroid_ladder": {
        "specialty": "dermatology",
        "title": "Topical Corticosteroid Ladder — IADVL Consensus",
        "audience": "doctor",
        "key_points": [
            "Group 1 (very potent): clobetasol — body only, max 2 weeks continuous",
            "Group 2 (potent): betamethasone dipropionate — body, short-term",
            "Group 3 (moderate): betamethasone valerate — body; triamcinolone",
            "Group 4 (mild): hydrocortisone 1% — face, flexures, genitals, children",
            "NEVER use potent steroids on face, groin, or axilla",
            "Steroid withdrawal: taper, don't stop abruptly (rebound flare risk)",
        ],
        "full_guideline_url": "https://iadvl.org",
        "academy_cta": f"{BASE_URL}/academy/dermatology-primary-care",
    },
    "oncology_pain": {
        "specialty": "oncology",
        "title": "Cancer Pain Management — WHO Analgesic Ladder",
        "audience": "doctor",
        "key_points": [
            "Step 1 (mild pain): Non-opioids — paracetamol ± NSAID",
            "Step 2 (moderate): Weak opioid — tramadol or codeine + non-opioid",
            "Step 3 (severe): Strong opioid — oral morphine, oxycodone, or fentanyl patch",
            "Always prescribe regular dosing + rescue dose (1/6th of 24h dose PRN)",
            "Add laxative prophylactically with any opioid",
            "Neuropathic pain: add gabapentin or amitriptyline alongside opioid",
        ],
        "full_guideline_url": "https://who.int/cancer/palliative/painladder",
        "academy_cta": f"{BASE_URL}/academy/oncology-fundamentals",
    },
    "general_chest_pain": {
        "specialty": "general",
        "title": "Acute Chest Pain Assessment in Primary Care — ESC / API Guidelines",
        "audience": "doctor",
        "key_points": [
            "Any chest pain: 12-lead ECG within 10 minutes of presentation",
            "High-risk features: pain >20 min, radiation to jaw/left arm, sweating, hypotension",
            "Troponin I at 0h and 3h; HEART score to risk stratify",
            "STEMI: activate cath lab immediately; thrombolyse if PCI >120 min away",
            "NSTEMI/UA: aspirin 300mg + ticagrelor 180mg + fondaparinux immediately",
            "Non-cardiac mimics: GERD, costochondritis, anxiety — diagnosis of exclusion only",
        ],
        "full_guideline_url": "https://escardio.org/acs-guidelines",
        "academy_cta": f"{BASE_URL}/academy",
    },
}


def get_clinical_guideline(specialty: str, topic: str) -> dict:
    """
    Returns simplified clinical guideline for a specialty/topic combination.

    Args:
        specialty: e.g. 'diabetes', 'oncology', 'surgery', 'dermatology', 'general'
        topic: e.g. 'hypertension', 'acne', 'type2'

    Returns:
        Dict with key_points, full_guideline_url, academy_cta
    """
    query = f"{specialty}_{topic}".lower().strip().replace(" ", "_")

    # Exact key match
    if query in CLINICAL_GUIDELINES:
        guideline = CLINICAL_GUIDELINES[query]
        return {"found": True, **guideline}

    # Search by keywords
    for key, guideline in CLINICAL_GUIDELINES.items():
        if topic.lower() in key or specialty.lower() in key:
            return {"found": True, **guideline}

    # Specialty-only fallback
    specialty_matches = {k: v for k, v in CLINICAL_GUIDELINES.items() if v["specialty"] == specialty.lower()}
    if specialty_matches:
        first = list(specialty_matches.values())[0]
        return {"found": True, "note": "Closest match for specialty", **first}

    return {
        "found": False,
        "message": f"No guideline found for {specialty} / {topic}.",
        "suggestion": "Browse all guidelines on Shapeshifters Academy.",
        "academy_url": f"{BASE_URL}/academy",
    }


# ──────────────────────────────────────────────────────────────
# 5. HEALTH Q&A — 25 pre-built question/answer pairs
# ──────────────────────────────────────────────────────────────

QA_DATABASE: list[dict] = [
    # Diabetes
    {"question": "what is normal blood sugar level", "keywords": ["normal", "blood sugar", "glucose", "fasting"], "answer": "Fasting blood glucose: 70–99 mg/dL (normal). 100–125 mg/dL = pre-diabetes. 126 mg/dL or above on two tests = diabetes. Post-meal (2 hours): below 140 mg/dL is normal.", "specialty": "diabetes"},
    {"question": "can diabetes be reversed", "keywords": ["reverse", "diabetes", "cure", "remission"], "answer": "Type 2 Diabetes can go into remission with significant weight loss (15%+ body weight), low-calorie diet, and exercise. This is not a cure — blood sugar can rise again if weight is regained. Type 1 Diabetes cannot be reversed.", "specialty": "diabetes"},
    {"question": "what foods should a diabetic avoid", "keywords": ["food", "avoid", "diabetic", "eat"], "answer": "Limit: white rice (large portions), white bread/maida, fruit juices, sugary drinks, deep-fried foods, full-fat dairy. Prefer: millets, brown rice, dals, non-starchy vegetables, lean protein, healthy fats.", "specialty": "diabetes"},
    {"question": "how often should I check hba1c", "keywords": ["hba1c", "how often", "check", "frequency"], "answer": "If your diabetes is well-controlled (HbA1c at target): test every 6 months. If you recently changed medication, started insulin, or are not at target: every 3 months.", "specialty": "diabetes"},
    {"question": "is metformin safe for kidneys", "keywords": ["metformin", "kidney", "safe", "renal"], "answer": "Metformin is safe when kidney function (eGFR) is above 45. It must be reduced or stopped if eGFR drops below 45, and stopped completely below 30. Your doctor will monitor kidney function annually.", "specialty": "diabetes"},
    # Cancer
    {"question": "what are early signs of cancer", "keywords": ["early signs", "cancer", "symptoms", "warning"], "answer": "7 warning signs (CAUTION): Change in bowel/bladder habits, A sore that doesn't heal, Unusual bleeding or discharge, Thickening or lump, Indigestion or difficulty swallowing, Obvious change in a wart or mole, Nagging cough or hoarseness. These don't always mean cancer — but see a doctor promptly.", "specialty": "oncology"},
    {"question": "how is cancer diagnosed", "keywords": ["diagnose", "diagnosis", "cancer", "test"], "answer": "Cancer diagnosis requires a biopsy (tissue sample) for confirmation. Imaging (CT, MRI, PET scan) shows location and spread. Blood markers (CA125, CEA, PSA) support — but cannot confirm — diagnosis alone.", "specialty": "oncology"},
    {"question": "what is chemotherapy", "keywords": ["chemotherapy", "chemo", "what is"], "answer": "Chemotherapy uses drugs to kill fast-dividing cancer cells. It's given as IV infusion or tablets, usually in cycles with rest periods. Common side effects: nausea, hair loss, fatigue, infection risk. Modern anti-nausea drugs have made it much more tolerable.", "specialty": "oncology"},
    {"question": "can I get a second opinion for cancer", "keywords": ["second opinion", "cancer", "diagnosis"], "answer": "Yes — and you should. Studies show that 30% of cancer diagnoses change after a second pathology review. Second opinions are standard in oncology, not an insult to your doctor. Shapeshifters Consult can connect you with a senior oncologist online.", "specialty": "oncology"},
    # Surgery
    {"question": "how long does recovery take after gallbladder surgery", "keywords": ["gallbladder", "recovery", "surgery", "cholecystectomy"], "answer": "Laparoscopic gallbladder removal: return home same day or next day. Resume light activities in 1 week. Full recovery in 2–4 weeks. Open surgery: 2–3 days hospital stay, 4–6 weeks full recovery.", "specialty": "surgery"},
    {"question": "what should I eat after abdominal surgery", "keywords": ["eat", "diet", "after surgery", "abdominal"], "answer": "Start with clear liquids, progress to soft foods (khichdi, curd rice, boiled vegetables) over 3–5 days. Avoid high-fibre foods initially. Resume normal diet by week 2–3 unless instructed otherwise.", "specialty": "surgery"},
    {"question": "is laparoscopic surgery safe", "keywords": ["laparoscopic", "keyhole", "safe", "risk"], "answer": "For most common procedures (appendix, gallbladder, hernia), laparoscopic surgery is very safe with lower complication rates than open surgery. Serious complications are rare (<1–2%). Discuss your specific case with your surgeon.", "specialty": "surgery"},
    # Dermatology
    {"question": "how do I get rid of acne scars", "keywords": ["acne scars", "remove", "treat", "marks"], "answer": "For post-inflammatory hyperpigmentation (dark spots): vitamin C + niacinamide + sunscreen daily, 3–6 months. For atrophic scars (pitted): dermatologist procedures — microneedling, chemical peels, laser. Never expect overnight results.", "specialty": "dermatology"},
    {"question": "what causes hair fall in India", "keywords": ["hair fall", "hair loss", "cause", "alopecia"], "answer": "Common causes: iron deficiency anaemia, thyroid disease (hypothyroidism), PCOS, Vitamin D deficiency, stress (telogen effluvium), and genetic male/female pattern baldness. Get a blood panel (CBC, TSH, ferritin, Vitamin D) before starting any treatment.", "specialty": "dermatology"},
    {"question": "is tretinoin safe for Indian skin", "keywords": ["tretinoin", "Indian skin", "safe", "dark skin"], "answer": "Yes, but Indian skin (Fitzpatrick IV–VI) is more prone to irritation and post-inflammatory pigmentation during the adjustment phase. Start with 0.025%, use every other night, always pair with moisturiser and SPF 50. Build up slowly over 6–8 weeks.", "specialty": "dermatology"},
    {"question": "best sunscreen for Indian skin", "keywords": ["sunscreen", "Indian skin", "SPF", "best"], "answer": "For Indian skin: SPF 50 PA++++ minimum. Look for broad-spectrum UVA + UVB protection. Good drugstore options: Minimalist SPF 50, La Shield, Lotus Safe Sun, ISDIN Eryfotona. Reapply every 2–3 hours outdoors.", "specialty": "dermatology"},
    # General Medicine
    {"question": "what is normal blood pressure", "keywords": ["normal", "blood pressure", "BP", "reading"], "answer": "Normal: below 120/80 mmHg. Elevated: 120–129 / <80. High blood pressure (Stage 1): 130–139 / 80–89. High (Stage 2): 140+/90+. Hypertensive crisis: >180/120 (seek emergency care immediately).", "specialty": "general"},
    {"question": "how to control high blood pressure without medicine", "keywords": ["blood pressure", "control", "without medicine", "lifestyle"], "answer": "Lifestyle changes can reduce BP by 10–20 mmHg: reduce salt (<2g/day), DASH diet, exercise 30 min/day 5 days/week, quit smoking, limit alcohol, reduce weight (every 1kg lost reduces BP ~1 mmHg). If BP is stage 2+, medication is usually needed alongside.", "specialty": "general"},
    {"question": "what are symptoms of hypothyroidism", "keywords": ["hypothyroidism", "symptoms", "thyroid", "underactive"], "answer": "Symptoms: unexplained weight gain, fatigue, feeling cold, constipation, dry skin and hair, depression, slow heart rate, puffy face, brain fog. A simple TSH blood test diagnoses it. Treatment: daily levothyroxine tablet.", "specialty": "general"},
    {"question": "what tests should I do every year", "keywords": ["annual", "yearly", "tests", "checkup", "health"], "answer": "Annual health checkup over age 30: CBC, fasting blood glucose, HbA1c, lipid profile, TSH, creatinine + eGFR, urine routine, blood pressure measurement. Over 40: add ECG. Over 50: add colonoscopy/FOBT, mammogram (women), PSA discussion (men).", "specialty": "general"},
    {"question": "is it safe to take paracetamol every day", "keywords": ["paracetamol", "daily", "safe", "everyday"], "answer": "Paracetamol is safe at recommended doses (500–1000 mg per dose, max 4g/day) for most adults. Daily use for chronic pain is not recommended without a doctor's guidance. High doses or regular use with alcohol can damage the liver.", "specialty": "general"},
    {"question": "what causes anaemia", "keywords": ["anaemia", "low haemoglobin", "tired", "cause"], "answer": "Common causes in India: iron deficiency (most common, especially in women), Vitamin B12 deficiency, folate deficiency, thalassemia, chronic disease. A CBC + peripheral smear will identify the type. Treatment depends on cause — iron tablets alone aren't always the answer.", "specialty": "general"},
    {"question": "how do I know if I need health insurance", "keywords": ["health insurance", "need", "why"], "answer": "If a single hospitalisation (appendix surgery ₹80,000–1.5L; heart attack 3–8L; cancer treatment 5–20L) would financially stress your household — you need health insurance. Buying before any diagnosis is critical; insurers exclude pre-existing conditions.", "specialty": "general"},
    {"question": "can I buy medicines without prescription in India", "keywords": ["prescription", "without", "medicine", "OTC"], "answer": "Medicines in India are classified: OTC (Schedule K) — no prescription needed (e.g. paracetamol, antacids). Schedule H — prescription mandatory (e.g. antibiotics, most diabetes drugs, tretinoin). Schedule H1 — restricted (e.g. certain antibiotics). Buying Schedule H drugs without prescription is illegal and risky.", "specialty": "general"},
    {"question": "what is the best time to take blood pressure medicine", "keywords": ["blood pressure", "medicine", "time", "when to take"], "answer": "Most BP medicines are once-daily. Amlodipine and most ARBs can be taken at any time. ACE inhibitors may cause morning cough — some doctors prescribe at night. New evidence suggests taking at least one BP medication at bedtime reduces cardiovascular events. Ask your doctor what's best for your specific drug.", "specialty": "general"},
]


def ask_health_question(question: str, audience: str = "patient") -> dict:
    """
    Matches a question to the best pre-built answer.
    Falls back to Consult CTA if no match found.

    Args:
        question: User's question string
        audience: 'patient' or 'doctor'

    Returns:
        Dict with answer or CTA
    """
    question_lower = question.lower().strip()
    question_words = set(question_lower.split())

    best_match = None
    best_score = 0

    for qa in QA_DATABASE:
        # Score = keyword overlaps + question similarity
        keyword_score = sum(1 for kw in qa["keywords"] if kw.lower() in question_lower)
        question_words_qa = set(qa["question"].split())
        word_overlap = len(question_words & question_words_qa)
        total_score = keyword_score * 2 + word_overlap

        if total_score > best_score:
            best_score = total_score
            best_match = qa

    if best_match and best_score >= 2:
        return {
            "found": True,
            "question": best_match["question"],
            "answer": best_match["answer"],
            "specialty": best_match["specialty"],
            "disclaimer": "This is educational information only. For personal medical advice, consult a doctor.",
            "consult_cta": f"Need personalised advice? → {BASE_URL}/consult",
        }

    # No match — redirect to Consult
    return {
        "found": False,
        "question": question,
        "message": "We don't have a pre-built answer for this question yet.",
        "consult_cta_text": "Speak to a Shapeshifters specialist — same-day consultation available",
        "consult_url": f"{BASE_URL}/consult",
        "disclaimer": "Always consult a qualified doctor for personal medical advice.",
    }
