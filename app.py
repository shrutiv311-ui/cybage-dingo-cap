import streamlit as st
import re
from collections import defaultdict

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cybage Digital Diagnostic",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0A0D14 !important;
    color: #E8EAF0 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1280px;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Typography ── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif; letter-spacing: -0.02em; }

/* ── Hero Banner ── */
.hero-wrap {
    background: linear-gradient(135deg, #0F1624 0%, #131D35 50%, #0A1628 100%);
    border: 1px solid rgba(99, 179, 237, 0.15);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: #63B3ED;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem; font-weight: 800; line-height: 1.1;
    color: #F0F4FF; margin-bottom: 0.75rem;
}
.hero-title span { color: #63B3ED; }
.hero-sub {
    font-size: 1rem; color: #8899BB; max-width: 580px; line-height: 1.6;
}

/* ── Step Header ── */
.step-header {
    display: flex; align-items: center; gap: 1rem;
    margin: 2rem 0 1.25rem;
}
.step-pill {
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.25);
    color: #63B3ED; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0.35rem 0.85rem; border-radius: 999px;
    white-space: nowrap;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem; font-weight: 700; color: #E8EAF0;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
}

/* ── Pain Point Tags ── */
.pain-grid {
    display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.5rem;
}
.pain-tag {
    background: rgba(99,179,237,0.07);
    border: 1px solid rgba(99,179,237,0.2);
    color: #A8C8EF;
    padding: 0.45rem 1rem;
    border-radius: 8px;
    font-size: 0.84rem; font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-block;
}
.pain-tag:hover, .pain-tag.active {
    background: rgba(99,179,237,0.18);
    border-color: #63B3ED;
    color: #E8F4FF;
}

/* ── Service Result Card ── */
.service-card {
    background: linear-gradient(135deg, rgba(15,22,36,0.95) 0%, rgba(10,16,28,0.95) 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.service-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #63B3ED, #3182CE);
}
.service-card-rank {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #63B3ED; margin-bottom: 0.4rem;
}
.service-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem; font-weight: 700; color: #E8EAF0;
    margin-bottom: 0.5rem;
}
.service-score-bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 999px; height: 5px; width: 180px;
    margin-bottom: 1rem;
}
.service-score-bar {
    background: linear-gradient(90deg, #63B3ED, #3182CE);
    border-radius: 999px; height: 5px;
}
.service-explanation {
    font-size: 0.9rem; color: #8899BB; line-height: 1.65;
    margin-bottom: 1rem;
}
.micro-chip {
    display: inline-block;
    background: rgba(99,179,237,0.09);
    border: 1px solid rgba(99,179,237,0.18);
    color: #A8C8EF;
    font-size: 0.78rem; font-weight: 500;
    padding: 0.3rem 0.8rem; border-radius: 6px;
    margin: 0.2rem;
}

/* ── Insight Banner ── */
.insight-banner {
    background: linear-gradient(135deg, rgba(49,130,206,0.12) 0%, rgba(99,179,237,0.06) 100%);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
}
.insight-banner strong { color: #63B3ED; }

/* ── Collateral Card ── */
.collateral-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.25rem;
    height: 100%;
    transition: border-color 0.2s;
}
.collateral-card:hover { border-color: rgba(99,179,237,0.3); }
.collateral-type-badge {
    display: inline-block;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 0.25rem 0.65rem;
    border-radius: 5px; margin-bottom: 0.6rem;
}
.badge-case-study { background: rgba(72,187,120,0.15); color: #48BB78; border: 1px solid rgba(72,187,120,0.3); }
.badge-brochure   { background: rgba(237,137,54,0.15);  color: #ED8936; border: 1px solid rgba(237,137,54,0.3); }
.badge-deck       { background: rgba(159,122,234,0.15); color: #9F7AEA; border: 1px solid rgba(159,122,234,0.3); }
.collateral-title { font-weight: 600; font-size: 0.95rem; color: #E0E4EE; margin-bottom: 0.3rem; }
.collateral-desc  { font-size: 0.82rem; color: #7788AA; line-height: 1.5; margin-bottom: 0.9rem; }

/* ── Streamlit Widget Overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(168,200,239,0.6) !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
}

[data-testid="stMultiSelect"] {
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Tab styling */
[data-testid="stTabs"] [role="tab"] {
    color: #7788AA !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #63B3ED !important;
    border-bottom-color: #63B3ED !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
details summary { color: #A8C8EF !important; font-weight: 500 !important; }

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; }

label, [data-testid="stMarkdownContainer"] p { color: #8899BB !important; }
.stSelectbox label { color: #8899BB !important; }

/* Download button */
.dl-btn {
    display: inline-block;
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63B3ED !important;
    font-size: 0.8rem; font-weight: 600;
    padding: 0.4rem 0.9rem; border-radius: 7px;
    text-decoration: none;
    margin-right: 0.4rem;
    transition: background 0.15s;
}
.dl-btn:hover { background: rgba(99,179,237,0.18); }
.preview-btn {
    display: inline-block;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.1);
    color: #7788AA !important;
    font-size: 0.8rem; font-weight: 500;
    padding: 0.4rem 0.9rem; border-radius: 7px;
    text-decoration: none;
    transition: border-color 0.15s;
}
.preview-btn:hover { border-color: rgba(255,255,255,0.25); color: #A8C8EF !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GLOBALS (available everywhere)
# ─────────────────────────────────────────────

INDUSTRIES = [
    "Select Industry…", "E-Commerce / Retail", "B2B SaaS / Technology",
    "BFSI (Banking & Financial Services)", "Healthcare & Pharma",
    "FMCG / Consumer Goods", "Media & Entertainment", "Education / EdTech",
    "Automotive", "Real Estate", "Manufacturing", "Other",
]

# ─────────────────────────────────────────────
# DATA LAYER  (fully self-contained, no Supabase needed to run)
# ─────────────────────────────────────────────

DIAGNOSTIC_MAPPING = {
    "Analytics & Business Intelligence": {
        "keywords": [
            "track", "ga4", "tagging", "gtm", "server-side", "cookie", "attribution",
            "journey", "dashboard", "looker", "power bi", "data silos", "reporting",
            "metrics", "conversion rate", "cro", "drop-off", "analytics", "visibility",
            "pixel", "data", "measure", "insight", "report", "funnel visibility",
        ],
        "micro_services": [
            "Server-Side Tagging & Privacy-First Tracking Setups",
            "GA4 Architecture Audits & Advanced Event Implementation",
            "Automated Looker Studio & Power BI Dashboard Engineering",
            "Multi-Touch Attribution Modeling & Funnel Leakage Analysis",
            "Conversion Rate Optimization (CRO) & User Behavior Mapping",
        ],
        "diagnostic_explanation": (
            "Your inputs indicate gaps in visibility, tracking compliance, or data fragmentation. "
            "We resolve this by auditing your tracking setup, deploying robust server-side analytics, "
            "and building unified dashboards to illuminate the exact customer journey."
        ),
        "icon": "📊",
    },
    "Media Mix Modeling (MMM)": {
        "keywords": [
            "mmm", "budget allocation", "incrementality", "diminishing returns", "spend optimization",
            "forecasting", "marketing mix", "offline impact", "external factors", "channel performance",
            "macro economic", "cookieless measurement", "long-term value", "budget", "spend",
            "channel", "media", "allocation", "mix",
        ],
        "micro_services": [
            "Privacy-Safe Statistical Media Mix Modeling",
            "Cross-Channel Budget Optimization & Forecasting",
            "Incrementality Testing & Lift Analysis",
            "External Factor (Seasonality/Economic) Impact Analysis",
        ],
        "diagnostic_explanation": (
            "You are facing challenges with macro-level budget efficiency and privacy-safe measurement. "
            "Our MMM frameworks analyze historical spend patterns to isolate the true incremental impact "
            "of every dollar, without relying on user-level cookies."
        ),
        "icon": "📈",
    },
    "Paid Advertising Support": {
        "keywords": [
            "cac", "cpa", "roi", "roas", "expensive ads", "google ads", "meta ads",
            "linkedin ads", "ad spend", "paid media", "bidding", "targeting", "lead cost",
            "performance marketing", "search ads", "programmatic", "ads", "advertising",
            "paid", "cost per", "acquisition cost", "return on ad",
        ],
        "micro_services": [
            "Paid Search & Social Campaign Restructuring",
            "Audience Segmentation & First-Party Data Targeting",
            "Smart Bidding Optimization & Ad Fraud Mitigation",
            "Creative Testing Frameworks & Copywriting Support",
        ],
        "diagnostic_explanation": (
            "Your primary bottleneck is performance marketing efficiency and rising acquisition costs. "
            "We deploy advanced bidding tactics, tighten audience targeting using first-party data, "
            "and eliminate wasted ad spend across digital networks."
        ),
        "icon": "🎯",
    },
    "Go-To-Market (GTM) Strategies": {
        "keywords": [
            "launch", "scale", "positioning", "audience", "market entry", "penetration",
            "competitor", "product launch", "value proposition", "icp", "ideal customer",
            "commercialization", "expansion", "new market", "growth", "strategy",
            "go-to-market", "gtm", "brand", "persona",
        ],
        "micro_services": [
            "Ideal Customer Profile (ICP) & Persona Development",
            "Competitive Landscape Mapping & Benchmarking",
            "Multi-Channel Launch Orchestration Playbooks",
            "Value Proposition & Messaging Framework Design",
        ],
        "diagnostic_explanation": (
            "You are focusing on a new market, product launch, or audience expansion. We build "
            "robust, data-backed market-entry blueprints that define exactly who your buyer is, "
            "where to find them, and how to out-position the competition."
        ),
        "icon": "🚀",
    },
    "Inbound & Content Marketing": {
        "keywords": [
            "seo", "organic", "traffic", "content", "blog", "leads", "unqualified",
            "nurturing", "email marketing", "hubspot", "automation", "whitepapers", "funnel",
            "inbound", "content strategy", "lead generation", "qualify", "top of funnel",
            "awareness", "engagement",
        ],
        "micro_services": [
            "Technical SEO & Content Velocity Audits",
            "B2B Lead Nurturing & Marketing Automation Workflows",
            "High-Intent Content Mapping & Asset Creation",
            "Inbound Funnel Mapping & Lead Scoring Setups",
        ],
        "diagnostic_explanation": (
            "Your inputs point to issues with low organic visibility or poor lead quality. "
            "We restructure your inbound funnel, implement precise lead scoring to weed out "
            "unqualified sign-ups, and optimize content for high-intent organic traffic."
        ),
        "icon": "✍️",
    },
}

SYNONYM_MAP = {
    # Paid Advertising
    "cac": ["Paid Advertising Support", "Media Mix Modeling (MMM)"],
    "cpa": ["Paid Advertising Support", "Media Mix Modeling (MMM)"],
    "roas": ["Paid Advertising Support", "Media Mix Modeling (MMM)"],
    "roi":  ["Paid Advertising Support", "Media Mix Modeling (MMM)"],
    "expensive ads": ["Paid Advertising Support"],
    "ad spend": ["Paid Advertising Support"],
    "google ads": ["Paid Advertising Support"],
    "meta ads": ["Paid Advertising Support"],
    "linkedin ads": ["Paid Advertising Support"],
    # Analytics
    "ga4": ["Analytics & Business Intelligence"],
    "funnel": ["Analytics & Business Intelligence", "Inbound & Content Marketing"],
    "tracking": ["Analytics & Business Intelligence"],
    "attribution": ["Analytics & Business Intelligence", "Media Mix Modeling (MMM)"],
    "cookie": ["Analytics & Business Intelligence", "Media Mix Modeling (MMM)"],
    "journey": ["Analytics & Business Intelligence"],
    "data silo": ["Analytics & Business Intelligence"],
    "dashboard": ["Analytics & Business Intelligence"],
    "drop off": ["Analytics & Business Intelligence"],
    # GTM
    "launch": ["Go-To-Market (GTM) Strategies"],
    "scale": ["Go-To-Market (GTM) Strategies"],
    "positioning": ["Go-To-Market (GTM) Strategies"],
    "icp": ["Go-To-Market (GTM) Strategies"],
    # Inbound
    "seo": ["Inbound & Content Marketing"],
    "organic": ["Inbound & Content Marketing"],
    "unqualified leads": ["Inbound & Content Marketing"],
    "nurture": ["Inbound & Content Marketing"],
    "email": ["Inbound & Content Marketing"],
    # MMM
    "budget allocation": ["Media Mix Modeling (MMM)"],
    "incrementality": ["Media Mix Modeling (MMM)"],
    "mmm": ["Media Mix Modeling (MMM)"],
    "media mix": ["Media Mix Modeling (MMM)"],
}

COMMON_PAIN_POINTS = {
    "📉 Declining marketing ROI": "roi roas budget allocation spend optimization diminishing returns",
    "🚫 Leads are not qualified": "unqualified leads inbound content seo funnel lead scoring nurturing",
    "🔍 Can't track customer journey": "tracking attribution ga4 journey cookie data silo analytics",
    "🧩 Data silos across platforms": "data silo dashboard reporting visibility analytics funnel",
    "💸 High customer acquisition cost (CAC)": "cac cpa expensive ads paid media bidding ad spend",
    "📊 No clear marketing attribution": "attribution multi-touch incrementality mmm media mix",
    "🌱 Low organic traffic / weak SEO": "seo organic traffic content blog inbound",
    "🚀 Planning a new product / market launch": "launch scale positioning icp gtm market entry",
    "🎯 Poor ad targeting & wasted spend": "targeting programmatic audience segmentation paid media",
    "📧 Email marketing underperforming": "email nurturing automation hubspot marketing automation",
}

COLLATERALS = [
    {
        "id": 1,
        "title": "E-Commerce Analytics Overhaul: 3× ROAS Recovery",
        "type": "case-study",
        "summary": "How server-side tagging and GA4 migration restored full attribution for a mid-market retailer.",
        "services": ["Analytics & Business Intelligence"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/analytics-case-study.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/analytics-case-study-preview.png",
    },
    {
        "id": 2,
        "title": "Media Mix Modeling for an FMCG Brand",
        "type": "case-study",
        "summary": "Statistical MMM revealed 28% budget reallocation opportunity across offline & digital.",
        "services": ["Media Mix Modeling (MMM)"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/mmm-case-study.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/mmm-preview.png",
    },
    {
        "id": 3,
        "title": "Cybage Paid Media Services – Capability Deck",
        "type": "deck",
        "summary": "Full overview of our paid search, social, and programmatic offering with pricing tiers.",
        "services": ["Paid Advertising Support"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/paid-media-deck.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/paid-media-preview.png",
    },
    {
        "id": 4,
        "title": "B2B SaaS GTM Playbook: 0 → $2M ARR",
        "type": "case-study",
        "summary": "ICP development, competitive benchmarking, and launch orchestration for a B2B SaaS client.",
        "services": ["Go-To-Market (GTM) Strategies"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/gtm-case-study.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/gtm-preview.png",
    },
    {
        "id": 5,
        "title": "Inbound Engine: 5× Lead Quality Improvement",
        "type": "case-study",
        "summary": "How lead scoring + SEO restructuring cut unqualified MQLs by 60% in 90 days.",
        "services": ["Inbound & Content Marketing"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/inbound-case-study.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/inbound-preview.png",
    },
    {
        "id": 6,
        "title": "Digital Marketing Services Brochure 2025",
        "type": "brochure",
        "summary": "One-pager covering all five Cybage Digital capability areas with service highlights.",
        "services": ["Analytics & Business Intelligence", "Media Mix Modeling (MMM)",
                     "Paid Advertising Support", "Go-To-Market (GTM) Strategies",
                     "Inbound & Content Marketing"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/cybage-digital-brochure.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/brochure-preview.png",
    },
    {
        "id": 7,
        "title": "CRO & Funnel Optimization Brochure",
        "type": "brochure",
        "summary": "Deep dive into our conversion optimization and behavior analytics methodology.",
        "services": ["Analytics & Business Intelligence", "Paid Advertising Support"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/cro-brochure.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/cro-preview.png",
    },
    {
        "id": 8,
        "title": "Performance Marketing Pitch Deck",
        "type": "deck",
        "summary": "Executive-ready deck positioning Cybage's paid media capabilities vs. competitors.",
        "services": ["Paid Advertising Support", "Media Mix Modeling (MMM)"],
        "file_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/perf-marketing-deck.pdf",
        "preview_url": "https://example-supabase.supabase.co/storage/v1/object/public/collaterals/previews/perf-deck-preview.png",
    },
]

# ─────────────────────────────────────────────
# ANALYSIS ENGINE
# ─────────────────────────────────────────────

def score_text_against_service(text: str, service_name: str, service_data: dict) -> float:
    """Score how well free-text aligns with a service using keyword frequency + synonym boost."""
    text_lower = text.lower()
    score = 0.0

    # Keyword hit scoring (weighted by word boundary match)
    for kw in service_data["keywords"]:
        kw_lower = kw.lower()
        if re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower):
            score += 2.0
        elif kw_lower in text_lower:
            score += 0.8

    # Synonym map boost
    for synonym, mapped_services in SYNONYM_MAP.items():
        if synonym in text_lower and service_name in mapped_services:
            score += 3.0

    return score


def analyse_free_text(text: str) -> dict:
    """Return dict of {service_name: score} for all services, sorted descending."""
    scores = {}
    for svc_name, svc_data in DIAGNOSTIC_MAPPING.items():
        scores[svc_name] = score_text_against_service(text, svc_name, svc_data)
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def analyse_pain_points(selected_labels: list) -> dict:
    """Turn selected pain-point labels into a combined text and score."""
    combined = " ".join(COMMON_PAIN_POINTS[lbl] for lbl in selected_labels if lbl in COMMON_PAIN_POINTS)
    return analyse_free_text(combined)


def get_relevant_collaterals(matched_services: list) -> list:
    relevant = []
    seen = set()
    for col in COLLATERALS:
        if col["id"] in seen:
            continue
        if any(svc in matched_services for svc in col["services"]):
            relevant.append(col)
            seen.add(col["id"])
    return relevant


# ─────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">⚡ Cybage Digital · Diagnostic Tool</div>
        <div class="hero-title">Find your <span>exact</span> digital<br>capability gap — in minutes.</div>
        <div class="hero-sub">
            Input your client's pain points and get a custom-mapped solution framework, 
            micro-service recommendations, and relevant case studies. Built for sales, 
            strategy, and client conversations.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_step_header(number: str, title: str):
    st.markdown(f"""
    <div class="step-header">
        <span class="step-pill">Step {number}</span>
        <span class="step-title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def render_service_card(rank: int, service_name: str, score: float, max_score: float):
    svc = DIAGNOSTIC_MAPPING[service_name]
    pct = min(int((score / max(max_score, 1)) * 100), 100)
    icon = svc["icon"]

    micro_chips = " ".join(f'<span class="micro-chip">{ms}</span>' for ms in svc["micro_services"])

    rank_label = {1: "Primary Recommendation", 2: "Secondary Recommendation"}.get(rank, "Additional Recommendation")

    st.markdown(f"""
    <div class="service-card">
        <div class="service-card-rank">{rank_label}</div>
        <div class="service-card-title">{icon}&nbsp; {service_name}</div>
        <div class="service-score-bar-wrap">
            <div class="service-score-bar" style="width:{pct}%"></div>
        </div>
        <div class="service-explanation">{svc["diagnostic_explanation"]}</div>
        <div><strong style="font-size:0.78rem;color:#7788AA;letter-spacing:0.08em;text-transform:uppercase;">Micro-Services Included</strong></div>
        <div style="margin-top:0.5rem">{micro_chips}</div>
    </div>
    """, unsafe_allow_html=True)


def render_collateral_card(col: dict):
    badge_class = {
        "case-study": "badge-case-study",
        "brochure":   "badge-brochure",
        "deck":       "badge-deck",
    }.get(col["type"], "badge-brochure")
    type_label = col["type"].replace("-", " ").title()

    st.markdown(f"""
    <div class="collateral-card">
        <span class="collateral-type-badge {badge_class}">{type_label}</span>
        <div class="collateral-title">{col["title"]}</div>
        <div class="collateral-desc">{col["summary"]}</div>
        <a class="dl-btn" href="{col["file_url"]}" target="_blank">⬇ Download</a>
        <a class="preview-btn" href="{col["preview_url"]}" target="_blank">👁 Preview</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────

def main():
    render_hero()

    # ── STEP 1: Client Context ──────────────────
    render_step_header("01", "Client Context")
    col1, col2 = st.columns([1, 1])
    with col1:
        company_name = st.text_input("Company Name", placeholder="e.g. Acme Corp")
    with col2:
        industry = st.selectbox("Industry", INDUSTRIES)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── STEP 2: Problem Diagnosis ───────────────
    render_step_header("02", "Problem Diagnosis")

    tab_a, tab_b = st.tabs(["🗂 Path A — Select Capabilities", "🔍 Path B — Pain Point Discovery (Recommended)"])

    service_scores = {}
    entry_method = None

    with tab_a:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        selected_services_a = st.multiselect(
            "Select one or more macro capabilities:",
            options=list(DIAGNOSTIC_MAPPING.keys()),
            placeholder="Choose services…",
        )
        if selected_services_a:
            service_scores = {svc: (5.0 if svc in selected_services_a else 0.0) for svc in DIAGNOSTIC_MAPPING}
            entry_method = "path_a"

    with tab_b:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.88rem;color:#7788AA;margin-bottom:0.8rem'>Select all pain points that resonate with your client:</div>", unsafe_allow_html=True)

        # Pain point multi-select via checkboxes
        cols = st.columns(2)
        selected_pain_points = []
        for i, (label, _) in enumerate(COMMON_PAIN_POINTS.items()):
            with cols[i % 2]:
                if st.checkbox(label, key=f"pp_{i}"):
                    selected_pain_points.append(label)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.88rem;color:#7788AA;margin-bottom:0.5rem'>— or describe the challenge in your own words —</div>", unsafe_allow_html=True)
        free_text = st.text_area(
            "Free-text input",
            placeholder="e.g. Our CAC has doubled, ads are expensive and we don't know which channel drives real results…",
            height=100,
            label_visibility="collapsed",
        )

        if selected_pain_points or free_text.strip():
            entry_method = "path_b"
            pain_scores = analyse_pain_points(selected_pain_points) if selected_pain_points else {}
            text_scores = analyse_free_text(free_text) if free_text.strip() else {}

            # Merge scores
            all_svcs = set(list(pain_scores.keys()) + list(text_scores.keys()))
            for svc in all_svcs:
                service_scores[svc] = pain_scores.get(svc, 0) + text_scores.get(svc, 0)

    # ── STEP 3: Solution Matrix ─────────────────
    if entry_method and service_scores:
        st.markdown("<hr>", unsafe_allow_html=True)
        render_step_header("03", "Your Custom Digital Strategy")

        # Filter to services with score > 0 (or all if path_a)
        if entry_method == "path_a":
            ranked = [(svc, 5.0) for svc in selected_services_a]
            top_names = [s for s, _ in ranked]
        else:
            ranked = [(svc, sc) for svc, sc in service_scores.items() if sc > 0]
            ranked.sort(key=lambda x: x[1], reverse=True)
            top_names = [s for s, _ in ranked[:4]]  # cap at 4

        if not ranked:
            st.info("No strong signal detected. Try adding more detail to your inputs.")
        else:
            # Insight banner
            primary = ranked[0][0] if ranked else ""
            secondary_list = [s for s, _ in ranked[1:3] if s != primary]
            secondary_txt = " and ".join(secondary_list) if secondary_list else ""

            if entry_method == "path_b":
                msg = f"Based on your inputs, your primary challenge relates to <strong>{primary}</strong>"
                if secondary_txt:
                    msg += f" with secondary gaps in <strong>{secondary_txt}</strong>"
                msg += ". Here is your custom mitigation framework:"
                st.markdown(f'<div class="insight-banner">🧠 {msg}</div>', unsafe_allow_html=True)

            max_score = ranked[0][1] if ranked else 1
            for rank_idx, (svc_name, score) in enumerate(ranked[:5], start=1):
                render_service_card(rank_idx, svc_name, score, max_score)

                # Expandable micro-service deep-dive
                with st.expander(f"📋 Expand: {svc_name} — Full Micro-Service Detail"):
                    svc = DIAGNOSTIC_MAPPING[svc_name]
                    for ms in svc["micro_services"]:
                        st.markdown(f"**→ {ms}**  \n*Addresses:* {svc['diagnostic_explanation'][:80]}…")
                        st.markdown("---")

        # ── STEP 4: Collaterals ─────────────────
        st.markdown("<hr>", unsafe_allow_html=True)
        render_step_header("04", "Proof of Capability")

        relevant = get_relevant_collaterals(top_names)
        if not relevant:
            st.info("No collaterals mapped yet for the selected services. Please check back soon.")
        else:
            col_count = 3
            rows = [relevant[i:i+col_count] for i in range(0, len(relevant), col_count)]
            for row in rows:
                cols = st.columns(col_count)
                for j, col_item in enumerate(row):
                    with cols[j]:
                        render_collateral_card(col_item)

        # ── Export Summary ──────────────────────
        if company_name.strip():
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="step-header"><span class="step-pill">Export</span><span class="step-title">Session Summary</span></div>', unsafe_allow_html=True)

            lines = [f"# Cybage Digital Diagnostic — {company_name}"]
            if industry != "Select Industry…":
                lines.append(f"**Industry:** {industry}")
            lines.append("\n## Recommended Services\n")
            for i, (svc, _) in enumerate(ranked[:5], 1):
                lines.append(f"### {i}. {svc}")
                lines.append(DIAGNOSTIC_MAPPING[svc]["diagnostic_explanation"])
                lines.append("\n**Micro-Services:**")
                for ms in DIAGNOSTIC_MAPPING[svc]["micro_services"]:
                    lines.append(f"- {ms}")
                lines.append("")

            lines.append("## Collaterals\n")
            for col_item in relevant:
                lines.append(f"- **{col_item['title']}** ({col_item['type']}): {col_item['summary']}")

            summary_text = "\n".join(lines)
            st.download_button(
                label="⬇ Download Diagnostic Summary (.md)",
                data=summary_text,
                file_name=f"cybage_diagnostic_{company_name.replace(' ', '_').lower()}.md",
                mime="text/markdown",
            )


if __name__ == "__main__":
    main()
