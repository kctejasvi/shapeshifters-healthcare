"""
Shapeshifters Healthcare — Consult Tool
Doctor search, specialty matching, and appointment CTA logic.
"""

import os

BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")

SPECIALTIES = {
    "diabetes": {
        "display": "Diabetes & Endocrinology",
        "common_conditions": ["Type 2 Diabetes", "Type 1 Diabetes", "PCOS", "Thyroid disorders", "Obesity"],
        "consult_url": f"{BASE_URL}/consult/diabetes",
    },
    "oncology": {
        "display": "Oncology (Cancer Care)",
        "common_conditions": ["Breast cancer", "Colorectal cancer", "Cervical cancer", "Oral cancer", "Prostate cancer"],
        "consult_url": f"{BASE_URL}/consult/oncology",
    },
    "surgery": {
        "display": "General Surgery",
        "common_conditions": ["Gallstones", "Hernia", "Appendicitis", "Haemorrhoids", "Thyroid surgery"],
        "consult_url": f"{BASE_URL}/consult/surgery",
    },
    "dermatology": {
        "display": "Dermatology",
        "common_conditions": ["Acne", "Eczema", "Psoriasis", "Hair loss", "Pigmentation"],
        "consult_url": f"{BASE_URL}/consult/dermatology",
    },
    "general_medicine": {
        "display": "General Medicine",
        "common_conditions": ["Hypertension", "Fever", "Infections", "Anaemia", "General checkup"],
        "consult_url": f"{BASE_URL}/consult/general",
    },
}

CITIES = ["Bangalore", "Mumbai", "Hyderabad", "Chennai", "Delhi"]


def find_specialist(specialty: str, city: str | None = None) -> dict:
    """
    Returns CTA and information for finding a specialist.
    Does not store or retrieve actual doctor profiles (future Supabase integration).
    """
    specialty_lower = specialty.lower().replace(" ", "_")
    spec_info = SPECIALTIES.get(specialty_lower)

    if not spec_info:
        # Fuzzy match
        for key, info in SPECIALTIES.items():
            if specialty_lower in key or key in specialty_lower:
                spec_info = info
                break

    if not spec_info:
        return {
            "found": False,
            "message": f"Specialty '{specialty}' not found. Available: {', '.join(SPECIALTIES.keys())}",
        }

    city_str = f" in {city}" if city else " online"
    return {
        "found": True,
        "specialty": spec_info["display"],
        "city": city or "Online (India-wide)",
        "cta_text": f"Consult a {spec_info['display']} specialist{city_str}",
        "cta_url": spec_info["consult_url"],
        "common_conditions": spec_info["common_conditions"],
        "message": (
            f"Connect with a verified {spec_info['display']} specialist{city_str} "
            f"via Shapeshifters Consult. Same-day appointments available."
        ),
    }


def get_second_opinion_cta(condition: str) -> dict:
    """
    Returns a second opinion CTA for a given condition.
    """
    return {
        "condition": condition,
        "cta_text": f"Get a second opinion on {condition} — Shapeshifters Consult",
        "cta_url": f"{BASE_URL}/consult/second-opinion",
        "message": (
            "A second opinion can change your treatment plan. "
            "Connect with a senior specialist on Shapeshifters in 24 hours."
        ),
    }


def list_cities() -> list[str]:
    return CITIES


def list_specialties() -> list[str]:
    return [v["display"] for v in SPECIALTIES.values()]
