"""
Shapeshifters Healthcare — Telegram Bot
Run: python bot/telegram_bot.py

BotFather commands list:
start - Start the bot and see the main menu
help - List all available commands
consult - Find a specialist in your city
drug - Look up a drug by name (educational)
news - Latest medical news
tip - Today's health tip
explain - Explain a medical term in simple language
myth - Check if a health claim is myth or fact
guideline - Get a simplified clinical guideline (for doctors)
ask - Ask a health question
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

from mcp.tools.drug_reference import search_drug, get_drug_interactions
from mcp.tools.medical_news import get_medical_news
from mcp.tools.consult import find_specialist, list_cities, list_specialties
from mcp.tools.educational import (
    explain_medical_term,
    myth_or_fact,
    get_daily_health_tip,
    get_clinical_guideline,
    ask_health_question,
)
from mcp.tools.insurance_faqs import search_insurance_faq, list_insurers
from mcp.tools.appointment_scheduler import (
    get_departments,
    get_available_slots,
    book_opd_appointment,
    cancel_appointment,
    get_appointment_details,
    HOSPITALS,
)
from mcp.tools.surgical_checklist import (
    get_surgery_checklist,
    detect_surgery_type,
    get_preop_documents,
    get_postop_warnings,
    get_followup_schedule,
    SURGICAL_CHECKLISTS,
)

try:
    from mcp.tools.medical_news_live import (
        get_live_news,
        get_news_by_country,
        get_news_summary_live,
        LAST_UPDATED,
        SOURCES,
    )
    LIVE_NEWS_AVAILABLE = True
except ImportError:
    LIVE_NEWS_AVAILABLE = False

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://shapeshifters.health")

# ── Main menu keyboard ───────────────────────────────────────
MAIN_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🩺 Find a Specialist"), KeyboardButton("💊 Drug Reference")],
        [KeyboardButton("📰 Medical News"), KeyboardButton("💡 Health Tips")],
        [KeyboardButton("📅 Book OPD"), KeyboardButton("📋 Surgery Checklist")],
        [KeyboardButton("🔍 Ask a Health Question"), KeyboardButton("📖 Medical Terms")],
        [KeyboardButton("🏥 Insurance Help"), KeyboardButton("🎓 Academy")],
        [KeyboardButton("ℹ️ About")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# ── Session management ───────────────────────────────────────
USER_SESSIONS: dict = {}

def get_session(user_id: int) -> dict:
    if user_id not in USER_SESSIONS:
        USER_SESSIONS[user_id] = {"step": None, "data": {}}
    return USER_SESSIONS[user_id]

def clear_session(user_id: int) -> None:
    USER_SESSIONS[user_id] = {"step": None, "data": {}}


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def _escape_md(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    special = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in special else c for c in str(text))


def _format_drug(drug: dict) -> str:
    """Format drug info as a readable Telegram message."""
    d = drug.get("drug", drug)
    lines = [
        f"💊 *{_escape_md(d['generic_name'])}*",
        f"",
        f"*Brand names in India:* {_escape_md(', '.join(d.get('brand_names_india', [])))}",
        f"*Class:* {_escape_md(d.get('class', 'N/A'))}",
        f"*Usual dose:* {_escape_md(d.get('usual_dose', 'See prescribing info'))}",
        f"",
        f"*Common side effects:*",
    ]
    for se in d.get("common_side_effects", [])[:4]:
        lines.append(f"• {_escape_md(se)}")
    lines.append("")
    lines.append(f"*Availability:* {_escape_md(d.get('availability_india', 'N/A'))}")
    lines.append(f"*Approx cost:* {_escape_md(d.get('approx_cost_india', 'N/A'))}")
    lines.append("")
    lines.append(f"_{_escape_md(drug.get('disclaimer', ''))}_")
    if d.get("article_link"):
        lines.append(f"")
        lines.append(f"📖 [Read full article]({BASE_URL}{d['article_link']})")
    return "\n".join(lines)


def _format_tip(tip: dict) -> str:
    """Format daily health tip as Telegram message."""
    lines = [
        f"💡 *Today's Health Tip*",
        f"",
        f"{_escape_md(tip['tip'])}",
        f"",
        f"📌 _{_escape_md(tip['specialty'].title())} · {_escape_md(tip['audience'].title())}_",
    ]
    if tip.get("affiliate_copy") and tip.get("affiliate_link"):
        lines.append(f"")
        lines.append(f"🛒 [{_escape_md(tip['affiliate_copy'])}]({tip['affiliate_link']})")
    return "\n".join(lines)


def _format_myth(result: dict) -> str:
    """Format myth-or-fact result as Telegram message."""
    if not result.get("found"):
        return (
            f"🤔 We couldn't match that statement\\.\n\n"
            f"Try rephrasing or [ask a specialist]({BASE_URL}/consult)\\."
        )
    lines = [
        f"🔬 *Myth or Fact Check*",
        f"",
        f"*Statement:* _{_escape_md(result['statement'])}_",
        f"",
        f"*Verdict:* {_escape_md(result['verdict_display'])}",
        f"",
        f"{_escape_md(result['explanation'])}",
        f"",
        f"📚 Source: _{_escape_md(result['source'])}_",
        f"",
        f"_{_escape_md(result.get('disclaimer', ''))}_",
    ]
    return "\n".join(lines)


def _format_guideline(result: dict) -> str:
    """Format clinical guideline as Telegram message."""
    if not result.get("found"):
        return f"No guideline found\\. Browse all at [Shapeshifters Academy]({BASE_URL}/academy)\\."
    lines = [
        f"📋 *{_escape_md(result['title'])}*",
        f"",
        f"*Key Points:*",
    ]
    for point in result.get("key_points", []):
        lines.append(f"• {_escape_md(point)}")
    lines.append("")
    lines.append(f"📖 [Full Guideline]({result['full_guideline_url']})")
    lines.append(f"🎓 [CME Course]({result['academy_cta']})")
    return "\n".join(lines)


def _format_qa(result: dict) -> str:
    """Format Q&A answer as Telegram message."""
    if not result.get("found"):
        return (
            f"🩺 We don't have a pre\\-built answer for that yet\\.\n\n"
            f"[{_escape_md(result.get('consult_cta_text', 'Speak to a specialist'))}]({result.get('consult_url', BASE_URL + '/consult')})"
        )
    lines = [
        f"❓ *{_escape_md(result['question'].title())}*",
        f"",
        f"{_escape_md(result['answer'])}",
        f"",
        f"_{_escape_md(result.get('disclaimer', ''))}_",
        f"",
        f"🩺 [Need personalised advice? Consult a specialist]({BASE_URL}/consult)",
    ]
    return "\n".join(lines)


def _format_insurer_list(data: dict) -> str:
    """Format list of empanelled insurers as Telegram message."""
    lines = [
        f"🏥 *{_escape_md(data['hospital'])}*",
        f"*{data['total']} Empanelled Insurance Companies*\n",
    ]
    for i, ins in enumerate(data["insurers"], 1):
        lines.append(
            f"*{i}\\. {_escape_md(ins['name'])}*\n"
            f"   📞 {_escape_md(ins['helpline'])}\n"
            f"   TPA: {_escape_md(ins['tpa'])}"
        )
        lines.append("")
    lines.append(f"_{_escape_md(data['note'])}_")
    return "\n".join(lines)


def _format_insurance_faq(result: dict) -> str:
    """Format insurance FAQ search result as Telegram message."""
    if not result["found"]:
        companies = ", ".join(_escape_md(c) for c in result["all_companies"])
        return (
            f"🔎 No insurance info found for *{_escape_md(result['query'])}*\\.\n\n"
            f"Try one of these insurers:\n{companies}\n\n"
            f"Or ask about topics: cashless, reimbursement, documents, TPA\\."
        )

    lines = []

    # Company info block
    ci = result.get("company_info")
    if ci:
        lines += [
            f"🏥 *{_escape_md(ci['name'])}*",
            f"",
            f"📞 Helpline: `{_escape_md(ci['helpline'])}`",
            f"🏢 TPA: {_escape_md(ci['tpa'])}",
            f"",
            f"*Cashless Process:*",
            f"_{_escape_md(ci['cashless_process'])}_",
            f"",
            f"*Reimbursement:*",
            f"_{_escape_md(ci['claim_process'])}_",
            f"",
        ]

    # Company-specific FAQs
    if result["company_faqs"]:
        lines.append(f"*Frequently Asked Questions:*\n")
        for faq in result["company_faqs"]:
            lines.append(f"❓ *{_escape_md(faq['q'])}*")
            lines.append(f"{_escape_md(faq['a'])}\n")

    # General FAQs
    if result["general_faqs"] and not result["company_faqs"]:
        lines.append(f"*General Insurance FAQs:*\n")
        for faq in result["general_faqs"]:
            lines.append(f"❓ *{_escape_md(faq['q'])}*")
            lines.append(f"{_escape_md(faq['a'])}\n")

    lines.append(f"_{_escape_md(result['disclaimer'])}_")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name or "there"
    text = (
        f"👋 Hello, {_escape_md(name)}\\!\n\n"
        f"Welcome to *Shapeshifters Healthcare* — India's trusted medical education platform\\.\n\n"
        f"I can help you with:\n"
        f"• 🩺 Finding a specialist in your city\n"
        f"• 💊 Drug reference \\(educational\\)\n"
        f"• 📰 Latest medical news\n"
        f"• 💡 Daily health tips\n"
        f"• 🔍 Health questions answered\n"
        f"• 📖 Medical terms explained\n"
        f"• 🎓 CME courses for doctors\n"
        f"• 🏥 Insurance & cashless queries \\(11 insurers\\)\n\n"
        f"Use the menu below or type /help for all commands\\."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=MAIN_MENU)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📋 *Shapeshifters Bot — All Commands*\n\n"
        "*For Patients:*\n"
        "/consult \\<specialty\\> — Find a specialist\n"
        "/drug \\<name\\> — Drug information\n"
        "/news — Latest medical news\n"
        "/tip — Today's health tip\n"
        "/explain \\<term\\> — Explain a medical term\n"
        "/myth \\<statement\\> — Myth or fact checker\n"
        "/ask \\<question\\> — Health question answered\n\n"
        "*For Doctors:*\n"
        "/guideline \\<specialty\\> \\<topic\\> — Clinical guidelines\n"
        "/tip doctor — Doctor\\-focused tips\n"
        "/news — Medical news\n\n"
        "*Insurance \\(Eesha Hospital\\):*\n"
        "/insurance \\<company\\> — Cashless & claim FAQs\n"
        "/insurers — All 11 empanelled insurers\n"
        "/cashless \\<company\\> — Cashless pre\\-auth guide\n\n"
        "*About Shapeshifters:*\n"
        "🩺 [Consult]({consult}) · 🎓 [Academy]({academy}) · 🎬 [Studios]({studios})\n\n"
        "⚕️ _All content is educational only\\. Always consult a qualified doctor for personal medical advice\\._"
    ).format(consult=BASE_URL + "/consult", academy=BASE_URL + "/academy", studios=BASE_URL + "/studios")
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=MAIN_MENU)


async def consult_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /consult [specialty] [city]
    e.g. /consult diabetes Bangalore
    """
    args = context.args
    if not args:
        # Show specialty picker
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🩸 Diabetes", callback_data="consult_diabetes"),
             InlineKeyboardButton("🎗️ Oncology", callback_data="consult_oncology")],
            [InlineKeyboardButton("🔪 Surgery", callback_data="consult_surgery"),
             InlineKeyboardButton("✨ Dermatology", callback_data="consult_dermatology")],
            [InlineKeyboardButton("❤️ General Medicine", callback_data="consult_general_medicine")],
        ])
        await update.message.reply_text(
            "🩺 *Find a Specialist*\n\nWhich specialty do you need?",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
        return

    specialty = args[0]
    city = args[1] if len(args) > 1 else None
    result = find_specialist(specialty, city)

    if not result.get("found"):
        await update.message.reply_text(
            f"❌ {_escape_md(result['message'])}",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    city_str = _escape_md(result["city"])
    spec_str = _escape_md(result["specialty"])
    cta_url = result["cta_url"]
    conditions = "\n".join(f"• {_escape_md(c)}" for c in result["common_conditions"][:4])

    text = (
        f"🩺 *{spec_str} Specialist — {city_str}*\n\n"
        f"*Common conditions treated:*\n{conditions}\n\n"
        f"[{_escape_md(result['cta_text'])}]({cta_url})\n\n"
        f"_Verified specialists · Same\\-day appointments available_"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=MAIN_MENU)


async def consult_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks for /consult specialty picker."""
    query = update.callback_query
    await query.answer()
    specialty = query.data.replace("consult_", "")
    result = find_specialist(specialty)
    if result.get("found"):
        text = (
            f"🩺 *{_escape_md(result['specialty'])} Specialists*\n\n"
            f"[Book a consultation online]({result['cta_url']})\n\n"
            f"_All cities · Same\\-day available_"
        )
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2)


async def drug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /drug <name>
    e.g. /drug metformin
    """
    if not context.args:
        await update.message.reply_text(
            "💊 *Drug Reference*\n\nUsage: `/drug <name>`\nExample: `/drug metformin`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    name = " ".join(context.args)
    result = search_drug(name)

    if not result.get("found"):
        await update.message.reply_text(
            f"❌ {_escape_md(result['message'])}\n\n"
            f"[Ask a specialist instead]({BASE_URL}/consult)",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    await update.message.reply_text(
        _format_drug(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


def format_live_news(result: dict, source_line: str = "") -> str:
    if result.get("status") != "success":
        return f"😔 {result.get('message', 'No news available right now.')}"

    lines = [f"📰 *Medical News*\n{source_line}\n"]
    for n in result.get("news", []):
        impact_icon = "🔴" if n.get("impact") == "High" else "🟡"
        country_flag = "🇮🇳" if n.get("country") == "India" else "🌍"
        headline = n.get("headline", "")[:80]
        summary  = n.get("summary",  "")[:120]
        source   = n.get("source", "")
        url      = n.get("url", n.get("read_more", ""))

        lines.append(
            f"{impact_icon}{country_flag} *{headline}*\n"
            f"   _{summary}..._\n"
            f"   📚 {source}\n"
            f"   🔗 {url}\n"
        )
    return "\n".join(lines)


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /news [specialty]
    e.g. /news diabetes
    """
    specialty = " ".join(context.args) if context.args else ""

    if LIVE_NEWS_AVAILABLE:
        result = await get_live_news({
            "specialty": specialty,
            "limit": 4
        })
        source_line = f"📡 Live from: {', '.join(SOURCES)}\n🕐 Updated: {LAST_UPDATED}"
    else:
        news_items = get_medical_news(specialty=specialty if specialty else None, limit=4)
        result = {"status": "success", "news": [
            {"headline": n["title"], "summary": n["summary"], "source": n["source"],
             "country": "India", "impact": "Medium", "url": "", "read_more": ""}
            for n in news_items
        ]} if news_items else {"status": "no_results", "message": "No news available right now."}
        source_line = "📋 Curated medical news"

    text = format_live_news(result, source_line)
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇳 India News",         callback_data="news_india")],
            [InlineKeyboardButton("🌍 International News",  callback_data="news_international")],
            [InlineKeyboardButton("🔴 High Impact Only",    callback_data="news_high")],
            [InlineKeyboardButton("🏠 Main Menu",           callback_data="back_main")],
        ]),
    )


def format_slot_result(result: dict) -> str:
    if result.get("status") != "success":
        return f"❌ {result.get('message', 'No slots available.')}"
    lines = [
        f"📅 *Available Slots — {result['department']}*",
        f"🗓 {result['day']}, {result['date']}\n",
    ]
    for doc in result.get("doctors", []):
        lines.append(f"👨‍⚕️ *{doc['name']}*")
        lines.append(f"💰 Fee: ₹{doc['fee']}")
        slots = doc.get("available_slots", [])
        if slots:
            lines.append("⏰ Available: " + "  ".join(slots[:10]))
        else:
            lines.append("⏰ No slots available")
        lines.append("")
    return "\n".join(lines)


def format_booking_confirmation(result: dict) -> str:
    lines = [
        f"✅ *Appointment Confirmed!*\n",
        f"🆔 Reference: `{result['reference']}`",
        f"🏥 {result['hospital']}",
        f"🏷️ Department: {result['department']}",
        f"👨‍⚕️ Doctor: {result['doctor']}",
        f"👤 Patient: {result['patient_name']}",
        f"📅 Date: {result['date']} ({result['day']})",
        f"⏰ Time: {result['time']}",
        f"💰 Consultation Fee: ₹{result['fee']}",
        f"\n📌 *Instructions:*",
    ]
    for inst in result.get("instructions", []):
        lines.append(f"  • {inst}")
    lines.append(f"\n💾 Save your reference: `{result['reference']}`")
    return "\n".join(lines)


def format_checklist(result: dict, phase: str) -> str:
    if result.get("status") != "success":
        return f"❌ {result.get('message', 'Checklist not available.')}"

    checklist = result.get("checklist", {})
    surgery   = result.get("surgery_name", "Surgery")
    phase_label = "Pre-Op" if phase == "pre_op" else "Post-Op"
    lines = [f"📋 *{surgery} — {phase_label} Checklist*\n"]

    if phase == "pre_op":
        if "7_days_before" in checklist:
            lines.append("*7 Days Before:*")
            for item in checklist["7_days_before"]:
                lines.append(f"  ✅ {item}")
        if "night_before" in checklist:
            lines.append("\n*Night Before Surgery:*")
            for item in checklist["night_before"]:
                lines.append(f"  🌙 {item}")
        if "day_of_surgery" in checklist:
            lines.append("\n*Day of Surgery:*")
            for item in checklist["day_of_surgery"]:
                lines.append(f"  🏥 {item}")
    else:
        if "in_hospital" in checklist:
            lines.append("*While in Hospital:*")
            for item in checklist["in_hospital"]:
                lines.append(f"  🏥 {item}")
        if "week_1_at_home" in checklist:
            lines.append("\n*First Week at Home:*")
            for item in checklist["week_1_at_home"][:5]:
                lines.append(f"  🏠 {item}")

    lines.append("\n_Always follow your surgeon's specific instructions above all._")
    return "\n".join(lines)


async def opd_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/opd — Show OPD departments and booking option."""
    result = await get_departments({})
    depts  = result["departments"]
    lines  = ["🏥 *Eesha Multispeciality Hospital*\n*OPD Departments*\n"]
    for d in depts:
        lines.append(f"• {d['name']}")
    lines.append(f"\n🕐 OPD Hours: {result['opd_hours']}")
    lines.append("\n💬 Book: `/book <department>`\nExample: `/book cardiology`")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Book Appointment", callback_data="opd_book_start")],
        [InlineKeyboardButton("🏠 Main Menu",        callback_data="back_main")],
    ])
    await update.message.reply_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/book [department] — Start OPD booking flow."""
    user_id = update.effective_user.id
    session = get_session(user_id)

    if context.args:
        dept_search = " ".join(context.args)
        # Find the department code
        hospital = HOSPITALS["eesha"]
        dept_key = None
        dept_code = None
        for key, dept in hospital["departments"].items():
            if dept_search.lower() in dept["name"].lower() or dept_search.lower() in key.lower():
                dept_key = key
                dept_code = dept["code"]
                dept_name = dept["name"]
                break
        if not dept_code:
            dept_code = dept_search[:2].upper()
            dept_name = dept_search.title()

        session["data"]["department_code"] = dept_code
        session["data"]["department_name"] = dept_name
        session["step"] = "awaiting_opd_date"
        await update.message.reply_text(
            f"📅 *Book OPD — {dept_name}*\n\n"
            f"Which date would you like?\n\nType: `today`, `tomorrow`, or a date like `2025-09-20`",
            parse_mode="Markdown",
        )
    else:
        session["step"] = "awaiting_opd_department"
        result = await get_departments({})
        depts  = result["departments"]
        keyboard_buttons = []
        for i in range(0, len(depts), 2):
            row = [InlineKeyboardButton(depts[i]["name"], callback_data=f"opd_dept_{depts[i]['code']}")]
            if i + 1 < len(depts):
                row.append(InlineKeyboardButton(depts[i+1]["name"], callback_data=f"opd_dept_{depts[i+1]['code']}"))
            keyboard_buttons.append(row)
        keyboard_buttons.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")])
        await update.message.reply_text(
            "🏥 *Book OPD Appointment*\n*Eesha Multispeciality Hospital*\n\nSelect department:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard_buttons),
        )


async def checklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/checklist [surgery type] — Get pre/post op checklist."""
    if context.args:
        query    = " ".join(context.args)
        surgery  = detect_surgery_type(query)
        result   = await get_surgery_checklist({"surgery_type": surgery, "phase": "pre_op"})
        text     = format_checklist(result, "pre_op")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏥 Post-Op Checklist", callback_data=f"checklist_post_{surgery}")],
            [InlineKeyboardButton("⚠️ Warning Signs",     callback_data=f"checklist_warn_{surgery}")],
            [InlineKeyboardButton("📋 Documents Needed",  callback_data=f"checklist_docs_{surgery}")],
            [InlineKeyboardButton("🏠 Main Menu",         callback_data="back_main")],
        ])
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔪 General Surgery",     callback_data="checklist_start_general_surgery")],
            [InlineKeyboardButton("🦴 Orthopaedic Surgery", callback_data="checklist_start_orthopaedic_surgery")],
            [InlineKeyboardButton("🔬 Laparoscopic",        callback_data="checklist_start_laparoscopic_surgery")],
            [InlineKeyboardButton("❤️ Cardiac Surgery",    callback_data="checklist_start_cardiac_surgery")],
            [InlineKeyboardButton("🏠 Main Menu",           callback_data="back_main")],
        ])
        await update.message.reply_text(
            "📋 *Surgery Checklist*\n\nSelect your surgery type:",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )


