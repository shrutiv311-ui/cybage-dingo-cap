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
    color: #E8EAF0 !important;
    border-radius: 10px !important;
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
# SUPABASE CONNECTION
# ─────────────────────────────────────────────
from supabase import create_client
import streamlit as st

@st.cache_resource
def get_supabase():
    """Initialize Supabase client with credentials from secrets."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = get_supabase()

# ─────────────────────────────────────────────
# DATA LAYER (from Supabase)
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_services():
    """Fetch all services from services_matrix table."""
    response = supabase.table("services_matrix").select("*").execute()
    services = response.data
    
    # Organize by macro_service name
    mapping = {}
    for row in services:
        macro = row["macro_service"]
        if macro not in mapping:
            mapping[macro] = {
                "keywords": [],
                "micro_services": [],
                "diagnostic_explanation": "",
                "icon": "⚙️"  # default icon
            }
        mapping[macro]["micro_services"].append(row["micro_service"])
        if row["description"]:
            mapping[macro]["diagnostic_explanation"] = row["description"]
    
    return mapping

@st.cache_data(ttl=3600)
def load_collaterals():
    """Fetch all collaterals from collaterals table."""
    response = supabase.table("collaterals").select("*").execute()
    return response.data

@st.cache_data(ttl=3600)
def load_pain_points():
    """Fetch all pain points from pain_point_map table."""
    response = supabase.table("pain_point_map").select("*").execute()
    pain_map = {}
    for row in response.data:
        pain_map[row["label"]] = row["keyword_string"]
    return pain_map

# Load data from Supabase
try:
    DIAGNOSTIC_MAPPING = load_services()
    COLLATERALS = load_collaterals()
    COMMON_PAIN_POINTS = load_pain_points()
except Exception as e:
    st.error(f"Failed to load data from Supabase: {e}")
    st.stop()

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
