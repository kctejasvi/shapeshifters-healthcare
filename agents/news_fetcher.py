"""
Shapeshifters Healthcare — Live RSS News Fetcher
Fetches from 4 feeds:
  Indian:        Times of India Health, NDTV Health
  International: WHO News, MedicalXpress
Runs every 6 hours via cron.
Updates mcp/tools/medical_news_live.py automatically.
"""

import feedparser
import json
import os
import sys
import logging
from datetime import datetime, timezone
from dateutil import parser as dateparser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# THE 4 RSS FEEDS
# ─────────────────────────────────────────────

RSS_FEEDS = [
    # ── INDIAN FEEDS ──────────────────────────
    {
        "name": "The Hindu Health",
        "url": "https://www.thehindu.com/sci-tech/health/feeder/default.rss",
        "country": "India",
        "language": "EN",
        "audience": ["patients", "general"],
        "specialty_hint": "General Medicine",
    },
    {
        "name": "Hindustan Times Health",
        "url": "https://www.hindustantimes.com/feeds/rss/health/rssfeed.xml",
        "country": "India",
        "language": "EN",
        "audience": ["patients", "general"],
        "specialty_hint": "General Medicine",
    },

    # ── INTERNATIONAL FEEDS ───────────────────
    {
        "name": "WHO News",
        "url": "https://www.who.int/rss-feeds/news-english.xml",
        "country": "International",
        "language": "EN",
        "audience": ["clinicians", "institutions"],
        "specialty_hint": "General Medicine",
    },
    {
        "name": "MedicalXpress",
        "url": "https://medicalxpress.com/rss-feed/",
        "country": "International",
        "language": "EN",
        "audience": ["clinicians", "researchers"],
        "specialty_hint": "Research",
    },
]

# ─────────────────────────────────────────────
# KEYWORD FILTERS
# ─────────────────────────────────────────────

SPECIALTY_KEYWORDS = {
    "Surgery": [
        "surgery", "surgical", "operation", "laparoscopic",
        "robotic surgery", "transplant", "orthopaedic", "orthopedic"
    ],
    "Diabetes & Endocrinology": [
        "diabetes", "insulin", "metformin", "blood sugar",
        "HbA1c", "endocrine", "thyroid", "obesity", "GLP-1"
    ],
    "Oncology": [
        "cancer", "tumour", "tumor", "chemotherapy", "oncology",
        "radiation", "immunotherapy", "carcinoma", "malignant"
    ],
    "Dermatology": [
        "skin", "dermatology", "acne", "psoriasis", "eczema",
        "hair loss", "melanoma", "rash", "dermatitis"
    ],
    "Cardiology": [
        "heart", "cardiac", "cardiology", "blood pressure",
        "hypertension", "coronary", "stroke", "ECG", "arrhythmia"
    ],
    "Neurology": [
        "brain", "neuro", "alzheimer", "parkinson", "epilepsy",
        "migraine", "dementia", "stroke", "neurological"
    ],
    "General Medicine": [
        "health", "medicine", "hospital", "doctor", "treatment",
        "patient", "drug", "vaccine", "infection", "virus",
        "india", "WHO", "ICMR", "AIIMS", "medical"
    ],
}

EXCLUDE_KEYWORDS = [
    "advertisement", "sponsored", "buy now", "sale",
    "discount", "offer", "beauty tips", "fashion",
    "celebrity", "bollywood", "cricket", "sports",
]

# ─────────────────────────────────────────────
# FETCH FUNCTIONS
# ─────────────────────────────────────────────

def detect_specialty(text: str) -> str:
    text_lower = text.lower()
    for specialty, keywords in SPECIALTY_KEYWORDS.items():
        if specialty == "General Medicine":
            continue
        if any(kw in text_lower for kw in keywords):
            return specialty
    return "General Medicine"


