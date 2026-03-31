"""
Shapeshifters Healthcare — Affiliate Tool
Manages affiliate link routing and contextual placement matching.

ETHICAL RULES:
- Never place affiliate links inside clinical advice sections.
- Never recommend a product for commission — only guide where to buy.
- All placement copy must be honest and non-misleading.
- All affiliate HTML must include rel="sponsored" and Sponsored label.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────
# Affiliate Links — read from .env with fallback placeholders
# ──────────────────────────────────────────────────────────────

AFFILIATE_LINKS: dict[str, str] = {
    "health_insurance_niva_bupa": os.getenv("AFFILIATE_NIVA_BUPA", "https://nivabupa.com/?utm_source=shapeshifters"),
    "health_insurance_star_health": os.getenv("AFFILIATE_STAR_HEALTH", "https://starhealth.in/?utm_source=shapeshifters"),
    "lab_tests_thyrocare": os.getenv("AFFILIATE_THYROCARE", "https://thyrocare.com/?ref=shapeshifters"),
    "lab_tests_1mg": os.getenv("AFFILIATE_1MG", "https://1mg.com/lab-tests?utm_source=shapeshifters"),
    "pharmacy_1mg": os.getenv("AFFILIATE_1MG", "https://1mg.com/?utm_source=shapeshifters"),
    "pharmacy_pharmeasy": os.getenv("AFFILIATE_PHARMEASY", "https://pharmeasy.in/?utm_source=shapeshifters"),
    "glucometer": os.getenv("AFFILIATE_MOREPEN", "https://drmorepen.com/?utm_source=shapeshifters"),
    "skincare": os.getenv("AFFILIATE_MINIMALIST", "https://beminimalist.co/?utm_source=shapeshifters"),
    "books_amazon": os.getenv("AFFILIATE_AMAZON", "https://amzn.in/?tag=shapeshifters-21"),
    "marrow_courses": os.getenv("AFFILIATE_MARROW", "https://marrow.com/?ref=shapeshifters"),
    "practo_software": os.getenv("AFFILIATE_PRACTO", "https://practo.com/?ref=shapeshifters"),
    "second_opinion": os.getenv("AFFILIATE_SECOND_OPINION", "https://shapeshifters.health/consult"),
    "shapeshifters_academy": os.getenv("AFFILIATE_ACADEMY", "https://shapeshifters.health/academy"),
}

# ──────────────────────────────────────────────────────────────
# Contextual matching rules
# keyword → list of (product_type, placement_copy, placement_position)
# ──────────────────────────────────────────────────────────────

CONTEXTUAL_RULES: dict[str, list[dict]] = {
    # Diabetes / Endocrinology
    "metformin": [
        {"product": "pharmacy_1mg", "copy": "Order Metformin online — verified pharmacy, home delivery", "position": "after_dosage_section"},
        {"product": "lab_tests_thyrocare", "copy": "HbA1c test at home — ₹249, results in 24 hours", "position": "after_monitoring_section"},
    ],
    "diabetes": [
        {"product": "lab_tests_thyrocare", "copy": "Full Diabetes Panel at home — HbA1c + fasting glucose + kidney function ₹499", "position": "after_intro"},
        {"product": "glucometer", "copy": "Dr. Morepen Glucometer — accurate blood sugar monitoring at home", "position": "after_monitoring_section"},
    ],
    "hba1c": [
        {"product": "lab_tests_thyrocare", "copy": "Book HbA1c test at home — Thyrocare ₹249, pan-India collection", "position": "after_intro"},
        {"product": "lab_tests_1mg", "copy": "HbA1c test on 1mg — certified lab, home collection", "position": "after_results_section"},
    ],
    "insulin": [
        {"product": "pharmacy_1mg", "copy": "Order insulin and diabetes supplies — 1mg verified pharmacy", "position": "after_dosage_section"},
        {"product": "glucometer", "copy": "Monitor your glucose with Dr. Morepen Glucometer", "position": "after_monitoring_section"},
    ],
    "semaglutide": [
        {"product": "pharmacy_1mg", "copy": "Check semaglutide (Ozempic / Rybelsus) availability — 1mg", "position": "after_availability_section"},
        {"product": "lab_tests_thyrocare", "copy": "Diabetes monitoring panel while on GLP-1 therapy — Thyrocare", "position": "after_monitoring_section"},
    ],
    # Cancer / Oncology
    "cancer": [
        {"product": "second_opinion", "copy": "Get a senior oncologist's second opinion — Shapeshifters Consult", "position": "after_intro"},
        {"product": "health_insurance_niva_bupa", "copy": "Cancer treatment cover — Niva Bupa Critical Illness Plan", "position": "after_cost_section"},
    ],
    "cancer screening": [
        {"product": "lab_tests_thyrocare", "copy": "Cancer Screening Panel at home — Thyrocare, pan-India ₹1499", "position": "after_screening_types"},
        {"product": "health_insurance_niva_bupa", "copy": "Cover cancer treatment costs — Niva Bupa Critical Illness", "position": "after_cost_section"},
    ],
    "chemotherapy": [
        {"product": "health_insurance_niva_bupa", "copy": "Cashless chemotherapy at 10,000+ hospitals — Niva Bupa", "position": "after_intro"},
        {"product": "second_opinion", "copy": "Second opinion before starting chemo — Shapeshifters Consult", "position": "after_treatment_options"},
    ],
    # Surgery
    "surgery": [
        {"product": "health_insurance_niva_bupa", "copy": "Cashless surgery at 10,000+ hospitals — Niva Bupa", "position": "after_intro"},
        {"product": "pharmacy_1mg", "copy": "Post-surgery medications delivered home — 1mg", "position": "after_medication_section"},
    ],
    "laparoscopic": [
        {"product": "health_insurance_niva_bupa", "copy": "Laparoscopic surgery fully covered — Niva Bupa health insurance", "position": "after_intro"},
        {"product": "second_opinion", "copy": "Unsure if you need surgery? Get a second opinion online", "position": "after_procedure_section"},
    ],
    # Dermatology
    "acne": [
        {"product": "skincare", "copy": "Minimalist Niacinamide 10% — dermatologist-recommended for acne ₹599", "position": "after_otc_section"},
        {"product": "pharmacy_1mg", "copy": "Prescription acne creams delivered — 1mg verified pharmacy", "position": "after_prescription_section"},
    ],
    "tretinoin": [
        {"product": "pharmacy_1mg", "copy": "Buy Retino-A (tretinoin) — 1mg, prescription required", "position": "after_where_to_buy"},
        {"product": "skincare", "copy": "Granactive Retinoid 2% (OTC starter) — Minimalist ₹599", "position": "after_alternatives_section"},
    ],
    "skincare": [
        {"product": "skincare", "copy": "Minimalist Skincare — science-backed, dermatologist-formulated, from ₹299", "position": "after_routine_section"},
    ],
    "hair loss": [
        {"product": "pharmacy_1mg", "copy": "Hair loss treatments and supplements — 1mg verified pharmacy", "position": "after_treatment_section"},
        {"product": "lab_tests_1mg", "copy": "Hair loss blood panel (thyroid, iron, vitamins) — 1mg lab tests", "position": "after_causes_section"},
    ],
    # General medicine
    "thyroid": [
        {"product": "lab_tests_thyrocare", "copy": "Thyroid Function Test (TSH + T3 + T4) at home — Thyrocare ₹299", "position": "after_intro"},
        {"product": "pharmacy_1mg", "copy": "Thyroid medications (Thyronorm, Eltroxin) — 1mg verified pharmacy", "position": "after_medication_section"},
    ],
    "blood pressure": [
        {"product": "glucometer", "copy": "Dr. Morepen BP Monitor — clinically validated, ₹899", "position": "after_monitoring_section"},
        {"product": "pharmacy_1mg", "copy": "Blood pressure medications delivered home — 1mg", "position": "after_medication_section"},
    ],
    "health insurance": [
        {"product": "health_insurance_niva_bupa", "copy": "Niva Bupa — ₹5L cover from ₹318/month, instant policy", "position": "after_intro"},
        {"product": "health_insurance_star_health", "copy": "Star Health — best for senior citizens, no sub-limits", "position": "after_comparison_table"},
    ],
    # Doctor-facing
    "cme": [
        {"product": "shapeshifters_academy", "copy": "Shapeshifters Academy — NMC-recognised CME, earn credits online", "position": "after_intro"},
        {"product": "marrow_courses", "copy": "Marrow Clinical — subspecialty CME for working doctors", "position": "after_comparison_table"},
    ],
    "neet pg": [
        {"product": "marrow_courses", "copy": "Marrow for NEET PG — 3-day free trial, 10,000+ questions", "position": "after_intro"},
        {"product": "books_amazon", "copy": "NEET PG books on Amazon India — Harrison's, Robbins and more", "position": "after_books_section"},
    ],
    "clinical guidelines": [
        {"product": "shapeshifters_academy", "copy": "Shapeshifters Academy — structured CME on latest clinical guidelines", "position": "after_guidelines_section"},
    ],
}


def get_affiliate_link(product_type: str, city: str | None = None) -> str:
    """
    Returns the affiliate URL for a given product type.

    Args:
        product_type: Key from AFFILIATE_LINKS dict
        city: Optional city (reserved for city-specific UTM tracking in future)

    Returns:
        Affiliate URL string
    """
    url = AFFILIATE_LINKS.get(product_type.lower().replace(" ", "_"))
    if not url:
        # Try partial match
        for key, val in AFFILIATE_LINKS.items():
            if product_type.lower() in key:
                url = val
                break

    if not url:
        return f"https://shapeshifters.health/consult"

    # Future: add city UTM parameter
    # if city:
    #     url += f"&utm_content={city.lower()}"

    return url


def get_contextual_affiliates(topic: str, audience: str = "patient") -> dict:
    """
    Given a topic and audience, returns 2–3 contextually relevant affiliate
    suggestions with links and placement copy.

    Args:
        topic: Medical topic string (e.g. "metformin", "cancer screening")
        audience: "patient" or "doctor"

    Returns:
        Dict with topic, audience, and list of suggestions
    """
    topic_lower = topic.lower().strip()

    # Find best matching rule
    matched_rules: list[dict] = []

    # Exact match
    if topic_lower in CONTEXTUAL_RULES:
        matched_rules = CONTEXTUAL_RULES[topic_lower]
    else:
        # Partial / keyword match — longest overlap wins
        best_key = ""
        for key in CONTEXTUAL_RULES:
            if key in topic_lower or topic_lower in key:
                if len(key) > len(best_key):
                    best_key = key
        if best_key:
            matched_rules = CONTEXTUAL_RULES[best_key]

    # Filter by audience where relevant
    doctor_products = {"marrow_courses", "practo_software", "shapeshifters_academy"}
    patient_products = {"health_insurance_niva_bupa", "health_insurance_star_health",
                        "lab_tests_thyrocare", "lab_tests_1mg", "pharmacy_1mg",
                        "pharmacy_pharmeasy", "glucometer", "skincare", "books_amazon",
                        "second_opinion"}

    filtered: list[dict] = []
    for rule in matched_rules:
        product = rule["product"]
        if audience == "doctor" and product in patient_products and product not in {"second_opinion", "lab_tests_thyrocare"}:
            continue  # skip patient-only for doctors (with exceptions)
        if audience == "patient" and product in doctor_products:
            continue  # skip doctor tools for patients
        filtered.append(rule)

    if not filtered:
        filtered = matched_rules  # fall back to all if over-filtered

    suggestions = []
    for rule in filtered[:3]:  # max 3
        link = get_affiliate_link(rule["product"])
        partner_display = _product_to_display_name(rule["product"])
        suggestions.append({
            "partner": partner_display,
            "placement_copy": rule["copy"],
            "link": link,
            "placement_position": rule["position"],
        })

    return {
        "topic": topic,
        "audience": audience,
        "suggestions": suggestions,
    }


def render_affiliate_html(suggestion: dict) -> str:
    """
    Renders a single affiliate suggestion as HTML.
    Follows Shapeshifters sponsored box format.
    """
    return (
        f'<div class="affiliate-box">\n'
        f'  <p class="affiliate-label">📋 Sponsored</p>\n'
        f'  <a href="{suggestion["link"]}" class="affiliate-cta" '
        f'target="_blank" rel="sponsored noopener">\n'
        f'    {suggestion["placement_copy"]}\n'
        f'  </a>\n'
        f'</div>'
    )


def _product_to_display_name(product_key: str) -> str:
    """Convert product key to human-readable partner name."""
    MAP = {
        "health_insurance_niva_bupa": "Niva Bupa",
        "health_insurance_star_health": "Star Health",
        "lab_tests_thyrocare": "Thyrocare",
        "lab_tests_1mg": "1mg Labs",
        "pharmacy_1mg": "1mg Pharmacy",
        "pharmacy_pharmeasy": "PharmEasy",
        "glucometer": "Dr. Morepen",
        "skincare": "Minimalist",
        "books_amazon": "Amazon India",
        "marrow_courses": "Marrow",
        "practo_software": "Practo",
        "second_opinion": "Shapeshifters Consult",
        "shapeshifters_academy": "Shapeshifters Academy",
    }
    return MAP.get(product_key, product_key.replace("_", " ").title())
