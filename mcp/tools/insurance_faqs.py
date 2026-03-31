"""
Shapeshifters Healthcare — Insurance FAQ Tool
FAQs for all 11 empanelled insurance companies at Eesha Multispeciality Hospital.

Educational only — for personalised insurance queries always direct to the insurer helpline.
"""

from __future__ import annotations

DISCLAIMER = (
    "This information is for guidance only. Policy terms vary — always confirm "
    "with your insurer or TPA before admission. Eesha Multispeciality Hospital's "
    "insurance desk is available 24 × 7 for cashless pre-authorisation queries."
)

# ── Master FAQ database ──────────────────────────────────────────────────────

INSURANCE_DATA: dict[str, dict] = {
    "iffco_tokio": {
        "name": "IFFCO Tokio General Insurance",
        "short": "IFFCO Tokio",
        "aliases": ["iffco", "iffco tokio", "iffco-tokio"],
        "helpline": "1800-103-5499",
        "website": "https://www.iffcotokio.co.in",
        "tpa": "In-house (IFFCO Tokio Health)",
        "cashless_process": (
            "Present your IFFCO Tokio health card at the insurance desk on admission. "
            "The hospital sends a pre-authorisation request; typical approval takes 2–4 hours. "
            "Planned procedures: send request at least 3 days prior."
        ),
        "claim_process": (
            "For reimbursement: collect all original bills, discharge summary, prescriptions, "
            "and investigation reports. Submit within 30 days of discharge to nearest IFFCO Tokio branch "
            "or upload via their portal/app."
        ),
        "faqs": [
            {
                "q": "Does IFFCO Tokio cover pre-existing diseases?",
                "a": "Pre-existing diseases are covered after a waiting period of 2–4 years depending on the policy. Check your policy schedule for exact terms.",
            },
            {
                "q": "What is the room rent limit under IFFCO Tokio?",
                "a": "Room rent limits vary by plan — typically 1–2% of Sum Insured per day. Some plans offer no room rent sub-limits. Check your policy document.",
            },
            {
                "q": "How do I check my IFFCO Tokio claim status?",
                "a": "Log in to the IFFCO Tokio customer portal or call the 24×7 helpline 1800-103-5499.",
            },
            {
                "q": "Is day-care treatment covered?",
                "a": "Yes — IFFCO Tokio covers day-care procedures (dialysis, chemotherapy, cataract surgery, etc.) that do not require 24-hour hospitalisation.",
            },
            {
                "q": "What documents are needed for cashless at Eesha?",
                "a": "Health insurance card / e-card, valid photo ID, policy number. The hospital insurance desk will handle pre-auth on your behalf.",
            },
        ],
    },

    "heritage_health": {
        "name": "Heritage Health TPA",
        "short": "Heritage Health TPA",
        "aliases": ["heritage", "heritage health", "heritage tpa"],
        "helpline": "1800-102-4321",
        "website": "https://www.heritagehealthtpa.com",
        "tpa": "Heritage Health TPA (Third Party Administrator)",
        "cashless_process": (
            "Heritage Health TPA processes cashless requests on behalf of several PSU and private insurers. "
            "Present your TPA card at the hospital desk. Pre-auth is typically processed within 2–6 hours for planned cases."
        ),
        "claim_process": (
            "Claims are submitted to Heritage Health TPA directly. Collect all original documents at discharge "
            "and submit within 15–30 days (as per your base insurer's policy). "
            "Online submission available via the Heritage Health portal."
        ),
        "faqs": [
            {
                "q": "Which insurers use Heritage Health TPA?",
                "a": "Heritage Health TPA processes claims for multiple PSU insurers including Oriental, National, and others. Your insurance card will state 'Heritage Health TPA' if applicable.",
            },
            {
                "q": "How do I get a Heritage Health TPA card?",
                "a": "After purchasing a policy administered by Heritage, they send a physical and e-card. Download the e-card from their member portal using your policy number.",
            },
            {
                "q": "What is the Heritage Health TPA helpline?",
                "a": "Call 1800-102-4321 (toll-free, 24×7) for pre-auth, claim status, and general queries.",
            },
            {
                "q": "How long does Heritage Health TPA take to settle claims?",
                "a": "Cashless discharge authorisation: within 2–4 hours of final bill submission. Reimbursement claims: 15–30 working days from receipt of complete documents.",
            },
            {
                "q": "Can I submit claim documents online?",
                "a": "Yes — upload scanned copies via the Heritage Health TPA member portal. Originals may be required for large claims.",
            },
        ],
    },

    "aditya_birla": {
        "name": "Aditya Birla Health Insurance",
        "short": "Aditya Birla",
        "aliases": ["aditya birla", "abhi", "aditya birla health", "activ"],
        "helpline": "1800-270-7000",
        "website": "https://www.adityabirlacapital.com/health-insurance",
        "tpa": "In-house",
        "cashless_process": (
            "Present your Activ Health e-card and photo ID at the insurance desk. "
            "Aditya Birla processes pre-auth in-house; planned admissions should be intimated 48 hours prior. "
            "Emergency cashless requests are processed within 4 hours."
        ),
        "claim_process": (
            "Reimbursement: file within 30 days of discharge. Upload documents via the Activ Health app "
            "or submit to the nearest Aditya Birla Health Insurance branch."
        ),
        "faqs": [
            {
                "q": "What is the Activ Health plan's HealthReturns feature?",
                "a": "HealthReturns rewards you with premium discounts of up to 30% if you meet daily health goals tracked via the Activ app (steps, health assessments).",
            },
            {
                "q": "Does Aditya Birla cover mental health treatment?",
                "a": "Yes — Activ plans cover psychiatric inpatient treatment as mandated by IRDAI regulations.",
            },
            {
                "q": "What is the waiting period for pre-existing diseases under Aditya Birla?",
                "a": "Standard waiting period is 3 years for most pre-existing conditions. Some plans offer a reduced 1-year waiting period.",
            },
            {
                "q": "Is there a no-claim bonus with Aditya Birla Health Insurance?",
                "a": "Yes — No Claim Bonus increases your Sum Insured by 10–50% for each claim-free year, subject to policy terms.",
            },
            {
                "q": "How do I add a family member to my Aditya Birla policy?",
                "a": "Log in to the Activ Health app or customer portal, or call 1800-270-7000 during policy renewal to add dependants.",
            },
        ],
    },

    "manipal_cigna": {
        "name": "ManipalCigna Health Insurance",
        "short": "ManipalCigna",
        "aliases": ["manipal cigna", "manipalcigna", "cigna", "manipal"],
        "helpline": "1800-102-4462",
        "website": "https://www.manipalcigna.com",
        "tpa": "In-house",
        "cashless_process": (
            "ManipalCigna cashless is processed in-house. Intimate planned hospitalisation 3 days in advance. "
            "For emergency, call 1800-102-4462 immediately after admission. "
            "Pre-auth TAT: 2–4 hours emergency, same day planned."
        ),
        "claim_process": (
            "File reimbursement claims within 30 days of discharge. "
            "Submit via the ManipalCigna website, app, or email to claims@manipalcigna.com."
        ),
        "faqs": [
            {
                "q": "What plans does ManipalCigna offer?",
                "a": "Key plans include ProHealth (individual/family), Prime (senior citizens), and Lifestyle Protection (critical illness). Each has different Sum Insured options and benefits.",
            },
            {
                "q": "Does ManipalCigna cover maternity expenses?",
                "a": "Yes — ProHealth plans include maternity cover after a 2-year waiting period. Covers normal delivery, C-section, and newborn care up to specified limits.",
            },
            {
                "q": "What is the ManipalCigna network hospital count?",
                "a": "ManipalCigna has a network of 6,500+ hospitals across India for cashless treatment.",
            },
            {
                "q": "How do I check if Eesha Hospital is on ManipalCigna's network?",
                "a": "Call 1800-102-4462 or check the hospital finder on manipalcigna.com. Eesha Multispeciality Hospital's insurance desk can also confirm your coverage.",
            },
            {
                "q": "Is OPD treatment covered under ManipalCigna?",
                "a": "Select plans include OPD cover (consultations, pharmacy). Check your specific plan's schedule of benefits.",
            },
        ],
    },

    "niva_bupa": {
        "name": "Niva Bupa Health Insurance",
        "short": "Niva Bupa",
        "aliases": ["niva bupa", "nivabupa", "max bupa", "bupa"],
        "helpline": "1800-200-8888",
        "website": "https://www.nivabupa.com",
        "tpa": "In-house",
        "cashless_process": (
            "Niva Bupa processes all cashless requests in-house with no TPA. "
            "Present e-card at the hospital insurance desk. "
            "Pre-auth TAT is typically 30 minutes to 2 hours for planned cases. "
            "Emergency cases are approved immediately."
        ),
        "claim_process": (
            "Reimbursement: file within 20 days of discharge via the Niva Bupa app, website, or helpline. "
            "Upload clear photos of all documents. Track claim status in real time via the app."
        ),
        "faqs": [
            {
                "q": "What is the Niva Bupa ReAssure plan?",
                "a": "ReAssure is a comprehensive family floater plan with features like Restore Benefit (Sum Insured refill after a claim), no room rent sub-limits, and lifelong renewability.",
            },
            {
                "q": "Does Niva Bupa offer a health account / wellness program?",
                "a": "Yes — the Health Plus app tracks health activities and offers wellness rewards. Some plans include complimentary health check-ups.",
            },
            {
                "q": "What is the waiting period for pre-existing diseases with Niva Bupa?",
                "a": "Standard 3-year waiting period for pre-existing diseases. Certain plans allow portability benefits reducing this period.",
            },
            {
                "q": "Can I port my existing policy to Niva Bupa?",
                "a": "Yes — IRDAI allows portability. Apply at least 45 days before your current policy renewal. Niva Bupa accepts portability requests.",
            },
            {
                "q": "How do I download my Niva Bupa e-card?",
                "a": "Log in to the Niva Bupa app or website with your policy number and date of birth to download the digital health card instantly.",
            },
        ],
    },

    "go_digit": {
        "name": "Go Digit General Insurance",
        "short": "Go Digit",
        "aliases": ["go digit", "godigit", "digit", "digit insurance"],
        "helpline": "1800-258-5956",
        "website": "https://www.godigit.com",
        "tpa": "In-house",
        "cashless_process": (
            "Go Digit uses a fully digital, in-house cashless process. "
            "At Eesha Hospital, show your Digit e-card (available on the Digit app). "
            "Pre-auth requests are submitted digitally; typical approval in 2–4 hours."
        ),
        "claim_process": (
            "Everything is handled via the Digit app or website. Upload documents, track status, "
            "and receive settlement digitally. No physical forms required. "
            "File within 30 days of discharge."
        ),
        "faqs": [
            {
                "q": "What makes Go Digit health insurance different?",
                "a": "Digit is 100% digital — from purchase to claims. Simple policy documents, quick claim approvals, and an intuitive app are core differentiators.",
            },
            {
                "q": "Does Go Digit cover AYUSH treatment?",
                "a": "Yes — Digit health plans cover Ayurveda, Yoga, Unani, Siddha, and Homeopathy (AYUSH) inpatient treatment.",
            },
            {
                "q": "What is the room rent limit under Go Digit?",
                "a": "Most Digit plans offer single private AC room without sub-limits. Verify your specific plan benefits in the policy schedule.",
            },
            {
                "q": "How quickly does Digit settle claims?",
                "a": "Digit targets cashless discharge approval within 2 hours and reimbursement settlement within 7–10 working days for complete documents.",
            },
            {
                "q": "Can senior citizens get Go Digit health insurance?",
                "a": "Yes — Digit covers individuals up to 65 years at entry (some plans up to 70). Lifelong renewability is available.",
            },
        ],
    },

    "cholamandalam": {
        "name": "Cholamandalam MS General Insurance",
        "short": "Chola MS",
        "aliases": ["cholamandalam", "chola", "chola ms", "cholamandalam ms"],
        "helpline": "1800-200-5544",
        "website": "https://www.cholainsurance.com",
        "tpa": "Third-party TPAs and in-house for select products",
        "cashless_process": (
            "Present Chola MS health card and photo ID at the hospital insurance desk. "
            "Pre-auth is submitted to Chola MS or their designated TPA. "
            "Planned admissions: intimate 3 days prior. Emergency: within 24 hours of admission."
        ),
        "claim_process": (
            "File reimbursement within 30 days of discharge. Submit all original documents to nearest "
            "Chola MS branch or the designated TPA office. Online claim submission available."
        ),
        "faqs": [
            {
                "q": "What health insurance plans does Cholamandalam offer?",
                "a": "Key plans include Chola Healthline (individual/family), Chola Accident & Health, and corporate group plans. Covers hospitalisation, critical illness, and personal accident.",
            },
            {
                "q": "Does Chola MS cover critical illness?",
                "a": "Yes — dedicated critical illness plans cover 10+ conditions including cancer, heart attack, stroke, and kidney failure with a lump-sum benefit.",
            },
            {
                "q": "What is the network hospital strength of Chola MS?",
                "a": "Cholamandalam MS has a network of 8,000+ hospitals across India.",
            },
            {
                "q": "Does Chola MS have a no-claim bonus?",
                "a": "Yes — NCB typically adds 10% to Sum Insured per claim-free year, up to a maximum of 50%.",
            },
            {
                "q": "Who is the TPA for Cholamandalam MS policies?",
                "a": "Chola MS uses multiple TPAs depending on your policy. Your health card will specify the TPA. Common TPAs include Medi Assist and Paramount. Some plans are in-house.",
            },
        ],
    },

    "liberty_general": {
        "name": "Liberty General Insurance",
        "short": "Liberty General",
        "aliases": ["liberty", "liberty general", "liberty insurance"],
        "helpline": "1800-266-5844",
        "website": "https://www.libertyinsurance.in",
        "tpa": "Medi Assist India TPA / In-house for select plans",
        "cashless_process": (
            "Liberty General processes cashless through Medi Assist TPA for most plans. "
            "Show your Liberty / Medi Assist TPA card at the insurance desk. "
            "Pre-auth TAT: 2–4 hours for planned cases."
        ),
        "claim_process": (
            "Submit reimbursement claims to Medi Assist TPA or Liberty General directly within 30 days. "
            "Track status via the Liberty Insurance app or Medi Assist portal."
        ),
        "faqs": [
            {
                "q": "What are the main Liberty General health plans?",
                "a": "Health Connect Supra (super top-up), Health Connect Plus (comprehensive), and group health plans for corporates.",
            },
            {
                "q": "What is a super top-up and does Liberty offer one?",
                "a": "A super top-up covers hospitalisation costs beyond a deductible, complementing a basic policy. Liberty's Health Connect Supra is a super top-up plan.",
            },
            {
                "q": "Does Liberty General cover domiciliary treatment?",
                "a": "Yes — domiciliary hospitalisation (home treatment recommended by a doctor when hospital admission isn't possible) is covered under select plans.",
            },
            {
                "q": "What is the Liberty General claim helpline?",
                "a": "Call 1800-266-5844 (toll-free) or Medi Assist TPA at 1800-425-9449 for cashless pre-auth and claim queries.",
            },
            {
                "q": "Is organ donor treatment covered by Liberty General?",
                "a": "Yes — organ donor's hospitalisation expenses related to harvesting are covered under most Liberty health plans.",
            },
        ],
    },

    "tata_aig": {
        "name": "Tata AIG General Insurance",
        "short": "Tata AIG",
        "aliases": ["tata aig", "tataaig", "tata", "aig"],
        "helpline": "1800-266-7780",
        "website": "https://www.tataaig.com",
        "tpa": "In-house (Tata AIG Health)",
        "cashless_process": (
            "Tata AIG processes cashless in-house. Present your MediCare / MediSenior e-card "
            "and photo ID. For planned admission: intimate 48 hours prior via the Tata AIG app or helpline. "
            "Emergency cashless: call 1800-266-7780 immediately after admission."
        ),
        "claim_process": (
            "File reimbursement within 30 days via the Tata AIG app, website, or by visiting a branch. "
            "Upload scanned documents; track claim in real time."
        ),
        "faqs": [
            {
                "q": "What is the Tata AIG MediCare plan?",
                "a": "MediCare is Tata AIG's flagship individual and family floater health plan covering inpatient, day-care, AYUSH, maternity, and OPD (select variants).",
            },
            {
                "q": "Does Tata AIG cover international medical emergencies?",
                "a": "Some Tata AIG travel insurance plans cover emergency medical treatment abroad. Standard health plans cover treatment within India only.",
            },
            {
                "q": "What is the waiting period under Tata AIG health plans?",
                "a": "30-day initial waiting period (except accidents). 2 years for specific diseases. 3–4 years for pre-existing conditions depending on the plan.",
            },
            {
                "q": "Does Tata AIG have a wellness program?",
                "a": "Yes — Tata AIG's Wellness program offers discounts on gym memberships, pharmacy purchases, and health check-ups for policyholders.",
            },
            {
                "q": "How many network hospitals does Tata AIG have?",
                "a": "Tata AIG has a network of 7,000+ hospitals across India for cashless treatment.",
            },
        ],
    },

    "future_generali": {
        "name": "Future Generali India Insurance",
        "short": "Future Generali",
        "aliases": ["future generali", "future", "generali", "future generali india"],
        "helpline": "1800-220-233",
        "website": "https://www.futuregenerali.in",
        "tpa": "In-house / Partnered TPAs",
        "cashless_process": (
            "Future Generali processes cashless in-house for most products. "
            "Present your policy e-card and ID. Planned admission: intimate 48 hours prior. "
            "Emergency: call 1800-220-233 immediately. Approval TAT: 2–6 hours."
        ),
        "claim_process": (
            "File within 30 days of discharge. Submit documents to Future Generali branch or "
            "upload via their app/website. Customer care: 1800-220-233."
        ),
        "faqs": [
            {
                "q": "What are the key Future Generali health plans?",
                "a": "Plans include Health Total (comprehensive), Criticare (critical illness), Personal Accident, and group health plans for corporates.",
            },
            {
                "q": "Does Future Generali cover COVID-19 treatment?",
                "a": "Yes — as mandated by IRDAI, standard health plans cover COVID-19 hospitalisation when the insured tests positive and requires inpatient treatment.",
            },
            {
                "q": "What is the Future Generali renewal age limit?",
                "a": "Lifelong renewability is available under IRDAI guidelines. Entry age limits vary by product.",
            },
            {
                "q": "How do I port my policy to Future Generali?",
                "a": "Submit a portability request at least 45 days before your current policy expiry. Call 1800-220-233 or visit the website to initiate.",
            },
            {
                "q": "Does Future Generali cover bariatric surgery?",
                "a": "Bariatric surgery may be covered if the patient meets specified BMI and comorbidity criteria. Check with Future Generali or Eesha's insurance desk before scheduling.",
            },
        ],
    },

    "sbi_general": {
        "name": "SBI General Insurance",
        "short": "SBI General",
        "aliases": ["sbi general", "sbi", "sbi insurance", "state bank insurance"],
        "helpline": "1800-22-1111",
        "website": "https://www.sbigeneral.in",
        "tpa": "Medi Assist India TPA (primary)",
        "cashless_process": (
            "SBI General uses Medi Assist India TPA for cashless processing. "
            "Present your Medi Assist TPA card and photo ID at the hospital desk. "
            "Planned admissions: intimate 3 days prior via Medi Assist portal or 1800-425-9449. "
            "Emergency: call within 24 hours of admission."
        ),
        "claim_process": (
            "Submit reimbursement claims to Medi Assist TPA within 30 days of discharge. "
            "Online submission via Medi Assist portal (mediassist.in) or the SBI General app."
        ),
        "faqs": [
            {
                "q": "What are the main SBI General health insurance plans?",
                "a": "Key plans include Arogya Premier (high-value), Arogya Plus (OPD + inpatient), Critical Illness Insurance, and Hospital Daily Cash.",
            },
            {
                "q": "Does SBI General cover OPD expenses?",
                "a": "Yes — SBI Arogya Plus covers OPD consultations, pharmacy, and diagnostic tests up to specified limits.",
            },
            {
                "q": "What is the SBI General TPA helpline?",
                "a": "Medi Assist TPA (for SBI General): 1800-425-9449. SBI General direct: 1800-22-1111.",
            },
            {
                "q": "How do I get a cashless pre-auth for SBI General at Eesha Hospital?",
                "a": "The Eesha Hospital insurance desk will submit a pre-auth request to Medi Assist TPA on your behalf. Carry your Medi Assist TPA card and SBI policy document.",
            },
            {
                "q": "What is the waiting period for pre-existing diseases under SBI General?",
                "a": "Standard 4-year waiting period for pre-existing conditions under SBI General health plans. Some conditions have a 2-year waiting period.",
            },
        ],
    },
}

