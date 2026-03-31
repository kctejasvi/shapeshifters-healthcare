# Shapeshifters Healthcare — Claude Code Project Memory

## What is Shapeshifters?

**Shapeshifters Healthcare** (shapeshifters.health) is a medical education, specialist access, and
clinical influence platform targeting India. It has three sub-platforms:

| Platform | Purpose | Audience |
|---|---|---|
| **Shapeshifters Consult** | Connect patients with verified specialists | Patients |
| **Shapeshifters Studios** | CME content production for doctors | Doctors / KOLs |
| **Shapeshifters Academy** | Clinical courses, guidelines, case-based learning | Doctors / Medical students |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Bot | Python 3.11+, python-telegram-bot v20+ |
| MCP Server | Python MCP SDK (mcp>=1.0.0) |
| Web server | Flask 3.0+, flask-compress, gunicorn |
| Database | Supabase (future — not yet integrated) |
| Deployment | Linux, systemd (bot), gunicorn (Flask) |
| SEO | Static HTML articles, schema.org JSON-LD, sitemap.xml |
| Analytics | Google Analytics 4 (tag placeholder in base.html) |
| Ads | Google AdSense (slot placeholders in templates) |

---

## Target Cities (Local SEO)

1. Bangalore
2. Mumbai
3. Hyderabad
4. Chennai
5. Delhi

---

## Target Specialties

1. Surgery (General Surgery, Laparoscopic)
2. Diabetes & Endocrinology
3. Oncology (Cancer Care)
4. General Medicine
5. Dermatology

---

## Affiliate Partners

| # | Partner | Product Type | Link Format |
|---|---|---|---|
| 1 | **1mg** | Pharmacy + Lab Tests | `https://1mg.com/?utm_source=shapeshifters` |
| 2 | **Thyrocare** | Lab Tests (budget) | `https://thyrocare.com/?ref=shapeshifters` |
| 3 | **PharmEasy** | Pharmacy | `https://pharmeasy.in/?utm_source=shapeshifters` |
| 4 | **Practo** | Doctor Software | `https://practo.com/?ref=shapeshifters` |
| 5 | **Niva Bupa** | Health Insurance | `https://nivabupa.com/?utm_source=shapeshifters` |
| 6 | **Star Health** | Health Insurance | `https://starhealth.in/?utm_source=shapeshifters` |
| 7 | **Amazon India** | Medical Books | `https://amzn.in/?tag=shapeshifters-21` |
| 8 | **Marrow** | NEET PG Courses | `https://marrow.com/?ref=shapeshifters` |
| 9 | **Dr. Morepen** | Glucometer / Devices | `https://drmorepen.com/?utm_source=shapeshifters` |
| 10 | **Minimalist** | Skincare | `https://beminimalist.co/?utm_source=shapeshifters` |

All affiliate links live in `.env` as `AFFILIATE_*` variables. The `affiliate.py` tool reads them
from environment with fallback to placeholder URLs so the system works before real links are added.

---

## AdSense Placement Rules

- **Three slots per article**: above-fold, mid-article, end-of-article
- `<div class="adsense-slot" data-slot="article-top"></div>` — above fold
- `<div class="adsense-slot" data-slot="article-mid"></div>` — mid-article
- `<div class="adsense-slot" data-slot="article-end"></div>` — end of article
- **NEVER** place AdSense slots inside clinical advice sections, drug dosage tables, or
  contraindication lists
- AdSense script placeholder: `<!-- ADSENSE_SCRIPT_HERE -->` in base.html `<head>`

---

## Ethical Rules (Non-Negotiable)

1. **Never recommend a drug or treatment for commission** — affiliate links are only placed
   near informational content (e.g. "where to buy", "get tested"), never inside clinical guidance.
2. All affiliate boxes must carry `<p class="affiliate-label">📋 Sponsored</p>`.
3. All affiliate links must use `rel="sponsored"`.
4. Drug information is for educational purposes only — always include disclaimer.
5. The bot must never give personalised medical advice; always redirect to Consult.
6. Editorial team review statement on every article: "Reviewed by Shapeshifters Editorial Team".

---

## File Structure

```
shapeshifters/
├── bot/
│   └── telegram_bot.py          # Telegram bot — all user-facing commands
├── mcp/
│   ├── server.py                 # MCP server exposing 21+ tools
│   └── tools/
│       ├── consult.py            # Doctor search, appointment booking logic
│       ├── studios.py            # CME content, KOL directory
│       ├── academy.py            # Course listings, clinical guidelines
│       ├── drug_reference.py     # Drug lookup, interactions, dosage
│       ├── medical_news.py       # Live medical news aggregation
│       ├── educational.py        # Myth busting, health tips, Q&A
│       └── affiliate.py          # Affiliate link routing and contextual matching
├── website/
│   ├── app.py                    # Flask web server
│   ├── articles/                 # All 32 SEO articles as .html files
│   ├── templates/
│   │   ├── base.html             # Master layout with GA + AdSense placeholders
│   │   ├── article.html          # Article page extending base
│   │   └── home.html             # Homepage
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── seo/
│   └── seo_content_strategy.py  # 32 article metadata + outlines + affiliate map
├── requirements.txt
├── .env                          # Real secrets — never commit
├── .env.example                  # Template — safe to commit
├── .gitignore
└── CLAUDE.md                     # This file
```

---

## How to Run

### Telegram Bot
```bash
cd /home/shapeshifters
python bot/telegram_bot.py
```

### MCP Server
```bash
cd /home/shapeshifters
python mcp/server.py
```

### Flask Website (dev)
```bash
cd /home/shapeshifters
flask --app website/app.py run --debug
```

### Flask Website (production)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "website.app:create_app()"
```

---

## Environment Variables Required

See `.env.example` for full list. Key variables:

```
TELEGRAM_BOT_TOKEN          # From @BotFather
AFFILIATE_1MG               # 1mg affiliate URL
AFFILIATE_THYROCARE         # Thyrocare affiliate URL
AFFILIATE_PHARMEASY         # PharmEasy affiliate URL
AFFILIATE_PRACTO            # Practo affiliate URL
AFFILIATE_NIVA_BUPA         # Niva Bupa insurance URL
AFFILIATE_STAR_HEALTH       # Star Health insurance URL
AFFILIATE_AMAZON            # Amazon Associates URL
AFFILIATE_MARROW            # Marrow affiliate URL
AFFILIATE_MOREPEN           # Dr. Morepen affiliate URL
AFFILIATE_MINIMALIST        # Minimalist skincare URL
BASE_URL                    # https://shapeshifters.health
```

---

## Key Decisions & Conventions

- Articles are static HTML (not database-driven) for maximum page speed and SEO
- Slug format: `{city}-{specialty}-{descriptor}` for local, `{specialty}-{topic}` for national
- Internal links always use relative paths: `href="/bangalore-diabetes-specialist"`
- Schema.org markup is JSON-LD, always in `<script type="application/ld+json">` in `<head>`
- Telegram bot messages use Markdown v2 formatting
- All Python files use `python-dotenv` — always call `load_dotenv()` at top of entry points