def detect_impact(text: str, source: str) -> str:
    text_lower = text.lower()
    high_impact = [
        "breakthrough", "trial", "study", "research", "new treatment",
        "approved", "guideline", "warning", "alert", "outbreak",
        "WHO", "ICMR", "AIIMS", "lancet", "nejm"
    ]
    if any(kw in text_lower for kw in high_impact) or source in ["WHO News", "MedicalXpress"]:
        return "High"
    return "Medium"


def is_relevant(title: str, summary: str) -> bool:
    combined = (title + " " + summary).lower()
    if any(kw in combined for kw in EXCLUDE_KEYWORDS):
        return False
    all_keywords = [kw for kws in SPECIALTY_KEYWORDS.values() for kw in kws]
    return any(kw in combined for kw in all_keywords)


def parse_date(entry) -> str:
    try:
        if hasattr(entry, "published"):
            return dateparser.parse(entry.published).strftime("%Y-%m-%d")
        if hasattr(entry, "updated"):
            return dateparser.parse(entry.updated).strftime("%Y-%m-%d")
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def fetch_feed(feed_config: dict) -> list:
    logger.info(f"Fetching: {feed_config['name']}")
    articles = []
    try:
        feed = feedparser.parse(feed_config["url"])
        if feed.bozo and not feed.entries:
            logger.warning(f"Feed error for {feed_config['name']}: {feed.bozo_exception}")
            return []

        for entry in feed.entries[:15]:
            title   = getattr(entry, "title",   "").strip()
            summary = getattr(entry, "summary", "").strip()
            link    = getattr(entry, "link",    "").strip()

            if not title or not is_relevant(title, summary):
                continue

            summary_clean = summary[:300].replace("<p>", "").replace("</p>", "").replace("<b>", "").replace("</b>", "").strip()
            if not summary_clean:
                summary_clean = title

            specialty = detect_specialty(title + " " + summary_clean)
            impact    = detect_impact(title + " " + summary_clean, feed_config["name"])
            date      = parse_date(entry)

            articles.append({
                "headline":           title,
                "summary":            summary_clean,
                "source":             feed_config["name"],
                "country":            feed_config["country"],
                "specialty":          [specialty],
                "audience":           feed_config["audience"],
                "impact":             impact,
                "date":               date,
                "url":                link,
                "type":               "news",
                "clinical_relevance": f"Latest update from {feed_config['name']} — {specialty}",
                "read_more":          link,
            })

        logger.info(f"Fetched {len(articles)} relevant articles from {feed_config['name']}")

    except Exception as e:
        logger.error(f"Failed to fetch {feed_config['name']}: {e}")

    return articles


def fetch_all_feeds() -> list:
    all_articles = []
    for feed in RSS_FEEDS:
        articles = fetch_feed(feed)
        all_articles.extend(articles)

    # Sort by date (newest first) and deduplicate by headline
    seen_headlines = set()
    unique_articles = []
    for article in sorted(all_articles, key=lambda x: x["date"], reverse=True):
        if article["headline"] not in seen_headlines:
            seen_headlines.add(article["headline"])
            unique_articles.append(article)

    logger.info(f"Total unique articles: {len(unique_articles)}")
    return unique_articles[:20]


# ─────────────────────────────────────────────
# SAVE TO DATABASE
# ─────────────────────────────────────────────