# ── General cashless process FAQs ────────────────────────────────────────────

GENERAL_FAQS: list[dict] = [
    {
        "topic": "cashless",
        "q": "What is cashless hospitalisation?",
        "a": (
            "Cashless hospitalisation means the hospital bills the insurance company directly, "
            "so you don't have to pay out-of-pocket (except for non-covered items). "
            "A pre-authorisation (pre-auth) request is sent to your insurer or TPA before or shortly after admission."
        ),
    },
    {
        "topic": "cashless",
        "q": "What documents do I need for cashless admission at Eesha Hospital?",
        "a": (
            "1. Insurance health card / e-card (physical or digital)\n"
            "2. Valid government-issued photo ID (Aadhaar, PAN, Passport)\n"
            "3. Doctor's referral letter (for planned admissions)\n"
            "4. Previous medical records (if available)\n\n"
            "Our insurance desk will guide you through the rest of the paperwork."
        ),
    },
    {
        "topic": "cashless",
        "q": "How long does cashless pre-authorisation take?",
        "a": (
            "Planned admissions: 2–6 hours (request should be sent 2–3 days prior).\n"
            "Emergency admissions: within 4 hours; treatment begins immediately."
        ),
    },
    {
        "topic": "reimbursement",
        "q": "What is the reimbursement claim process?",
        "a": (
            "1. Pay the hospital bill at discharge.\n"
            "2. Collect all original documents: bills, discharge summary, prescriptions, lab reports.\n"
            "3. Fill the insurer's/TPA's claim form.\n"
            "4. Submit within 30 days (some insurers allow up to 60 days — check your policy).\n"
            "5. Track claim status via the insurer's app or portal."
        ),
    },
    {
        "topic": "reimbursement",
        "q": "What documents are required for reimbursement?",
        "a": (
            "• Completed claim form (from insurer/TPA)\n"
            "• Original hospital bills and receipts\n"
            "• Discharge summary / case summary\n"
            "• Investigation reports (blood tests, scans, etc.)\n"
            "• Prescription copies\n"
            "• Doctor's certificate / treating doctor's note\n"
            "• NEFT / bank details for claim credit\n"
            "• Policy document / health card copy\n"
            "• Photo ID proof"
        ),
    },
    {
        "topic": "general",
        "q": "What is not covered under most health insurance plans?",
        "a": (
            "Common exclusions include:\n"
            "• Cosmetic or aesthetic treatments\n"
            "• Self-inflicted injuries\n"
            "• War or hazardous activity injuries\n"
            "• Dental treatment (unless due to accident)\n"
            "• Vision correction (spectacles, lenses)\n"
            "• Infertility / IVF\n"
            "• Pre-existing conditions during waiting period\n\n"
            "Always read your policy's exclusion list."
        ),
    },
    {
        "topic": "general",
        "q": "What is a TPA (Third Party Administrator)?",
        "a": (
            "A TPA is a licensed intermediary that processes health insurance claims on behalf of the insurer. "
            "They handle cashless pre-authorisation, claim settlement, and hospital coordination. "
            "Common TPAs include Medi Assist, Paramount, and Heritage Health."
        ),
    },
    {
        "topic": "general",
        "q": "What is the difference between floater and individual health insurance?",
        "a": (
            "Individual policy: separate Sum Insured for each family member.\n"
            "Family floater: a single shared Sum Insured for the entire family. "
            "Floaters are cost-effective for younger families; individual plans are better when multiple family members have regular claims."
        ),
    },
]


