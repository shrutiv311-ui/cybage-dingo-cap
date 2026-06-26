-- ============================================================
-- Cybage Digital Capability Diagnostic Tool
-- Supabase SQL Schema + Seed Data
-- Run this in: Supabase Dashboard > SQL Editor > New Query
-- ============================================================

-- ── 1. Enable extensions ─────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── 2. Drop tables if re-running ────────────────────────────
DROP TABLE IF EXISTS collaterals        CASCADE;
DROP TABLE IF EXISTS services_matrix    CASCADE;
DROP TABLE IF EXISTS pain_point_map     CASCADE;

-- ── 3. services_matrix ──────────────────────────────────────
CREATE TABLE services_matrix (
    id                  SERIAL PRIMARY KEY,
    macro_service       TEXT        NOT NULL,
    micro_service       TEXT        NOT NULL,
    mapped_pain_points  TEXT[]      NOT NULL DEFAULT '{}',
    description         TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── 4. collaterals ──────────────────────────────────────────
CREATE TABLE collaterals (
    id                      SERIAL PRIMARY KEY,
    title                   TEXT        NOT NULL,
    type                    TEXT        NOT NULL CHECK (type IN ('case-study','brochure','deck')),
    associated_macro_services TEXT[]    NOT NULL DEFAULT '{}',
    summary                 TEXT,
    file_url                TEXT,
    preview_url             TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── 5. pain_point_map (optional lookup table) ───────────────
CREATE TABLE pain_point_map (
    id              SERIAL PRIMARY KEY,
    label           TEXT    NOT NULL,
    keyword_string  TEXT    NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── 6. Row Level Security (public read, auth required write) ─
ALTER TABLE services_matrix  ENABLE ROW LEVEL SECURITY;
ALTER TABLE collaterals       ENABLE ROW LEVEL SECURITY;
ALTER TABLE pain_point_map    ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read services_matrix"
    ON services_matrix FOR SELECT USING (true);

CREATE POLICY "Public read collaterals"
    ON collaterals FOR SELECT USING (true);

CREATE POLICY "Public read pain_point_map"
    ON pain_point_map FOR SELECT USING (true);

-- ── 7. Seed: services_matrix ─────────────────────────────────

-- Analytics & Business Intelligence
INSERT INTO services_matrix (macro_service, micro_service, mapped_pain_points, description) VALUES
('Analytics & Business Intelligence',
 'Server-Side Tagging & Privacy-First Tracking Setups',
 ARRAY['Data silos across platforms','Can''t track customer journey','No clear marketing attribution'],
 'Deploy server-side GTM containers to capture accurate, consent-compliant data without third-party cookie dependency.'),

('Analytics & Business Intelligence',
 'GA4 Architecture Audits & Advanced Event Implementation',
 ARRAY['Can''t track customer journey','Data silos across platforms'],
 'Full GA4 property audit, custom event schema design, and BigQuery export configuration for enterprise-grade reporting.'),

('Analytics & Business Intelligence',
 'Automated Looker Studio & Power BI Dashboard Engineering',
 ARRAY['Data silos across platforms','No clear marketing attribution'],
 'Connect all data sources into a single, auto-refreshing executive dashboard eliminating manual reporting.'),

('Analytics & Business Intelligence',
 'Multi-Touch Attribution Modeling & Funnel Leakage Analysis',
 ARRAY['No clear marketing attribution','Declining marketing ROI','Can''t track customer journey'],
 'Build data-driven attribution models to correctly credit each touchpoint and identify where leads drop off.'),

('Analytics & Business Intelligence',
 'Conversion Rate Optimization (CRO) & User Behavior Mapping',
 ARRAY['Declining marketing ROI','Poor ad targeting & wasted spend'],
 'Heatmaps, session recordings, and A/B test orchestration to lift conversion rates without increasing spend.');

-- Media Mix Modeling (MMM)
INSERT INTO services_matrix (macro_service, micro_service, mapped_pain_points, description) VALUES
('Media Mix Modeling (MMM)',
 'Privacy-Safe Statistical Media Mix Modeling',
 ARRAY['No clear marketing attribution','Declining marketing ROI'],
 'Bayesian MMM using aggregate spend and outcome data — no user-level cookies required.'),

('Media Mix Modeling (MMM)',
 'Cross-Channel Budget Optimization & Forecasting',
 ARRAY['Declining marketing ROI','High customer acquisition cost (CAC)'],
 'Prescriptive scenario planning to find the optimal channel budget split for your revenue targets.'),

('Media Mix Modeling (MMM)',
 'Incrementality Testing & Lift Analysis',
 ARRAY['No clear marketing attribution','Declining marketing ROI'],
 'Geo-holdout and PSA experiments to measure the true causal impact of media investment.'),

('Media Mix Modeling (MMM)',
 'External Factor (Seasonality/Economic) Impact Analysis',
 ARRAY['Declining marketing ROI'],
 'Decompose marketing performance variance between campaign actions and external macro-economic forces.');

-- Paid Advertising Support
INSERT INTO services_matrix (macro_service, micro_service, mapped_pain_points, description) VALUES
('Paid Advertising Support',
 'Paid Search & Social Campaign Restructuring',
 ARRAY['High customer acquisition cost (CAC)','Declining marketing ROI','Poor ad targeting & wasted spend'],
 'Account architecture overhaul for Google, Meta, and LinkedIn — consolidate campaigns, eliminate overlap, reduce CPA.'),

('Paid Advertising Support',
 'Audience Segmentation & First-Party Data Targeting',
 ARRAY['Poor ad targeting & wasted spend','Leads are not qualified'],
 'Build CRM-based custom audiences and lookalike models to reach high-intent buyers at scale.'),

('Paid Advertising Support',
 'Smart Bidding Optimization & Ad Fraud Mitigation',
 ARRAY['High customer acquisition cost (CAC)','Poor ad targeting & wasted spend'],
 'Deploy value-based bidding strategies and install click-fraud protection to maximize every ad dollar.'),

('Paid Advertising Support',
 'Creative Testing Frameworks & Copywriting Support',
 ARRAY['Declining marketing ROI','Poor ad targeting & wasted spend'],
 'Structured creative experimentation (hooks, formats, CTAs) backed by statistical significance thresholds.');

-- Go-To-Market (GTM) Strategies
INSERT INTO services_matrix (macro_service, micro_service, mapped_pain_points, description) VALUES
('Go-To-Market (GTM) Strategies',
 'Ideal Customer Profile (ICP) & Persona Development',
 ARRAY['Planning a new product / market launch','Leads are not qualified'],
 'Data-enriched ICP built from CRM, intent signals, and interview synthesis — know exactly who to target.'),

('Go-To-Market (GTM) Strategies',
 'Competitive Landscape Mapping & Benchmarking',
 ARRAY['Planning a new product / market launch'],
 'Systematic competitor analysis across positioning, pricing, messaging, and digital share of voice.'),

('Go-To-Market (GTM) Strategies',
 'Multi-Channel Launch Orchestration Playbooks',
 ARRAY['Planning a new product / market launch'],
 'Week-by-week execution playbook coordinating paid, organic, email, and PR across launch phases.'),

('Go-To-Market (GTM) Strategies',
 'Value Proposition & Messaging Framework Design',
 ARRAY['Planning a new product / market launch','Leads are not qualified'],
 'Jobs-to-be-done messaging architecture mapped to each ICP segment and stage of the buying journey.');

-- Inbound & Content Marketing
INSERT INTO services_matrix (macro_service, micro_service, mapped_pain_points, description) VALUES
('Inbound & Content Marketing',
 'Technical SEO & Content Velocity Audits',
 ARRAY['Low organic traffic / weak SEO','Leads are not qualified'],
 'Core Web Vitals, crawlability, and topical authority audit with a 90-day content sprint roadmap.'),

('Inbound & Content Marketing',
 'B2B Lead Nurturing & Marketing Automation Workflows',
 ARRAY['Leads are not qualified','Email marketing underperforming'],
 'HubSpot / Marketo workflow builds that segment, score, and advance leads through every funnel stage.'),

('Inbound & Content Marketing',
 'High-Intent Content Mapping & Asset Creation',
 ARRAY['Low organic traffic / weak SEO','Leads are not qualified'],
 'Keyword-to-content matrix targeting bottom-of-funnel queries where purchase intent is highest.'),

('Inbound & Content Marketing',
 'Inbound Funnel Mapping & Lead Scoring Setups',
 ARRAY['Leads are not qualified','Email marketing underperforming','Can''t track customer journey'],
 'Design lead-scoring models in your MAP that filter out noise and surface only sales-ready MQLs.');

-- ── 8. Seed: collaterals ──────────────────────────────────────
INSERT INTO collaterals (title, type, associated_macro_services, summary, file_url, preview_url) VALUES

('E-Commerce Analytics Overhaul: 3× ROAS Recovery',
 'case-study',
 ARRAY['Analytics & Business Intelligence'],
 'How server-side tagging and GA4 migration restored full attribution for a mid-market retailer.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/analytics-case-study.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/analytics-preview.png'),

('Media Mix Modeling for an FMCG Brand',
 'case-study',
 ARRAY['Media Mix Modeling (MMM)'],
 'Statistical MMM revealed 28% budget reallocation opportunity across offline & digital channels.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/mmm-case-study.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/mmm-preview.png'),

('Cybage Paid Media Services – Capability Deck',
 'deck',
 ARRAY['Paid Advertising Support'],
 'Full overview of our paid search, social, and programmatic offering with pricing tiers.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/paid-media-deck.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/paid-media-preview.png'),

('B2B SaaS GTM Playbook: 0 → $2M ARR',
 'case-study',
 ARRAY['Go-To-Market (GTM) Strategies'],
 'ICP development, competitive benchmarking, and launch orchestration for a B2B SaaS client.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/gtm-case-study.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/gtm-preview.png'),

('Inbound Engine: 5× Lead Quality Improvement',
 'case-study',
 ARRAY['Inbound & Content Marketing'],
 'How lead scoring + SEO restructuring cut unqualified MQLs by 60% in 90 days.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/inbound-case-study.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/inbound-preview.png'),

('Digital Marketing Services Brochure 2025',
 'brochure',
 ARRAY['Analytics & Business Intelligence','Media Mix Modeling (MMM)','Paid Advertising Support','Go-To-Market (GTM) Strategies','Inbound & Content Marketing'],
 'One-pager covering all five Cybage Digital capability areas with service highlights.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/cybage-digital-brochure.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/brochure-preview.png'),

('CRO & Funnel Optimization Brochure',
 'brochure',
 ARRAY['Analytics & Business Intelligence','Paid Advertising Support'],
 'Deep dive into our conversion optimization and behavior analytics methodology.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/cro-brochure.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/cro-preview.png'),

('Performance Marketing Pitch Deck',
 'deck',
 ARRAY['Paid Advertising Support','Media Mix Modeling (MMM)'],
 'Executive-ready deck positioning Cybage''s paid media capabilities vs. competitors.',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/perf-marketing-deck.pdf',
 'https://<YOUR_PROJECT>.supabase.co/storage/v1/object/public/collaterals/previews/perf-deck-preview.png');

-- ── 9. Seed: pain_point_map ──────────────────────────────────
INSERT INTO pain_point_map (label, keyword_string) VALUES
('📉 Declining marketing ROI',             'roi roas budget allocation spend optimization diminishing returns'),
('🚫 Leads are not qualified',             'unqualified leads inbound content seo funnel lead scoring nurturing'),
('🔍 Can''t track customer journey',       'tracking attribution ga4 journey cookie data silo analytics'),
('🧩 Data silos across platforms',         'data silo dashboard reporting visibility analytics funnel'),
('💸 High customer acquisition cost (CAC)','cac cpa expensive ads paid media bidding ad spend'),
('📊 No clear marketing attribution',      'attribution multi-touch incrementality mmm media mix'),
('🌱 Low organic traffic / weak SEO',      'seo organic traffic content blog inbound'),
('🚀 Planning a new product / market launch','launch scale positioning icp gtm market entry'),
('🎯 Poor ad targeting & wasted spend',    'targeting programmatic audience segmentation paid media'),
('📧 Email marketing underperforming',     'email nurturing automation hubspot marketing automation');

-- ── 10. Verification queries ─────────────────────────────────
-- Run these to confirm data loaded correctly:
-- SELECT macro_service, COUNT(*) FROM services_matrix GROUP BY macro_service;
-- SELECT type, COUNT(*) FROM collaterals GROUP BY type;
-- SELECT COUNT(*) FROM pain_point_map;