async def myappointment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/myappointment <reference> — View appointment details."""
    if context.args:
        ref    = context.args[0].upper()
        result = await get_appointment_details({"reference_id": ref})
        if result["status"] == "success":
            appt = result["appointment"]
            text = (
                f"📅 *Appointment Details*\n\n"
                f"🆔 Ref: `{appt['reference']}`\n"
                f"🏥 {appt['hospital']}\n"
                f"🏷️ {appt['department']}\n"
                f"👨‍⚕️ {appt['doctor']}\n"
                f"👤 {appt['patient_name']}\n"
                f"📅 {appt['date']} ({appt['day']})\n"
                f"⏰ {appt['time_slot']}\n"
                f"💰 Fee: ₹{appt['fee']}\n"
                f"📌 Status: {appt['status'].title()}"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel Appointment", callback_data=f"cancel_{ref}")],
                [InlineKeyboardButton("🏠 Main Menu",         callback_data="back_main")],
            ])
        else:
            text = f"❌ {result['message']}\n\nCheck your reference number and try again."
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📅 Book New Appointment", callback_data="opd_book_start")],
            ])
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Usage: `/myappointment EH-OPD-XXXXXXXX`\n\nEnter your appointment reference number.",
            parse_mode="Markdown",
        )


async def tip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /tip [specialty] [audience]
    e.g. /tip diabetes patient
         /tip doctor
    """
    args = context.args
    specialty = None
    audience = None

    if args:
        # Check if first arg is audience or specialty
        if args[0].lower() in ("doctor", "patient"):
            audience = args[0].lower()
        else:
            specialty = args[0].lower()
        if len(args) > 1 and args[1].lower() in ("doctor", "patient"):
            audience = args[1].lower()

    tip = get_daily_health_tip(specialty=specialty, audience=audience)
    await update.message.reply_text(
        _format_tip(tip),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /explain <medical term>
    e.g. /explain HbA1c
    """
    if not context.args:
        await update.message.reply_text(
            "📖 *Explain a Medical Term*\n\nUsage: `/explain <term>`\nExample: `/explain HbA1c`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    term = " ".join(context.args)
    result = explain_medical_term(term)

    if not result.get("found"):
        await update.message.reply_text(
            f"❓ Term *{_escape_md(term)}* not found\\.\n\n"
            f"[Ask a specialist]({BASE_URL}/consult)",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    lines = [
        f"📖 *{_escape_md(term.title())}*\n",
        f"{_escape_md(result['simple'])}\n",
        f"*Who needs to know:* {_escape_md(result['who_needs_to_know'])}\n",
        f"_{_escape_md(result['disclaimer'])}_",
    ]
    if result.get("article_link"):
        lines.append(f"\n📚 [Read full article]({result['article_link']})")

    await update.message.reply_text(
        "\n".join(lines),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def myth_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /myth <statement>
    e.g. /myth diabetics cannot eat rice
    """
    if not context.args:
        await update.message.reply_text(
            "🔬 *Myth or Fact Checker*\n\nUsage: `/myth <statement>`\nExample: `/myth diabetics cannot eat rice`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    statement = " ".join(context.args)
    result = myth_or_fact(statement)
    await update.message.reply_text(
        _format_myth(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
    )


async def guideline_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /guideline <specialty> <topic>
    e.g. /guideline diabetes type2
         /guideline dermatology acne
    """
    if len(context.args) < 2:
        await update.message.reply_text(
            "📋 *Clinical Guidelines*\n\n"
            "Usage: `/guideline <specialty> <topic>`\n\n"
            "Examples:\n"
            "• `/guideline diabetes type2`\n"
            "• `/guideline dermatology acne`\n"
            "• `/guideline general hypertension`\n"
            "• `/guideline oncology cancer_screening`\n"
            "• `/guideline surgery antibiotic_prophylaxis`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    specialty = context.args[0]
    topic = "_".join(context.args[1:])
    result = get_clinical_guideline(specialty, topic)
    await update.message.reply_text(
        _format_guideline(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /ask <question>
    e.g. /ask what is normal blood sugar
    """
    if not context.args:
        await update.message.reply_text(
            "🔍 *Ask a Health Question*\n\nUsage: `/ask <question>`\nExample: `/ask what is normal blood sugar`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    question = " ".join(context.args)
    result = ask_health_question(question)
    await update.message.reply_text(
        _format_qa(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def insurance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /insurance [company or topic]
    e.g. /insurance niva bupa
         /insurance cashless
         /insurance reimbursement
    """
    if not context.args:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Cashless Process", callback_data="ins_cashless"),
             InlineKeyboardButton("📄 Reimbursement", callback_data="ins_reimbursement")],
            [InlineKeyboardButton("📋 All Insurers", callback_data="ins_list"),
             InlineKeyboardButton("📑 Documents Needed", callback_data="ins_documents")],
        ])
        await update.message.reply_text(
            "🏥 *Insurance Help — Eesha Multispeciality Hospital*\n\n"
            "We are empanelled with *11 insurance companies*\\.\n\n"
            "Choose a topic or type `/insurance <company name>` for insurer\\-specific FAQs\\.\n\n"
            "Examples:\n"
            "• `/insurance niva bupa`\n"
            "• `/insurance tata aig`\n"
            "• `/insurance cashless`\n"
            "• `/insurance reimbursement`",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
        return

    query = " ".join(context.args)
    result = search_insurance_faq(query)
    await update.message.reply_text(
        _format_insurance_faq(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def insurers_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/insurers — List all 11 empanelled insurance companies."""
    data = list_insurers()
    await update.message.reply_text(
        _format_insurer_list(data),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
    )


async def cashless_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /cashless [company]
    e.g. /cashless sbi general
    Quick lookup of the cashless process.
    """
    if context.args:
        company = " ".join(context.args)
        result = search_insurance_faq("cashless", company=company)
    else:
        result = search_insurance_faq("cashless")

    await update.message.reply_text(
        _format_insurance_faq(result),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def insurance_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks for insurance menu."""
    query = update.callback_query
    await query.answer()
    action = query.data  # ins_cashless / ins_reimbursement / ins_list / ins_documents

    if action == "ins_list":
        data = list_insurers()
        text = _format_insurer_list(data)
    elif action == "ins_cashless":
        result = search_insurance_faq("cashless")
        text = _format_insurance_faq(result)
    elif action == "ins_reimbursement":
        result = search_insurance_faq("reimbursement")
        text = _format_insurance_faq(result)
    elif action == "ins_documents":
        result = search_insurance_faq("documents")
        text = _format_insurance_faq(result)
    else:
        text = "Unknown action\\."

    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2)


async def opd_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle OPD booking inline keyboard callbacks."""
    query   = update.callback_query
    await query.answer()
    data    = query.data
    user_id = query.from_user.id
    session = get_session(user_id)

    if data == "opd_book_start":
        session["step"] = "awaiting_opd_department"
        result = await get_departments({})
        depts  = result["departments"]
        keyboard_buttons = []
        for i in range(0, len(depts), 2):
            row = [InlineKeyboardButton(depts[i]["name"], callback_data=f"opd_dept_{depts[i]['code']}")]
            if i + 1 < len(depts):
                row.append(InlineKeyboardButton(depts[i+1]["name"], callback_data=f"opd_dept_{depts[i+1]['code']}"))
            keyboard_buttons.append(row)
        keyboard_buttons.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")])
        await query.edit_message_text(
            "🏥 *Book OPD Appointment*\n*Eesha Multispeciality Hospital*\n\nSelect department:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard_buttons),
        )

    elif data.startswith("opd_dept_"):
        dept_code = data.replace("opd_dept_", "")
        # Find department name
        dept_name = dept_code
        for dept in HOSPITALS["eesha"]["departments"].values():
            if dept["code"] == dept_code:
                dept_name = dept["name"]
                break
        session["data"]["department_code"] = dept_code
        session["data"]["department_name"] = dept_name
        session["step"] = "awaiting_opd_date"
        await query.edit_message_text(
            f"📅 *Book OPD — {dept_name}*\n\n"
            f"Which date would you like?\n\nType: `today`, `tomorrow`, or a date like `2025-09-20`",
            parse_mode="Markdown",
        )

    elif data.startswith("opd_slot_"):
        # Format: opd_slot_DR001_9:00
        parts     = data.replace("opd_slot_", "").split("_", 1)
        doctor_id = parts[0]
        time_slot = parts[1] if len(parts) > 1 else ""
        session["data"]["doctor_id"]  = doctor_id
        session["data"]["time_slot"]  = time_slot
        session["step"] = "awaiting_opd_patient_name"
        await query.edit_message_text(
            f"⏰ Slot selected: *{time_slot}*\n\n👤 Please type the *patient's full name*:",
            parse_mode="Markdown",
        )

    elif data.startswith("cancel_"):
        ref = data.replace("cancel_", "")
        session["data"]["cancel_ref"] = ref
        session["step"] = "awaiting_cancel_phone"
        await query.edit_message_text(
            f"❌ *Cancel Appointment {ref}*\n\n"
            f"Please type the *phone number* used during booking to confirm cancellation:",
            parse_mode="Markdown",
        )


async def checklist_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle surgery checklist inline keyboard callbacks."""
    query = update.callback_query
    await query.answer()
    data  = query.data

    if data == "checklist_menu":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔪 General Surgery",      callback_data="checklist_start_general_surgery")],
            [InlineKeyboardButton("🦴 Orthopaedic Surgery",  callback_data="checklist_start_orthopaedic_surgery")],
            [InlineKeyboardButton("🔬 Laparoscopic Surgery", callback_data="checklist_start_laparoscopic_surgery")],
            [InlineKeyboardButton("❤️ Cardiac Surgery",     callback_data="checklist_start_cardiac_surgery")],
            [InlineKeyboardButton("🏠 Main Menu",            callback_data="back_main")],
        ])
        await query.edit_message_text(
            "📋 *Surgery Checklist*\n\nSelect your surgery type:",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    elif data.startswith("checklist_start_"):
        surgery_type = data.replace("checklist_start_", "")
        result = await get_surgery_checklist({"surgery_type": surgery_type, "phase": "pre_op"})
        text   = format_checklist(result, "pre_op")
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏥 Post-Op Guide",  callback_data=f"checklist_post_{surgery_type}")],
                [InlineKeyboardButton("⚠️ Warning Signs",  callback_data=f"checklist_warn_{surgery_type}")],
                [InlineKeyboardButton("📋 Documents",      callback_data=f"checklist_docs_{surgery_type}")],
                [InlineKeyboardButton("📅 Follow-Up",      callback_data=f"checklist_followup_{surgery_type}")],
                [InlineKeyboardButton("🏠 Main Menu",      callback_data="back_main")],
            ]),
        )

    elif data.startswith("checklist_post_"):
        surgery_type = data.replace("checklist_post_", "")
        result = await get_surgery_checklist({"surgery_type": surgery_type, "phase": "post_op"})
        text   = format_checklist(result, "post_op")
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚠️ Warning Signs", callback_data=f"checklist_warn_{surgery_type}")],
                [InlineKeyboardButton("📅 Follow-Up",     callback_data=f"checklist_followup_{surgery_type}")],
                [InlineKeyboardButton("🏠 Main Menu",     callback_data="back_main")],
            ]),
        )

    elif data.startswith("checklist_warn_"):
        surgery_type = data.replace("checklist_warn_", "")
        result   = await get_postop_warnings({"surgery_type": surgery_type})
        warnings = result.get("warnings", [])
        text = f"⚠️ *When to Call Your Doctor — {result.get('surgery_name', '')}*\n\n"
        for w in warnings:
            text += f"🚨 {w}\n"
        text += "\n_When in doubt — call your doctor. Better safe than sorry._"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📅 Follow-Up Schedule", callback_data=f"checklist_followup_{surgery_type}")],
                [InlineKeyboardButton("🏠 Main Menu",          callback_data="back_main")],
            ]),
        )

    elif data.startswith("checklist_docs_"):
        surgery_type = data.replace("checklist_docs_", "")
        result = await get_preop_documents({"surgery_type": surgery_type})
        docs   = result.get("documents", [])
        text   = f"📋 *Documents Needed — {result.get('surgery_name', '')}*\n\n"
        for doc in docs:
            text += f"📄 {doc}\n"
        text += "\n_Carry originals + 2 photocopies of each._"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")],
            ]),
        )

    elif data.startswith("checklist_followup_"):
        surgery_type = data.replace("checklist_followup_", "")
        result   = await get_followup_schedule({"surgery_type": surgery_type})
        schedule = result.get("schedule", [])
        text     = f"📅 *Follow-Up Schedule — {result.get('surgery_name', '')}*\n\n"
        for appt in schedule:
            text += f"🗓️ {appt}\n"
        text += "\n_Do not miss follow-up appointments — they are critical for recovery._"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📅 Book Follow-Up", callback_data="opd_book_start")],
                [InlineKeyboardButton("🏠 Main Menu",      callback_data="back_main")],
            ]),
        )


