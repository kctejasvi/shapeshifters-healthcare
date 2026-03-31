"""
Shapeshifters Healthcare — Academy Tool
Clinical courses, NEET PG resources, and case-based learning.
"""

import os

BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")

COURSES = [
    {
        "id": "A001",
        "title": "Master Diabetes Management",
        "specialty": "diabetes",
        "audience": "doctor",
        "level": "intermediate",
        "modules": 12,
        "cme_credits": 5,
        "price_inr": 1499,
        "url": f"{BASE_URL}/academy/diabetes-management",
        "highlights": [
            "RSSDI 2024 guidelines deep-dive",
            "Insulin initiation protocols",
            "CGM interpretation",
            "20 clinical case studies",
        ],
    },
    {
        "id": "A002",
        "title": "Oncology Fundamentals for Generalists",
        "specialty": "oncology",
        "audience": "doctor",
        "level": "beginner",
        "modules": 8,
        "cme_credits": 3,
        "price_inr": 999,
        "url": f"{BASE_URL}/academy/oncology-fundamentals",
        "highlights": [
            "Cancer screening protocols",
            "Chemotherapy side-effect management",
            "Palliative care essentials",
            "Referral decision frameworks",
        ],
    },
    {
        "id": "A003",
        "title": "NEET PG Surgery — High-Yield Module",
        "specialty": "surgery",
        "audience": "student",
        "level": "exam-prep",
        "modules": 15,
        "cme_credits": 0,
        "price_inr": 2499,
        "url": f"{BASE_URL}/academy/neet-pg-surgery",
        "highlights": [
            "Previous year questions analysis",
            "Surgical anatomy MCQs",
            "Rapid revision notes",
            "5 mock tests",
        ],
    },
    {
        "id": "A004",
        "title": "Dermatology for Primary Care",
        "specialty": "dermatology",
        "audience": "doctor",
        "level": "beginner",
        "modules": 6,
        "cme_credits": 2,
        "price_inr": 799,
        "url": f"{BASE_URL}/academy/dermatology-primary-care",
        "highlights": [
            "Common skin conditions recognition",
            "Topical steroid ladder",
            "Acne treatment protocols",
            "When to refer to a dermatologist",
        ],
    },
]


def list_courses(specialty: str | None = None, audience: str | None = None) -> list[dict]:
    """List Academy courses, optionally filtered."""
    courses = COURSES.copy()
    if specialty:
        courses = [c for c in courses if c["specialty"] == specialty.lower()]
    if audience:
        courses = [c for c in courses if c["audience"] == audience.lower()]
    return courses


def get_course(course_id: str) -> dict | None:
    for c in COURSES:
        if c["id"] == course_id:
            return c
    return None


def get_academy_cta(specialty: str | None = None, audience: str = "doctor") -> dict:
    """Returns a CTA to Shapeshifters Academy."""
    if audience == "student":
        return {
            "cta_text": "Shapeshifters Academy — NEET PG Prep Courses",
            "cta_url": f"{BASE_URL}/academy/neet-pg",
            "message": "Prepare for NEET PG with high-yield modules and mock tests.",
        }
    specialty_str = f" — {specialty.capitalize()}" if specialty else ""
    return {
        "cta_text": f"Shapeshifters Academy{specialty_str} — CME Courses for Doctors",
        "cta_url": f"{BASE_URL}/academy",
        "message": "Earn NMC CME credits with structured clinical courses from Shapeshifters Academy.",
    }
