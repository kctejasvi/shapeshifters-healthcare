"""
Shapeshifters Healthcare — Medical News Tool
Aggregates and formats medical news for India.
"""

import os
from datetime import datetime, timezone


# Static curated headlines used as fallback when no live API is configured.
# Replace with NewsAPI / PubMed / RSS fetch when API key is available.
CURATED_HEADLINES = [
    {
        "title": "ICMR Updates Diabetes Management Guidelines for 2024",
        "summary": "The Indian Council of Medical Research has revised HbA1c targets and updated first-line treatment algorithms for Type 2 Diabetes in India.",
        "specialty": "diabetes",
        "source": "ICMR",
        "date": "2024-11-15",
        "url": "https://icmr.gov.in",
        "audience": ["doctor", "patient"],
    },
    {
        "title": "Cervical Cancer Vaccination Programme Expanded to 9–14 Year Olds Nationally",
        "summary": "India's national immunisation programme now includes HPV vaccination for adolescent girls, covering 5 crore children in phase one.",
        "specialty": "oncology",
        "source": "Ministry of Health",
        "date": "2024-10-20",
        "url": "https://mohfw.gov.in",
        "audience": ["doctor", "patient"],
    },
    {
        "title": "AIIMS Delhi Performs First Robotic Liver Resection for Cancer",
        "summary": "AIIMS New Delhi announced the first successful robotic-assisted liver resection for hepatocellular carcinoma, reducing recovery time by 40%.",
        "specialty": "surgery",
        "source": "AIIMS Delhi",
        "date": "2024-12-01",
        "url": "https://aiims.edu",
        "audience": ["doctor"],
    },
    {
        "title": "Tretinoin Now Requires Prescription Across All Indian States",
        "summary": "The Central Drugs Standard Control Organisation (CDSCO) has reinforced Schedule H status for tretinoin following misuse concerns.",
        "specialty": "dermatology",
        "source": "CDSCO",
        "date": "2024-09-10",
        "url": "https://cdsco.gov.in",
        "audience": ["doctor", "patient"],
    },
    {
        "title": "Ozempic (Semaglutide) Demand Surges in India Amid Obesity Crisis",
        "summary": "A 300% increase in semaglutide prescriptions was recorded in 2024 as Indian cardiologists and endocrinologists adopt GLP-1 therapy more widely.",
        "specialty": "diabetes",
        "source": "Economic Times Health",
        "date": "2024-11-28",
        "url": "https://health.economictimes.indiatimes.com",
        "audience": ["doctor", "patient"],
    },
    {
        "title": "New NMC CME Rules: All Doctors Need 30 Credits Every 5 Years",
        "summary": "The National Medical Commission has clarified that all registered medical practitioners must complete 30 CME credits per 5-year period for licence renewal.",
        "specialty": "general",
        "source": "NMC India",
        "date": "2024-08-05",
        "url": "https://nmc.org.in",
        "audience": ["doctor"],
    },
    {
        "title": "India's Cancer Incidence to Rise 12% by 2030 — ICMR Report",
        "summary": "A new ICMR report projects 15.7 lakh new cancer cases annually by 2030, with breast, cervical, and oral cancers leading in incidence.",
        "specialty": "oncology",
        "source": "ICMR",
        "date": "2024-10-08",
        "url": "https://icmr.gov.in",
        "audience": ["doctor", "patient"],
    },
    {
        "title": "Hypertension Awareness Campaign Targets 2 Crore Indians",
        "summary": "The government's HEARTS programme aims to treat 2 crore hypertensive patients at primary health centres using a standardised protocol.",
        "specialty": "general",
        "source": "Ministry of Health",
        "date": "2024-11-01",
        "url": "https://mohfw.gov.in",
        "audience": ["doctor", "patient"],
    },
]


def get_medical_news(
    specialty: str | None = None,
    audience: str | None = None,
    limit: int = 5
) -> list[dict]:
    """
    Returns recent medical news, optionally filtered by specialty or audience.

    Args:
        specialty: 'diabetes', 'oncology', 'surgery', 'dermatology', 'general'
        audience: 'doctor' or 'patient'
        limit: number of articles to return (default 5)

    Returns:
        List of news dicts with title, summary, source, date, url
    """
    news = CURATED_HEADLINES.copy()

    if specialty:
        news = [n for n in news if n.get("specialty") == specialty.lower()]

    if audience:
        news = [n for n in news if audience.lower() in n.get("audience", [])]

    news.sort(key=lambda n: n["date"], reverse=True)
    return news[:limit]


def format_news_for_telegram(news_items: list[dict]) -> str:
    """Format news list as Telegram-ready Markdown."""
    if not news_items:
        return "No recent news found for this category."

    lines = ["📰 *Latest Medical News*\n"]
    for i, item in enumerate(news_items, 1):
        lines.append(f"*{i}\\. {item['title']}*")
        lines.append(f"_{item['summary'][:120]}\\.\\.\\._")
        lines.append(f"🗓 {item['date']} · {item['source']}")
        lines.append("")

    return "\n".join(lines)
