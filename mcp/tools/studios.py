"""
Shapeshifters Healthcare — Studios Tool
CME content production, KOL directory, and video module logic.
"""

import os

BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")

STUDIOS_MODULES = [
    {
        "id": "S001",
        "title": "Diabetes Management: 2024 RSSDI Guidelines Explained",
        "specialty": "diabetes",
        "format": "video",
        "duration_minutes": 45,
        "cme_credits": 1,
        "audience": "doctor",
        "url": f"{BASE_URL}/studios/diabetes-rssdi-2024",
    },
    {
        "id": "S002",
        "title": "Laparoscopic Cholecystectomy: Surgical Technique Updates",
        "specialty": "surgery",
        "format": "video",
        "duration_minutes": 60,
        "cme_credits": 1,
        "audience": "doctor",
        "url": f"{BASE_URL}/studios/laparoscopic-cholecystectomy",
    },
    {
        "id": "S003",
        "title": "Melanoma vs Benign Lesions: Dermoscopy for Generalists",
        "specialty": "dermatology",
        "format": "video",
        "duration_minutes": 30,
        "cme_credits": 1,
        "audience": "doctor",
        "url": f"{BASE_URL}/studios/dermoscopy-melanoma",
    },
    {
        "id": "S004",
        "title": "Oncology Emergencies in the ED: What Every Doctor Must Know",
        "specialty": "oncology",
        "format": "video",
        "duration_minutes": 50,
        "cme_credits": 1,
        "audience": "doctor",
        "url": f"{BASE_URL}/studios/oncology-emergencies-ed",
    },
]


def list_cme_modules(specialty: str | None = None) -> list[dict]:
    """List available CME modules, optionally filtered by specialty."""
    modules = STUDIOS_MODULES.copy()
    if specialty:
        modules = [m for m in modules if m["specialty"] == specialty.lower()]
    return modules


def get_module(module_id: str) -> dict | None:
    for m in STUDIOS_MODULES:
        if m["id"] == module_id:
            return m
    return None


def get_studios_cta(specialty: str | None = None) -> dict:
    """Returns a CTA to Shapeshifters Studios."""
    specialty_str = f" — {specialty.capitalize()}" if specialty else ""
    return {
        "cta_text": f"Watch CME Videos{specialty_str} — Shapeshifters Studios",
        "cta_url": f"{BASE_URL}/studios",
        "message": "Earn NMC CME credits with expert-led clinical videos from Shapeshifters Studios.",
    }
