"""
Shapeshifters Healthcare — Drug Reference Tool
Provides drug information for educational purposes only.
NEVER used to recommend treatment — purely informational.
"""

import os

DRUG_DATABASE = {
    "metformin": {
        "generic_name": "Metformin Hydrochloride",
        "brand_names_india": ["Glycomet", "Glucophage", "Obimet", "Bigomet"],
        "class": "Biguanide (antidiabetic)",
        "indications": ["Type 2 Diabetes Mellitus", "PCOS (off-label)", "Pre-diabetes prevention"],
        "usual_dose": "500–2000 mg/day in divided doses with meals",
        "max_dose": "2550 mg/day",
        "route": "Oral",
        "common_side_effects": [
            "Nausea and vomiting (especially on initiation)",
            "Diarrhoea",
            "Abdominal discomfort",
            "Metallic taste",
            "Vitamin B12 deficiency (long-term use)",
        ],
        "serious_side_effects": ["Lactic acidosis (rare, <0.01%)"],
        "contraindications": [
            "eGFR < 30 mL/min (absolute contraindication)",
            "Severe hepatic impairment",
            "Acute heart failure",
            "Contrast dye procedures (hold 48 hours before/after)",
        ],
        "monitoring": ["HbA1c every 3 months initially, then 6-monthly", "Renal function (eGFR) annually", "Vitamin B12 every 1–2 years"],
        "pregnancy_category": "Category B",
        "availability_india": "Schedule H — prescription required",
        "approx_cost_india": "₹5–15 per tablet (500 mg)",
        "patient_counselling": [
            "Take with food to reduce GI side effects",
            "Do not skip doses",
            "Stay well hydrated",
            "Inform doctor before any surgery or contrast scan",
        ],
        "article_link": "/metformin-side-effects-india",
    },
    "semaglutide": {
        "generic_name": "Semaglutide",
        "brand_names_india": ["Ozempic (SC injection)", "Rybelsus (oral)"],
        "class": "GLP-1 Receptor Agonist",
        "indications": ["Type 2 Diabetes Mellitus", "Cardiovascular risk reduction in T2DM", "Obesity (Wegovy — not yet in India)"],
        "usual_dose": "0.25 mg SC weekly (starting), titrate to 0.5–1 mg weekly",
        "route": "Subcutaneous injection (weekly) / Oral tablet",
        "common_side_effects": ["Nausea", "Vomiting", "Diarrhoea", "Constipation", "Decreased appetite"],
        "serious_side_effects": ["Pancreatitis", "Thyroid C-cell tumours (animal data)", "Diabetic retinopathy worsening"],
        "contraindications": [
            "Personal/family history of medullary thyroid carcinoma",
            "MEN2 syndrome",
            "Pregnancy",
        ],
        "monitoring": ["HbA1c", "Renal function", "Amylase/lipase if abdominal pain"],
        "pregnancy_category": "Category C — discontinue 2 months before planned pregnancy",
        "availability_india": "Available (Ozempic injection); Rybelsus limited availability",
        "approx_cost_india": "₹3,500–6,000 per pen (4 doses)",
        "article_link": "/ozempic-india-semaglutide-guide",
    },
    "tretinoin": {
        "generic_name": "Tretinoin (all-trans retinoic acid)",
        "brand_names_india": ["Retino-A", "A-Ret", "Tretin"],
        "class": "Retinoid (topical)",
        "indications": ["Acne vulgaris", "Photoageing", "Hyperpigmentation"],
        "usual_dose": "0.025%–0.05% cream, applied nightly (pea-sized amount)",
        "route": "Topical",
        "common_side_effects": ["Skin dryness", "Peeling", "Redness", "Initial acne purge (weeks 2–6)"],
        "serious_side_effects": ["Severe skin irritation if overused", "Sun sensitivity"],
        "contraindications": ["Pregnancy (Category X — teratogenic)", "Eczema / rosacea (use with caution)"],
        "monitoring": ["Sun protection mandatory", "Skin tolerance"],
        "availability_india": "Schedule H — prescription required (Retino-A 0.025% / 0.05%)",
        "approx_cost_india": "₹80–200 per tube (20g)",
        "article_link": "/tretinoin-india-guide",
    },
    "levothyroxine": {
        "generic_name": "Levothyroxine Sodium (L-thyroxine)",
        "brand_names_india": ["Thyronorm", "Eltroxin", "Thyrox"],
        "class": "Thyroid hormone replacement",
        "indications": ["Hypothyroidism", "Goitre", "TSH suppression in thyroid cancer"],
        "usual_dose": "25–200 mcg daily (individualised based on TSH)",
        "route": "Oral (take on empty stomach, 30 min before breakfast)",
        "common_side_effects": ["Symptoms of hyperthyroidism if over-dosed: palpitations, tremor, insomnia, weight loss"],
        "contraindications": ["Untreated adrenal insufficiency", "Acute MI (use caution)"],
        "monitoring": ["TSH every 6–8 weeks after dose change, then annually when stable"],
        "availability_india": "Schedule H",
        "approx_cost_india": "₹1–3 per tablet",
        "article_link": "/thyroid-test-india",
    },
    "amlodipine": {
        "generic_name": "Amlodipine Besylate",
        "brand_names_india": ["Amlopin", "Amlokind", "Amloz", "Stamlo"],
        "class": "Calcium channel blocker (antihypertensive)",
        "indications": ["Hypertension", "Stable angina", "Vasospastic angina"],
        "usual_dose": "5–10 mg once daily",
        "route": "Oral",
        "common_side_effects": ["Peripheral oedema (ankle swelling)", "Flushing", "Headache", "Palpitations"],
        "contraindications": ["Severe aortic stenosis", "Cardiogenic shock"],
        "monitoring": ["Blood pressure", "Heart rate"],
        "availability_india": "Schedule H",
        "approx_cost_india": "₹2–5 per tablet",
        "article_link": "/blood-pressure-management-india",
    },
}


