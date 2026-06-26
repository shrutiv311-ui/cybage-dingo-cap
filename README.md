# ⚡ Cybage Digital Capability Diagnostic Tool

A premium sales-enablement web application that dynamically maps client pain points to Cybage Digital's service capabilities, micro-services, and marketing collaterals.

---

## 🚀 Quick Start (Standalone — No Supabase Required)

The app ships with all data hardcoded in `app.py`, so it runs immediately:

```bash
pip install streamlit
streamlit run app.py
```

Open `http://localhost:8501` — fully functional with mock data.

---

## 🗄 Supabase Integration (Optional — for live data management)

### Step 1: Create a Supabase Project
1. Go to [supabase.com](https://supabase.com) → New Project
2. Note your **Project URL** and **anon/public API key**

### Step 2: Run the Schema
1. Open **SQL Editor** in your Supabase dashboard
2. Paste the entire contents of `supabase_schema.sql`
3. Click **Run** — tables are created and seeded

### Step 3: Upload Collateral Files
1. Go to **Storage** → Create bucket named `collaterals`
2. Set it to **Public**
3. Upload your PDFs, decks, and preview images
4. Replace `<YOUR_PROJECT>` in the SQL seed with your actual Supabase project ref

### Step 4: Connect the App
Add a `.streamlit/secrets.toml` file:

```toml
[supabase]
url = "https://YOUR_PROJECT_REF.supabase.co"
key = "YOUR_ANON_PUBLIC_KEY"
```

Then extend `app.py` to fetch from Supabase:

```python
from supabase import create_client
import streamlit as st

@st.cache_resource
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = get_supabase()

# Fetch services
services = supabase.table("services_matrix").select("*").execute().data

# Fetch collaterals
collaterals = supabase.table("collaterals").select("*").execute().data
```

---

## 🏗 Architecture

```
app.py
├── DATA LAYER          — All mapping data + synonym dictionary
├── ANALYSIS ENGINE     — Keyword scoring + synonym boost algorithm
│   ├── score_text_against_service()
│   ├── analyse_free_text()
│   └── analyse_pain_points()
└── UI COMPONENTS
    ├── render_hero()
    ├── render_step_header()
    ├── render_service_card()      — with animated score bar
    └── render_collateral_card()   — with Download + Preview links
```

### User Flow
```
Step 01: Client Context (Company + Industry)
Step 02: Diagnosis
  ├── Path A: Direct service selection (multi-select)
  └── Path B: Pain point checkboxes + free-text entry
Step 03: Solution Matrix (ranked, scored, explained)
Step 04: Proof of Capability (case studies, decks, brochures)
Export:  Download .md summary
```

---

## 🧠 Scoring Engine

The analysis engine scores free-text inputs across all 5 service categories:

| Signal Type       | Score Weight |
|------------------|-------------|
| Exact keyword (word boundary) | +2.0 per hit |
| Partial keyword match | +0.8 per hit |
| Synonym map match | +3.0 per hit |

Services are ranked by total score and displayed in descending order. The UI shows a relative confidence bar for each recommendation.

---

## 📁 File Structure

```
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── supabase_schema.sql     # Full DB schema + seed data
└── README.md               # This file
```

---

## 📊 Database Schema

### `services_matrix`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| macro_service | TEXT | Top-level service area |
| micro_service | TEXT | Specific deliverable |
| mapped_pain_points | TEXT[] | Pain points this addresses |
| description | TEXT | Plain-language explanation |

### `collaterals`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| title | TEXT | Document title |
| type | TEXT | case-study / brochure / deck |
| associated_macro_services | TEXT[] | Services this supports |
| summary | TEXT | One-line description |
| file_url | TEXT | Supabase storage URL |
| preview_url | TEXT | Thumbnail image URL |

---

## 🎨 Design System

- **Background:** `#0A0D14` (deep navy)
- **Accent:** `#63B3ED` (cool blue)
- **Surface:** `rgba(255,255,255,0.03)` glass cards
- **Typography:** Syne (display) + Inter (body)
- **Accent bar:** left-border gradient on service cards