def save_to_database(articles: list):
    output_path = "mcp/tools/medical_news_live.py"

    # Add news_id to each article
    for i, article in enumerate(articles):
        article["news_id"] = f"LIVE{str(i+1).zfill(3)}"

    content = f'''"""
Shapeshifters Healthcare — Live Medical News Database
Auto-generated by RSS fetcher on {datetime.now().strftime("%Y-%m-%d %H:%M")}
Sources: Times of India Health, NDTV Health, WHO News, MedicalXpress
DO NOT edit manually — this file is overwritten every 6 hours
"""

from datetime import datetime

LIVE_NEWS_DATABASE = {json.dumps(articles, indent=4, ensure_ascii=False)}

LAST_UPDATED = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
TOTAL_ARTICLES = {len(articles)}
SOURCES = ["Times of India Health", "NDTV Health", "WHO News", "MedicalXpress"]


async def get_live_news(args: dict) -> dict:
    specialty = args.get("specialty", "").lower()
    impact    = args.get("impact", "").lower()
    limit     = int(args.get("limit", 5))
    country   = args.get("country", "").lower()

    results = LIVE_NEWS_DATABASE

    if specialty:
        results = [n for n in results if any(specialty in s.lower() for s in n.get("specialty", []))]
    if impact:
        results = [n for n in results if n.get("impact", "").lower() == impact]
    if country:
        results = [n for n in results if country in n.get("country", "").lower()]

    results = results[:limit]

    if not results:
        return {{
            "status": "no_results",
            "message": "No live news matched your filters.",
            "last_updated": LAST_UPDATED,
        }}

    return {{
        "status": "success",
        "count": len(results),
        "last_updated": LAST_UPDATED,
        "sources": SOURCES,
        "news": results,
    }}


async def get_news_by_country(args: dict) -> dict:
    country = args.get("country", "india").lower()
    results = [n for n in LIVE_NEWS_DATABASE if country in n.get("country", "").lower()]
    return {{
        "status": "success",
        "country": country,
        "count": len(results),
        "news": results[:5],
        "last_updated": LAST_UPDATED,
    }}


async def get_news_summary_live(args: dict) -> dict:
    indian_news = [n for n in LIVE_NEWS_DATABASE if n.get("country") == "India"]
    intl_news   = [n for n in LIVE_NEWS_DATABASE if n.get("country") == "International"]
    high_impact = [n for n in LIVE_NEWS_DATABASE if n.get("impact") == "High"]

    return {{
        "status": "success",
        "summary": {{
            "total_articles":    len(LIVE_NEWS_DATABASE),
            "indian_news":       len(indian_news),
            "international":     len(intl_news),
            "high_impact":       len(high_impact),
            "last_updated":      LAST_UPDATED,
            "sources":           SOURCES,
        }},
        "top_headlines": [
            {{
                "headline": n["headline"],
                "source":   n["source"],
                "impact":   n["impact"],
                "url":      n["url"],
            }}
            for n in LIVE_NEWS_DATABASE[:3]
        ],
    }}
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Saved {len(articles)} articles to {output_path}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    logger.info("Starting RSS news fetcher...")
    logger.info(f"Feeds: {[f['name'] for f in RSS_FEEDS]}")

    articles = fetch_all_feeds()

    if not articles:
        logger.warning("No articles fetched. Check feed URLs.")
        sys.exit(1)

    save_to_database(articles)

    logger.info("RSS fetch complete!")
    logger.info(f"Articles saved: {len(articles)}")
    logger.info("Preview:")
    for a in articles[:3]:
        logger.info(f"  [{a['source']}] {a['headline'][:60]}...")

def restart_bot():
    import subprocess
    try:
        result = subprocess.run(
            ["systemctl", "restart", "shapeshifters-bot"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info("Bot restarted successfully.")
        else:
            logger.error(f"Bot restart failed: {result.stderr.strip()}")
    except Exception as e:
        logger.error(f"Bot restart failed: {e}")


def main():
    logger.info("Starting RSS news fetcher...")
    logger.info(f"Feeds: {[f['name'] for f in RSS_FEEDS]}")

    articles = fetch_all_feeds()

    if not articles:
        logger.warning("No articles fetched. Check feed URLs.")
        sys.exit(1)

    save_to_database(articles)

    logger.info("RSS fetch complete!")
    logger.info(f"Articles saved: {len(articles)}")
    logger.info("Preview:")
    for a in articles[:3]:
        logger.info(f"  [{a['source']}] {a['headline'][:60]}...")

    restart_bot()

if __name__ == "__main__":
    main()
