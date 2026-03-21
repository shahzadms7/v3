"""
GovRAG V3 — Streamlit Frontend (Compliance Cockpit + Career Intelligence)
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
Streamlit = 100% Python frontend. No HTML/CSS/JS needed.
This single file creates the ENTIRE user interface:
  - Left sidebar: Document sources, metrics, mode toggle
  - Center: Query input + grounded answer + citations
  - Right: Faithfulness bar, confidence score, audit trail

PRIVACY: Nothing stored. Refresh = clean slate.
"""

import streamlit as st
import httpx
import json
import time

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GovRAG — Grounded Knowledge Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for galaxy theme ───────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243E 100%); }
    .stTextInput > div > div > input { background-color: rgba(0,0,0,0.3); color: white; border: 1px solid rgba(255,255,255,0.2); }
    .stTextArea > div > div > textarea { background-color: rgba(0,0,0,0.3); color: white; border: 1px solid rgba(255,255,255,0.2); }
    .source-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; margin: 8px 0; }
    .metric-card { background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; }
    .trust-bar { height: 8px; border-radius: 4px; background: rgba(255,255,255,0.1); margin: 5px 0; }
    .rainbow-bar { height: 3px; background: linear-gradient(90deg, #ff0000, #ff8000, #ffff00, #00ff00, #0080ff, #8000ff, #ff0080); }
    div[data-testid="stSidebar"] { background: rgba(15,12,41,0.95); }
</style>
""", unsafe_allow_html=True)

# ── API Base URL ──────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

# ── Rainbow Bar ───────────────────────────────────────────────────────────────
st.markdown('<div class="rainbow-bar"></div>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🏛️ GovRAG — Grounded Knowledge Assistant")
    st.markdown("*Compliance + Career Intelligence | Zero Data Storage | Every Answer Cited*")
with col2:
    mode = st.selectbox("Mode", ["🏢 Compliance", "🌍 Career Intelligence", "🔄 Auto"], index=2)

st.markdown("---")

# ── Sidebar: Sources + Metrics ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 System Status")

    # Fetch health
    try:
        health = httpx.get(f"{API_URL}/api/health", timeout=5).json()
        st.success(f"✅ Online — v{health['version']}")
        st.metric("Documents Indexed", health["rag_index"]["total_chunks"])
        st.metric("AI Providers", health["rag_index"]["unique_sources"])

        col_a, col_b = st.columns(2)
        col_a.metric("Career", health["rag_index"]["career_chunks"])
        col_b.metric("Compliance", health["rag_index"]["compliance_chunks"])
    except Exception:
        st.warning("⏳ API starting up... Run: `uvicorn app.api.main:app`")

    st.markdown("---")
    st.markdown("### 📈 Audit Metrics")

    try:
        metrics_data = httpx.get(f"{API_URL}/api/metrics", timeout=5).json()
        m = metrics_data["metrics"]
        st.metric("Total Queries", m["total_queries"])
        st.metric("Avg Confidence", f"{m['avg_confidence']}%")
        st.metric("Avg Faithfulness", f"{m['avg_faithfulness']}%")
        st.metric("Block Rate", f"{m['block_rate']}%")
        st.metric("Avg Latency", f"{m['avg_latency_ms']}ms")
    except Exception:
        st.info("No metrics yet — ask a question first!")

    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.markdown("- **Zero data storage**")
    st.markdown("- No database")
    st.markdown("- Refresh = clean slate")
    st.markdown("- PII never logged")

# ── Main Content ──────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬 Ask a Question", "📄 Career Analyzer", "📊 Audit Dashboard"])

# ── Tab 1: Compliance/Career Query ────────────────────────────────────────────
with tab1:
    st.markdown("### Ask anything about your documents or career")
    st.markdown("*Every answer will cite exact sources. No hallucinations.*")

    query = st.text_area(
        "Your question:",
        placeholder="Examples:\n• What is our data retention policy for EU customers?\n• What are HIPAA breach notification requirements?\n• What certifications should a cloud engineer get in 2026?",
        height=100,
    )

    if st.button("🔍 Get Grounded Answer", type="primary", use_container_width=True):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Searching documents → Generating grounded answer → Verifying faithfulness..."):
                try:
                    mode_map = {"🏢 Compliance": "compliance", "🌍 Career Intelligence": "career", "🔄 Auto": "auto"}
                    resp = httpx.post(f"{API_URL}/api/query",
                                     json={"query": query, "mode": mode_map.get(mode, "auto")},
                                     timeout=60).json()

                    # Trust indicators
                    col_t1, col_t2, col_t3 = st.columns(3)
                    conf = resp.get("confidence", 0)
                    faith = resp.get("faithfulness", 0)
                    grounded = resp.get("grounded", False)

                    col_t1.metric("🎯 Confidence", f"{conf}%",
                                  delta="Trusted" if conf >= 70 else "Verify" if conf >= 40 else "Low")
                    col_t2.metric("📏 Faithfulness", f"{faith}%",
                                  delta="Grounded" if faith >= 70 else "Partial" if faith >= 40 else "Check")
                    col_t3.metric("⚡ Latency",
                                  f"{resp.get('metrics', {}).get('total_latency_ms', 0)}ms")

                    # Warnings
                    for w in resp.get("warnings", []):
                        st.warning(f"⚠️ {w}")

                    # Answer
                    st.markdown("### 📋 Answer")
                    st.markdown(resp.get("answer", "No answer available."))

                    # Sources
                    sources = resp.get("sources", [])
                    if sources:
                        st.markdown("### 📚 Sources (click to verify)")
                        for s in sources:
                            with st.expander(f"[Source {s['source_number']}] {s['document']} — {s['section']} (relevance: {s['relevance']})"):
                                st.markdown(f"**Document:** {s['document']}")
                                st.markdown(f"**Section:** {s['section']}")
                                st.markdown(f"**Type:** {s['doc_type']}")
                                st.markdown(f"**Preview:**\n{s['preview']}")

                    # Metrics detail
                    with st.expander("🔬 Full Metrics"):
                        st.json(resp.get("metrics", {}))

                except httpx.ConnectError:
                    st.error("❌ Cannot connect to API. Start it with: `uvicorn app.api.main:app --reload`")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ── Tab 2: Career Analyzer ───────────────────────────────────────────────────
with tab2:
    st.markdown("### 📄 Resume & Career Analysis")
    st.markdown("*Paste your resume. Get TOP 1% career advice grounded in real data. NEVER stored.*")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        resume = st.text_area("Paste your resume:", height=250, placeholder="Paste resume text here...\n\nYour data is NEVER stored. Gone on refresh.")
    with col_r2:
        job_desc = st.text_area("Job description (optional):", height=150, placeholder="Paste the job description you're targeting...")
        country = st.text_input("Your country:", placeholder="e.g., Canada, USA, UK, India")
        industry = st.selectbox("Industry:", ["IT", "Healthcare", "Finance", "Engineering", "Education",
                                               "Trades", "Marketing", "Legal", "HR", "Logistics",
                                               "Creative", "Hospitality", "Government", "Science", "Other"])
        analysis = st.selectbox("Analysis type:", ["full", "ats_score", "skills_gap", "rewrite", "interview_prep"])

    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if not resume.strip():
            st.error("Please paste your resume.")
        else:
            with st.spinner("Analyzing resume against career intelligence data..."):
                try:
                    resp = httpx.post(f"{API_URL}/api/career/analyze",
                                     json={"resume": resume, "job_description": job_desc,
                                           "analysis_type": analysis, "country": country,
                                           "industry": industry},
                                     timeout=60).json()

                    # Privacy reminder
                    st.info(f"🔒 {resp.get('privacy', 'Your data was NOT stored.')}")

                    analysis_data = resp.get("analysis", {})

                    # Score
                    score = analysis_data.get("score", 0)
                    col_s1, col_s2, col_s3 = st.columns(3)
                    col_s1.metric("📊 Score", f"{score}/100")
                    col_s2.metric("⏱️ Latency", f"{resp.get('metrics', {}).get('total_latency_ms', 0)}ms")
                    col_s3.metric("🤖 AI", resp.get("metrics", {}).get("provider", ""))

                    # Summary
                    st.markdown(f"### Summary\n{analysis_data.get('summary', '')}")

                    # Strengths & Weaknesses
                    col_w1, col_w2 = st.columns(2)
                    with col_w1:
                        st.markdown("### ✅ Strengths")
                        for s in analysis_data.get("strengths", []):
                            st.markdown(f"- {s}")
                    with col_w2:
                        st.markdown("### ❌ Weaknesses & Missing")
                        for w in analysis_data.get("weaknesses", []):
                            st.markdown(f"- 🔴 {w}")
                        for m in analysis_data.get("missing_skills", []):
                            st.markdown(f"- ⚠️ Missing: {m}")

                    # Recommendations
                    if analysis_data.get("recommended_certs"):
                        st.markdown("### 📜 Recommended Certifications")
                        for c in analysis_data["recommended_certs"]:
                            st.markdown(f"- {c}")

                    if analysis_data.get("action_items"):
                        st.markdown("### 🎯 Action Items")
                        for a in analysis_data["action_items"]:
                            st.markdown(f"- {a}")

                    # Sources
                    sources = resp.get("sources", [])
                    if sources:
                        with st.expander("📚 Career Intelligence Sources Used"):
                            for s in sources:
                                st.markdown(f"**[Source {s['source_number']}]** {s['document']} — {s['section']}")

                except httpx.ConnectError:
                    st.error("❌ Cannot connect to API. Start it with: `uvicorn app.api.main:app --reload`")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ── Tab 3: Audit Dashboard ───────────────────────────────────────────────────
with tab3:
    st.markdown("### 📊 Audit Dashboard — Full Observability")
    st.markdown("*Every query tracked. No PII logged. Metrics only.*")

    if st.button("🔄 Refresh Metrics"):
        st.rerun()

    try:
        metrics_resp = httpx.get(f"{API_URL}/api/metrics", timeout=5).json()
        m = metrics_resp["metrics"]

        # Top metrics row
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        col_m1.metric("Total Queries", m["total_queries"])
        col_m2.metric("Today", m["queries_today"])
        col_m3.metric("Avg Confidence", f"{m['avg_confidence']}%")
        col_m4.metric("Avg Faithfulness", f"{m['avg_faithfulness']}%")
        col_m5.metric("Blocked", m["total_blocked"])

        # By verdict
        st.markdown("#### Verdicts")
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        by_v = m.get("by_verdict", {})
        col_v1.metric("✅ Allowed", by_v.get("allow", 0))
        col_v2.metric("⚠️ Warned", by_v.get("warn", 0))
        col_v3.metric("🚫 Blocked", by_v.get("block", 0))
        col_v4.metric("❌ Errors", by_v.get("error", 0))

        # Recent audit entries
        st.markdown("#### Recent Audit Trail")
        recent = metrics_resp.get("recent", [])
        if recent:
            for entry in recent[:10]:
                verdict_icon = {"ALLOW": "✅", "WARN": "⚠️", "BLOCK": "🚫", "ERROR": "❌"}.get(entry["verdict"], "❓")
                st.markdown(
                    f"{verdict_icon} `{entry['timestamp'][:19]}` | "
                    f"Confidence: **{entry['confidence']}%** | "
                    f"Faithfulness: **{entry['faithfulness']}%** | "
                    f"{entry['provider']}/{entry['model']} | "
                    f"{entry['latency_ms']}ms | "
                    f"Mode: {entry['mode']}"
                )
        else:
            st.info("No queries yet. Ask a question to see audit trail!")

    except Exception:
        st.info("Start the API to see metrics: `uvicorn app.api.main:app --reload`")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "**GovRAG V3** — Grounded Knowledge Assistant | "
    "Microsoft Hackathon 2026 | "
    "100% Azure · 100% Python · Zero Data Storage · "
    "Built by Shahzad Muhammad + Claude Opus 4.6 + Zara (age 12)"
)