async def news_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks for news filters."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.message.reply_text(
            "Choose an option from the menu below\\.",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=MAIN_MENU,
        )
        return

    elif data == "news_india":
        if LIVE_NEWS_AVAILABLE:
            result = await get_news_by_country({"country": "india"})
            source_line = "🇮🇳 Indian Medical News — Live"
        else:
            result = {"status": "no_results", "message": "Live news not available yet."}
            source_line = ""
        text = format_live_news(result, source_line)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌍 International", callback_data="news_international")],
                [InlineKeyboardButton("🏠 Main Menu",     callback_data="back_main")],
            ]),
        )

    elif data == "news_international":
        if LIVE_NEWS_AVAILABLE:
            result = await get_news_by_country({"country": "international"})
            source_line = "🌍 International Medical News — Live"
        else:
            result = {"status": "no_results", "message": "Live news not available yet."}
            source_line = ""
        text = format_live_news(result, source_line)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇮🇳 India News", callback_data="news_india")],
                [InlineKeyboardButton("🏠 Main Menu",   callback_data="back_main")],
            ]),
        )

    elif data == "news_high":
        if LIVE_NEWS_AVAILABLE:
            result = await get_live_news({"impact": "High", "limit": 4})
            source_line = "🔴 High Impact Medical News — Live"
        else:
            result = {"status": "no_results", "message": "Live news not available yet."}
            source_line = ""
        text = format_live_news(result, source_line)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇮🇳 India", callback_data="news_india")],
                [InlineKeyboardButton("🌍 World",  callback_data="news_international")],
                [InlineKeyboardButton("🏠 Menu",   callback_data="back_main")],
            ]),
        )