# ── Search function ──────────────────────────────────────────────────────────

def search_insurance_faq(query: str, company: str | None = None) -> dict:
    """
    Search the insurance FAQ database.

    Args:
        query: Search term — company name, topic (cashless, reimbursement, claim, documents),
               or a question keyword.
        company: Optional — specify a company name to narrow results.

    Returns:
        dict with keys: found, company_info (if company matched), faqs, general_faqs, disclaimer
    """
    query_lower = query.lower().strip()
    company_lower = company.lower().strip() if company else None

    matched_company: dict | None = None

    # Try to identify the company from `company` param or from the query itself
    search_in = company_lower or query_lower
    for key, data in INSURANCE_DATA.items():
        if any(alias in search_in for alias in data["aliases"]):
            matched_company = data
            break

    # Gather company-specific FAQs
    company_faqs: list[dict] = []
    if matched_company:
        for faq in matched_company["faqs"]:
            if (
                not query_lower
                or query_lower in faq["q"].lower()
                or query_lower in faq["a"].lower()
                or query_lower in matched_company["name"].lower()
            ):
                company_faqs.append(faq)

    # Gather general FAQs matching the query
    gen_faqs: list[dict] = []
    topic_keywords = {
        "cashless": ["cashless", "pre-auth", "pre auth", "preauth", "admission", "network"],
        "reimbursement": ["reimburse", "claim", "document", "bill", "receipt"],
        "general": ["tpa", "floater", "individual", "exclusion", "not covered", "waiting period"],
    }
    for faq in GENERAL_FAQS:
        q_lower = faq["q"].lower()
        a_lower = faq["a"].lower()
        if (
            query_lower in q_lower
            or query_lower in a_lower
            or faq["topic"] == query_lower
        ):
            gen_faqs.append(faq)
        else:
            for topic, kws in topic_keywords.items():
                if any(kw in query_lower for kw in kws) and faq["topic"] == topic:
                    if faq not in gen_faqs:
                        gen_faqs.append(faq)

    # Build company info summary
    company_info: dict | None = None
    if matched_company:
        company_info = {
            "name": matched_company["name"],
            "helpline": matched_company["helpline"],
            "website": matched_company["website"],
            "tpa": matched_company["tpa"],
            "cashless_process": matched_company["cashless_process"],
            "claim_process": matched_company["claim_process"],
        }

    found = bool(matched_company or company_faqs or gen_faqs)

    return {
        "found": found,
        "query": query,
        "company_info": company_info,
        "company_faqs": company_faqs[:5],
        "general_faqs": gen_faqs[:3],
        "all_companies": [d["short"] for d in INSURANCE_DATA.values()],
        "disclaimer": DISCLAIMER,
    }


def list_insurers() -> dict:
    """Return all empanelled insurance companies with key contact info."""
    return {
        "hospital": "Eesha Multispeciality Hospital",
        "total": len(INSURANCE_DATA),
        "insurers": [
            {
                "name": d["name"],
                "short": d["short"],
                "helpline": d["helpline"],
                "tpa": d["tpa"],
            }
            for d in INSURANCE_DATA.values()
        ],
        "note": (
            "For cashless pre-authorisation, visit Eesha Hospital's insurance desk "
            "(Ground Floor, near main reception) — open 24 × 7."
        ),
    }