def search_drug(name: str) -> dict:
    """
    Look up a drug by generic or brand name.
    Returns drug info dict or error message.
    """
    name_lower = name.lower().strip()

    # Direct key match
    if name_lower in DRUG_DATABASE:
        drug = DRUG_DATABASE[name_lower]
        return {"found": True, "drug": drug, "disclaimer": _disclaimer()}

    # Search by brand name
    for key, drug in DRUG_DATABASE.items():
        brands = [b.lower() for b in drug.get("brand_names_india", [])]
        if any(name_lower in b for b in brands):
            return {"found": True, "drug": drug, "disclaimer": _disclaimer()}

    # Partial match on key
    matches = [k for k in DRUG_DATABASE if name_lower in k]
    if matches:
        drug = DRUG_DATABASE[matches[0]]
        return {"found": True, "drug": drug, "disclaimer": _disclaimer()}

    return {
        "found": False,
        "message": f"Drug '{name}' not found in our reference database.",
        "suggestion": "Ask your pharmacist or consult a doctor for accurate drug information.",
        "consult_cta": "https://shapeshifters.health/consult",
    }


def get_drug_interactions(drug1: str, drug2: str) -> dict:
    """
    Basic interaction checker — educational only.
    Returns known interaction data or advisory to check with pharmacist.
    """
    KNOWN_INTERACTIONS = {
        ("metformin", "contrast_dye"): {
            "severity": "Major",
            "description": "Risk of lactic acidosis. Metformin must be held 48 hours before and after iodinated contrast procedures.",
            "action": "Hold metformin 48h before procedure; restart only after renal function confirmed normal.",
        },
        ("levothyroxine", "calcium"): {
            "severity": "Moderate",
            "description": "Calcium supplements reduce levothyroxine absorption.",
            "action": "Take levothyroxine 4 hours apart from calcium supplements.",
        },
        ("metformin", "alcohol"): {
            "severity": "Moderate",
            "description": "Alcohol increases risk of lactic acidosis with metformin.",
            "action": "Limit alcohol consumption. Avoid binge drinking.",
        },
    }

    d1, d2 = drug1.lower().strip(), drug2.lower().strip()
    interaction = (
        KNOWN_INTERACTIONS.get((d1, d2))
        or KNOWN_INTERACTIONS.get((d2, d1))
    )

    if interaction:
        return {"found": True, "interaction": interaction, "disclaimer": _disclaimer()}

    return {
        "found": False,
        "message": f"No known major interaction between {drug1} and {drug2} in our database.",
        "advisory": "This database is not exhaustive. Always verify drug interactions with a pharmacist or prescribing doctor.",
        "disclaimer": _disclaimer(),
    }


def _disclaimer() -> str:
    return (
        "⚠️ This information is for educational purposes only. "
        "It does not constitute medical advice. Always consult a qualified doctor "
        "or pharmacist before starting, stopping, or changing any medication."
    )
