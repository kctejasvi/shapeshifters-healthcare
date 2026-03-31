"""
Shapeshifters Healthcare — Flask Web Server

Routes:
  /                         → home page
  /<slug>                   → article page
  /specialty/<name>         → specialty article list
  /city/<name>              → city article list
  /news                     → medical news page
  /api/news                 → JSON news feed
  /api/drug/<name>          → JSON drug lookup
  /api/tip                  → JSON daily health tip
  /sitemap.xml              → auto-generated sitemap
  /robots.txt               → SEO robots file
  404                       → custom 404

Run (dev):
  flask --app website/app.py run --debug

Run (production):
  gunicorn -w 4 -b 0.0.0.0:8000 "website.app:create_app()"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, Response, abort, send_from_directory
from flask_compress import Compress

# ── Internal tool imports ────────────────────────────────────
from mcp.tools.drug_reference import search_drug
from mcp.tools.medical_news import get_medical_news
from mcp.tools.educational import get_daily_health_tip, explain_medical_term
from mcp.tools.affiliate import get_contextual_affiliates

# ── SEO article data ─────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'seo'))
from seo_content_strategy import ARTICLES, get_articles_by_specialty, get_articles_by_city


BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")
ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-production")

    # Gzip compression
    Compress(app)

    # Cache-control helper
    def cache(seconds: int = 3600):
        def decorator(f):
            from functools import wraps
            @wraps(f)
            def wrapped(*args, **kwargs):
                response = f(*args, **kwargs)
                if hasattr(response, 'headers'):
                    response.headers['Cache-Control'] = f'public, max-age={seconds}'
                return response
            return wrapped
        return decorator

    # ── Template context ─────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return {"base_url": BASE_URL}

    # ── Homepage ─────────────────────────────────────────────
    @app.route("/")
    def home():
        # Featured = top 6 by RPM
        featured = sorted(ARTICLES, key=lambda a: a.get("rpm_estimate", 0), reverse=True)[:6]
        news = get_medical_news(limit=5)
        return render_template(
            "home.html",
            featured_articles=featured,
            news=news,
        )

    # ── Article page ─────────────────────────────────────────
    @app.route("/<slug>")
    def article_page(slug: str):
        # Try to serve pre-built static HTML article
        html_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        if os.path.exists(html_path):
            with open(html_path, encoding="utf-8") as f:
                content = f.read()
            return Response(content, mimetype="text/html")

        # Fall back to dynamic template rendering with metadata
        meta = next((a for a in ARTICLES if a["slug"] == slug), None)
        if not meta:
            abort(404)

        affiliates = get_contextual_affiliates(
            topic=meta.get("specialty", ""),
            audience=meta.get("audience", "patient"),
        )

        related = [
            a for a in ARTICLES
            if a["specialty"] == meta["specialty"] and a["slug"] != slug
        ][:4]

        sidebar = sorted(ARTICLES, key=lambda a: a.get("rpm_estimate", 0), reverse=True)[:5]

        article_data = {
            **meta,
            "content": f"<p>This article is being written. Check back soon.</p>",
            "meta_description": f"Read about {meta['primary_keyword']} — expert information from Shapeshifters Healthcare.",
            "date_published": "2025-01-01",
            "date_modified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "faq": [],
        }

        return render_template(
            "article.html",
            article=article_data,
            related_articles=related,
            sidebar_articles=sidebar,
            sidebar_affiliates=affiliates.get("suggestions", [])[:2],
        )

    # ── Specialty listing page ───────────────────────────────
    @app.route("/specialty/<specialty_name>")
    def specialty_page(specialty_name: str):
        articles = get_articles_by_specialty(specialty_name.lower())
        news = get_medical_news(specialty=specialty_name, limit=3)
        return render_template(
            "home.html",
            featured_articles=articles,
            news=news,
            page_title=f"{specialty_name.title()} — Shapeshifters Healthcare",
        )

    # ── City listing page ────────────────────────────────────
    @app.route("/city/<city_name>")
    def city_page(city_name: str):
        articles = get_articles_by_city(city_name.title())
        news = get_medical_news(limit=3)
        return render_template(
            "home.html",
            featured_articles=articles,
            news=news,
            page_title=f"{city_name.title()} — Shapeshifters Healthcare",
        )

    # ── News page ────────────────────────────────────────────
    @app.route("/news")
    def news_page():
        news = get_medical_news(limit=20)
        return render_template("home.html", featured_articles=[], news=news)

    # ── API: News ────────────────────────────────────────────
    @app.route("/api/news")
    def api_news():
        specialty = __import__('flask').request.args.get('specialty')
        audience = __import__('flask').request.args.get('audience')
        limit = int(__import__('flask').request.args.get('limit', 5))
        news = get_medical_news(specialty=specialty, audience=audience, limit=limit)
        response = jsonify(news)
        response.headers['Cache-Control'] = 'public, max-age=1800'
        return response

    # ── API: Drug reference ──────────────────────────────────
    @app.route("/api/drug/<drug_name>")
    def api_drug(drug_name: str):
        result = search_drug(drug_name)
        response = jsonify(result)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response

    # ── API: Daily health tip ─────────────────────────────────
    @app.route("/api/tip")
    def api_tip():
        from flask import request as req
        specialty = req.args.get('specialty')
        audience = req.args.get('audience')
        tip = get_daily_health_tip(specialty=specialty, audience=audience)
        response = jsonify(tip)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response

    # ── Sitemap ───────────────────────────────────────────────
    @app.route("/sitemap.xml")
    def sitemap():
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        def priority(article):
            if article["type"] == "featured":
                return "1.0"
            if article["type"] == "local":
                return "1.0"
            if article["type"] == "national":
                return "0.9"
            return "0.7"

        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        # Homepage
        xml_parts.append(f"""  <url>
    <loc>{BASE_URL}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <lastmod>{today}</lastmod>
  </url>""")

        # All articles
        for a in ARTICLES:
            xml_parts.append(f"""  <url>
    <loc>{BASE_URL}/{a['slug']}</loc>
    <changefreq>monthly</changefreq>
    <priority>{priority(a)}</priority>
    <lastmod>{today}</lastmod>
  </url>""")

        xml_parts.append('</urlset>')

        response = Response("\n".join(xml_parts), mimetype="application/xml")
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response

    # ── robots.txt ────────────────────────────────────────────
    @app.route("/robots.txt")
    def robots():
        content = f"""User-agent: *
Allow: /

Disallow: /api/

Sitemap: {BASE_URL}/sitemap.xml
"""
        response = Response(content, mimetype="text/plain")
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response

    # ── Static files with caching ─────────────────────────────
    @app.after_request
    def add_cache_headers(response):
        if '/static/' in str(__import__('flask').request.path):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response

    # ── 404 handler ───────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    # ── 500 handler ───────────────────────────────────────────
    @app.errorhandler(500)
    def server_error(e):
        return render_template("404.html"), 500

    return app


# Allow direct run for development
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