# ── Menu button handlers ─────────────────────────────────────
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route menu button taps and session steps to the appropriate handler."""
    text    = update.message.text.strip()
    user_id = update.effective_user.id
    session = get_session(user_id)
    step    = session.get("step")

    # If user taps a menu button mid-session, cancel the session and route normally
    MENU_BUTTONS = {
        "📅 Book OPD", "📋 Surgery Checklist", "🩺 Find a Specialist",
        "💊 Drug Reference", "📰 Medical News", "💡 Health Tips",
        "🔍 Ask a Health Question", "📖 Medical Terms",
        "🏥 Insurance Help", "🎓 Academy", "ℹ️ About",
    }
    if text in MENU_BUTTONS and step:
        clear_session(user_id)
        session = get_session(user_id)
        step = None

    # ── OPD booking session steps ─────────────────────────────
    if step == "awaiting_opd_date":
        session["data"]["date"] = text
        dept_code = session["data"].get("department_code", "")
        result = await get_available_slots({"department_code": dept_code, "date": text})
        if result["status"] == "success" and result.get("doctors"):
            session["data"]["slot_result"] = result
            session["step"] = "awaiting_opd_time_selection"
            text_reply = format_slot_result(result)
            # Build slot buttons
            buttons = []
            for doc in result["doctors"]:
                for slot in doc["available_slots"][:8]:
                    cb = f"opd_slot_{doc['doctor_id']}_{slot}"
                    buttons.append(InlineKeyboardButton(slot, callback_data=cb))
            rows = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
            rows.append([InlineKeyboardButton("🏠 Cancel", callback_data="back_main")])
            await update.message.reply_text(
                text_reply,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rows),
            )
        else:
            await update.message.reply_text(
                f"❌ {result.get('message', 'No slots available.')} Try a different date.",
                parse_mode="Markdown",
            )
        return

    if step == "awaiting_opd_patient_name":
        session["data"]["patient_name"] = text
        session["step"] = "awaiting_opd_phone"
        await update.message.reply_text("📱 Patient's *phone number*?", parse_mode="Markdown")
        return

    if step == "awaiting_opd_phone":
        session["data"]["patient_phone"] = text
        session["step"] = "awaiting_opd_reason"
        await update.message.reply_text(
            "📝 *Reason for visit* (type 'skip' to skip):",
            parse_mode="Markdown",
        )
        return

    if step == "awaiting_opd_reason":
        session["data"]["reason"] = "" if text.lower() == "skip" else text
        result = await book_opd_appointment(session["data"])
        clear_session(user_id)
        if result["status"] == "booked":
            text_reply = format_booking_confirmation(result)
        else:
            text_reply = f"❌ Booking failed: {result.get('message', 'Please try again.')}"
        await update.message.reply_text(
            text_reply,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Pre-Op Checklist", callback_data="checklist_start_general_surgery")],
                [InlineKeyboardButton("🏠 Main Menu",        callback_data="back_main")],
            ]),
        )
        return

    if step == "awaiting_cancel_phone":
        ref    = session["data"].get("cancel_ref", "")
        result = await cancel_appointment({"reference_id": ref, "patient_phone": text})
        clear_session(user_id)
        await update.message.reply_text(
            f"{'✅' if result['status'] == 'cancelled' else '❌'} {result['message']}",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU,
        )
        return

    if text == "📅 Book OPD":
        context.args = []
        await book_command(update, context)

    elif text == "📋 Surgery Checklist":
        context.args = []
        await checklist_command(update, context)

    elif text == "🩺 Find a Specialist":
        context.args = []
        await consult_command(update, context)

    elif text == "💊 Drug Reference":
        await update.message.reply_text(
            "💊 *Drug Reference*\n\nType: `/drug <name>`\nExample: `/drug metformin`\n\nAvailable drugs: metformin, semaglutide, tretinoin, levothyroxine, amlodipine, and more\\.",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    elif text == "📰 Medical News":
        context.args = []
        await news_command(update, context)

    elif text == "💡 Health Tips":
        context.args = []
        await tip_command(update, context)

    elif text == "🔍 Ask a Health Question":
        await update.message.reply_text(
            "🔍 *Ask a Health Question*\n\nType: `/ask <question>`\nExample: `/ask what is normal blood pressure`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    elif text == "📖 Medical Terms":
        await update.message.reply_text(
            "📖 *Medical Terms*\n\nType: `/explain <term>`\nExample: `/explain HbA1c`\n\nTerms available: HbA1c, insulin resistance, biopsy, metastasis, tretinoin, TSH, eGFR, BMI, and more\\.",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    elif text == "🏥 Insurance Help":
        context.args = []
        await insurance_command(update, context)

    elif text == "🎓 Academy":
        await update.message.reply_text(
            f"🎓 *Shapeshifters Academy*\n\nCME courses for Indian doctors\\.\nEarn NMC\\-recognised credits online\\.\n\n[Browse Courses]({BASE_URL}/academy)",
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    elif text == "ℹ️ About":
        await update.message.reply_text(
            f"*About Shapeshifters Healthcare*\n\n"
            f"India's trusted medical education and specialist access platform\\.\n\n"
            f"🩺 [Consult]({BASE_URL}/consult) — verified specialists in 5 cities\n"
            f"🎓 [Academy]({BASE_URL}/academy) — CME courses for doctors\n"
            f"🎬 [Studios]({BASE_URL}/studios) — clinical video modules\n\n"
            f"⚕️ _Educational content only\\. Not medical advice\\._",
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )

    else:
        # Treat as a free-text health question
        context.args = text.split()
        await ask_command(update, context)


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment. Copy .env.example to .env and add your token.")

    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("consult", consult_command))
    app.add_handler(CommandHandler("drug", drug_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("tip", tip_command))
    app.add_handler(CommandHandler("explain", explain_command))
    app.add_handler(CommandHandler("myth", myth_command))
    app.add_handler(CommandHandler("guideline", guideline_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("insurance", insurance_command))
    app.add_handler(CommandHandler("insurers", insurers_command))
    app.add_handler(CommandHandler("cashless", cashless_command))
    app.add_handler(CommandHandler("opd", opd_command))
    app.add_handler(CommandHandler("book", book_command))
    app.add_handler(CommandHandler("checklist", checklist_command))
    app.add_handler(CommandHandler("myappointment", myappointment_command))

    # Inline keyboard callbacks
    app.add_handler(CallbackQueryHandler(consult_callback,   pattern=r"^consult_"))
    app.add_handler(CallbackQueryHandler(insurance_callback, pattern=r"^ins_"))
    app.add_handler(CallbackQueryHandler(opd_callback,       pattern=r"^(opd_|cancel_)"))
    app.add_handler(CallbackQueryHandler(checklist_callback, pattern=r"^checklist_"))
    app.add_handler(CallbackQueryHandler(news_callback,      pattern=r"^(news_|back_main)"))

    # Menu button and free-text handler (must be last)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    logger.info("Shapeshifters Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
