"""
Shapeshifters Healthcare — MCP Server
Exposes all tools via the Model Context Protocol.

Run: python mcp/server.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from mcp.tools.drug_reference import search_drug, get_drug_interactions
from mcp.tools.medical_news import get_medical_news
from mcp.tools.consult import find_specialist, get_second_opinion_cta, list_cities, list_specialties
from mcp.tools.studios import list_cme_modules, get_module, get_studios_cta
from mcp.tools.academy import list_courses, get_course, get_academy_cta
from mcp.tools.affiliate import get_affiliate_link, get_contextual_affiliates
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
    get_todays_appointments,
)
from mcp.tools.surgical_checklist import (
    get_surgery_checklist,
    detect_surgery_type,
    get_preop_documents,
    get_postop_warnings,
    get_followup_schedule,
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

app = Server("shapeshifters-healthcare")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # Drug Reference
        types.Tool(
            name="search_drug",
            description="Look up drug information by generic or brand name (educational only).",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Drug name"}},
                "required": ["name"],
            },
        ),
        types.Tool(
            name="get_drug_interactions",
            description="Check for known interactions between two drugs (educational only).",
            inputSchema={
                "type": "object",
                "properties": {
                    "drug1": {"type": "string"},
                    "drug2": {"type": "string"},
                },
                "required": ["drug1", "drug2"],
            },
        ),
        # Medical News
        types.Tool(
            name="get_medical_news",
            description="Get latest medical news, optionally filtered by specialty or audience.",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string", "description": "diabetes|oncology|surgery|dermatology|general"},
                    "audience": {"type": "string", "description": "doctor|patient"},
                    "limit": {"type": "integer", "description": "Number of articles (default 5)"},
                },
            },
        ),
        # Consult
        types.Tool(
            name="find_specialist",
            description="Find a specialist by specialty and optionally city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string"},
                    "city": {"type": "string", "description": "Bangalore|Mumbai|Hyderabad|Chennai|Delhi"},
                },
                "required": ["specialty"],
            },
        ),
        types.Tool(
            name="get_second_opinion_cta",
            description="Returns CTA for getting a second medical opinion.",
            inputSchema={
                "type": "object",
                "properties": {"condition": {"type": "string"}},
                "required": ["condition"],
            },
        ),
        types.Tool(
            name="list_cities",
            description="List the 5 cities Shapeshifters serves.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="list_specialties",
            description="List all available medical specialties.",
            inputSchema={"type": "object", "properties": {}},
        ),
        # Studios
        types.Tool(
            name="list_cme_modules",
            description="List CME video modules available on Shapeshifters Studios.",
            inputSchema={
                "type": "object",
                "properties": {"specialty": {"type": "string"}},
            },
        ),
        # Academy
        types.Tool(
            name="list_courses",
            description="List Academy courses, optionally filtered by specialty and audience.",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string"},
                    "audience": {"type": "string", "description": "doctor|student"},
                },
            },
        ),
        # Affiliate
        types.Tool(
            name="get_affiliate_link",
            description="Get the affiliate URL for a product type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_type": {"type": "string"},
                    "city": {"type": "string"},
                },
                "required": ["product_type"],
            },
        ),
        types.Tool(
            name="get_contextual_affiliates",
            description="Get 2-3 contextually relevant affiliate suggestions for a topic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "audience": {"type": "string", "description": "patient|doctor"},
                },
                "required": ["topic"],
            },
        ),
        # Educational
        types.Tool(
            name="explain_medical_term",
            description="Explain a medical term in simple language.",
            inputSchema={
                "type": "object",
                "properties": {"term": {"type": "string"}},
                "required": ["term"],
            },
        ),
        types.Tool(
            name="myth_or_fact",
            description="Evaluate a health myth or claim and return verdict.",
            inputSchema={
                "type": "object",
                "properties": {"statement": {"type": "string"}},
                "required": ["statement"],
            },
        ),
        types.Tool(
            name="get_daily_health_tip",
            description="Get today's rotating health tip, optionally filtered by specialty and audience.",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string"},
                    "audience": {"type": "string"},
                },
            },
        ),
        types.Tool(
            name="get_clinical_guideline",
            description="Get simplified clinical guideline for a specialty and topic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string"},
                    "topic": {"type": "string"},
                },
                "required": ["specialty", "topic"],
            },
        ),
        types.Tool(
            name="ask_health_question",
            description="Match a health question to a pre-built evidence-based answer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "audience": {"type": "string", "description": "patient|doctor"},
                },
                "required": ["question"],
            },
        ),
        # Insurance FAQs
        types.Tool(
            name="search_insurance_faq",
            description=(
                "Search insurance FAQs for all 11 empanelled insurers at Eesha Multispeciality Hospital. "
                "Query by company name (e.g. 'Niva Bupa'), topic (cashless, reimbursement, claim, documents), "
                "or a general insurance question."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Company name, topic, or question keyword"},
                    "company": {"type": "string", "description": "Optional: specific insurer name to filter results"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="list_insurers",
            description="List all 11 insurance companies empanelled at Eesha Multispeciality Hospital with helplines.",
            inputSchema={"type": "object", "properties": {}},
        ),
        # OPD Appointments
        types.Tool(
            name="get_departments",
            description="Get all OPD departments at Eesha Multispeciality Hospital.",
            inputSchema={
                "type": "object",
                "properties": {
                    "hospital_id": {"type": "string", "description": "Hospital ID (default: eesha)"},
                },
            },
        ),
        types.Tool(
            name="get_available_slots",
            description="Get available OPD appointment slots for a department and date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_code": {"type": "string", "description": "e.g. GM, SG, CD, OR"},
                    "date": {"type": "string", "description": "YYYY-MM-DD, 'today', or 'tomorrow'"},
                    "hospital_id": {"type": "string"},
                },
                "required": ["department_code", "date"],
            },
        ),
        types.Tool(
            name="book_opd_appointment",
            description="Book an OPD appointment at Eesha Multispeciality Hospital.",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_code": {"type": "string"},
                    "doctor_id":       {"type": "string"},
                    "patient_name":    {"type": "string"},
                    "patient_phone":   {"type": "string"},
                    "date":            {"type": "string"},
                    "time_slot":       {"type": "string", "description": "e.g. 9:00"},
                    "reason":          {"type": "string"},
                },
                "required": ["department_code", "doctor_id", "patient_name", "patient_phone", "date", "time_slot"],
            },
        ),
        types.Tool(
            name="cancel_appointment",
            description="Cancel an existing OPD appointment by reference ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reference_id":  {"type": "string"},
                    "patient_phone": {"type": "string"},
                },
                "required": ["reference_id", "patient_phone"],
            },
        ),
        types.Tool(
            name="get_appointment_details",
            description="Get full details of an existing appointment by reference ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reference_id": {"type": "string"},
                },
                "required": ["reference_id"],
            },
        ),
        # Surgical Checklists
        types.Tool(
            name="get_surgery_checklist",
            description="Get pre-op or post-op checklist for a surgery type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "surgery_type": {"type": "string", "description": "general_surgery|orthopaedic_surgery|laparoscopic_surgery|cardiac_surgery"},
                    "phase":        {"type": "string", "description": "pre_op|post_op|both"},
                },
                "required": ["surgery_type", "phase"],
            },
        ),
        types.Tool(
            name="get_preop_documents",
            description="Get list of documents required before a surgery.",
            inputSchema={
                "type": "object",
                "properties": {
                    "surgery_type": {"type": "string"},
                },
                "required": ["surgery_type"],
            },
        ),
        types.Tool(
            name="get_postop_warnings",
            description="Get warning signs to watch for after a surgery.",
            inputSchema={
                "type": "object",
                "properties": {
                    "surgery_type": {"type": "string"},
                },
                "required": ["surgery_type"],
            },
        ),
        # Live News
        types.Tool(
            name="get_live_news",
            description=(
                "Get latest live medical news from RSS feeds. "
                "Updated every 6 hours from Times of India Health, "
                "NDTV Health, WHO News, and MedicalXpress."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string", "description": "Filter by specialty (optional)"},
                    "impact": {"type": "string", "description": "High or Medium (optional)"},
                    "limit": {"type": "integer", "description": "Number of articles (optional)"},
                    "country": {"type": "string", "description": "India or International (optional)"},
                },
            },
        ),
        types.Tool(
            name="get_news_by_country",
            description=(
                "Get medical news filtered by country — "
                "India for local news, International for global."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "country": {"type": "string", "description": "India or International"},
                },
                "required": ["country"],
            },
        ),
        types.Tool(
            name="get_news_summary_live",
            description=(
                "Get summary of live news — counts by source, "
                "impact level, and top 3 headlines."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = None

    if name == "search_drug":
        result = search_drug(arguments["name"])
    elif name == "get_drug_interactions":
        result = get_drug_interactions(arguments["drug1"], arguments["drug2"])
    elif name == "get_medical_news":
        result = get_medical_news(
            specialty=arguments.get("specialty"),
            audience=arguments.get("audience"),
            limit=arguments.get("limit", 5),
        )
    elif name == "find_specialist":
        result = find_specialist(arguments["specialty"], arguments.get("city"))
    elif name == "get_second_opinion_cta":
        result = get_second_opinion_cta(arguments["condition"])
    elif name == "list_cities":
        result = list_cities()
    elif name == "list_specialties":
        result = list_specialties()
    elif name == "list_cme_modules":
        result = list_cme_modules(specialty=arguments.get("specialty"))
    elif name == "list_courses":
        result = list_courses(
            specialty=arguments.get("specialty"),
            audience=arguments.get("audience"),
        )
    elif name == "get_affiliate_link":
        result = get_affiliate_link(arguments["product_type"], arguments.get("city"))
    elif name == "get_contextual_affiliates":
        result = get_contextual_affiliates(
            topic=arguments["topic"],
            audience=arguments.get("audience", "patient"),
        )
    elif name == "explain_medical_term":
        result = explain_medical_term(arguments["term"])
    elif name == "myth_or_fact":
        result = myth_or_fact(arguments["statement"])
    elif name == "get_daily_health_tip":
        result = get_daily_health_tip(
            specialty=arguments.get("specialty"),
            audience=arguments.get("audience"),
        )
    elif name == "get_clinical_guideline":
        result = get_clinical_guideline(arguments["specialty"], arguments["topic"])
    elif name == "ask_health_question":
        result = ask_health_question(
            question=arguments["question"],
            audience=arguments.get("audience", "patient"),
        )
    elif name == "search_insurance_faq":
        result = search_insurance_faq(
            query=arguments["query"],
            company=arguments.get("company"),
        )
    elif name == "list_insurers":
        result = list_insurers()
    elif name == "get_departments":
        result = await get_departments(arguments)
    elif name == "get_available_slots":
        result = await get_available_slots(arguments)
    elif name == "book_opd_appointment":
        result = await book_opd_appointment(arguments)
    elif name == "cancel_appointment":
        result = await cancel_appointment(arguments)
    elif name == "get_appointment_details":
        result = await get_appointment_details(arguments)
    elif name == "get_surgery_checklist":
        result = await get_surgery_checklist(arguments)
    elif name == "get_preop_documents":
        result = await get_preop_documents(arguments)
    elif name == "get_postop_warnings":
        result = await get_postop_warnings(arguments)
    elif name == "get_live_news" and LIVE_NEWS_AVAILABLE:
        result = await get_live_news(arguments)
    elif name == "get_news_by_country" and LIVE_NEWS_AVAILABLE:
        result = await get_news_by_country(arguments)
    elif name == "get_news_summary_live" and LIVE_NEWS_AVAILABLE:
        result = await get_news_summary_live(arguments)
    else:
        result = {"error": f"Unknown tool: {name}"}

    return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
