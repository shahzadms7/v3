<div align="center">

# Alfalah AI — Career Intelligence Platform
### *الفلاح · "Come to Success"*

**Free AI career guidance for 8 billion people · No account · No data stored · 100% Microsoft Azure**

<br/>

[![Azure](https://img.shields.io/badge/Microsoft_Azure-100%25_Cloud-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-gpt--4o--mini-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/products/ai-services/openai-service)
[![Azure Functions](https://img.shields.io/badge/Azure_Functions_v2-Python_3.12-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/products/functions)
[![Azure AI Search](https://img.shields.io/badge/Azure_AI_Search-289_RAG_Chunks-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/products/ai-services/ai-search)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/shahzadms7/v3/actions)

[![Live](https://img.shields.io/badge/LIVE-govrag--v3--func.azurewebsites.net-22C55E?style=for-the-badge)](https://govrag-v3-func.azurewebsites.net)
[![Health](https://img.shields.io/badge/API_Health-/api/health-22C55E?style=for-the-badge)](https://govrag-v3-func.azurewebsites.net/api/health)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Hackathon](https://img.shields.io/badge/Microsoft_Hackathon-Innovation_Challenge_2026-FF6B35?style=for-the-badge)](https://github.com/shahzadms7/v3)

<br/>

[**🌐 Live Platform**](https://govrag-v3-func.azurewebsites.net) &nbsp;·&nbsp;
[**📊 API Health**](https://govrag-v3-func.azurewebsites.net/api/health) &nbsp;·&nbsp;
[**📊 PPTX Deck**](./Alfalah_AI_2026_V3.pptx) &nbsp;·&nbsp;
[**🏗️ Architecture**](./ARCHITECTURE.md) &nbsp;·&nbsp;
[**🤖 Responsible AI**](./docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md)

</div>

---

## 📸 Live Platform

![Alfalah AI — Homepage](./docs/screenshots/screencapture-govrag-v3-func-azurewebsites-net-2026-03-26-16_24_26.png)

---

## ⚡ Built in 7 Days — V3 At a Glance

> **Every human being on this planet deserves access to world-class career guidance — not just those who can afford it.**

| What | Number | Detail |
|------|--------|--------|
| **AI Career Tools** | **20** | One upload → 20 professional outputs in ~15 seconds |
| **Countries Supported** | **195** | All UN-recognized nations — salary, visa, labour law for each |
| **Azure Services** | **7** | Functions · OpenAI · AI Search · Content Safety · Key Vault · App Insights · Monitor |
| **RAG Knowledge Chunks** | **289** | Indexed in Azure AI Search from 35 Markdown files |
| **Knowledge Files** | **35** | 32 career + 3 compliance — ISCO-08 · ESCO · O\*NET · NOC Canada |
| **Occupations Covered** | **436** | ISCO-08 unit groups (ILO standard) + 3,000 ESCO + 1,016 O\*NET |
| **API Endpoints** | **10** | All serverless · Azure Functions v2 · Python 3.12 |
| **Parallel AI Calls** | **4** | ThreadPoolExecutor — all 4 fire simultaneously |
| **Response Time** | **~15 sec** | From upload to 20 tools delivered |
| **Cost to User** | **$0** | Free forever · no login · no account · no paywall |
| **Data Stored** | **Zero** | Processed in memory · discarded after response |
| **Build Time (V3)** | **7 days** | March 20–26, 2026 · 31 sessions · 1 developer |
| **Deploy Time** | **< 2 min** | GitHub push → Azure Functions live via GitHub Actions |
| **Lines of Code** | **887** | function_app.py — all 10 endpoints in Azure Functions v2 |

**Hackathon:** Microsoft AI Skills Challenge — Innovation Challenge — March 2026 · Submitted March 26, 2026

---

## 🏆 Judging Criteria — How This Project Scores

*The PPTX deck ([Alfalah_AI_2026_V3.pptx](./Alfalah_AI_2026_V3.pptx)) addresses each criterion on dedicated slides with visual evidence. Each section below mirrors the PPTX directly.*

| Criterion | Weight | PPTX Slide | Evidence |
|-----------|--------|-----------|----------|
| **Performance** | 25% | Slide 3 | 4 parallel calls · < 15 sec · 99.95% SLA · live health endpoint |
| **Innovation** | 25% | Slides 2, 5, 9 | 20 tools · 195 countries · free · zero storage · RAG architecture |
| **Breadth of Azure Services** | 25% | Slide 4 | 7 services in production · all in rg-v3 East US |
| **Responsible AI** | 25% | Slide 7 | 3-gate pipeline · RAI Standard v2 · full docs in /docs |

---

## 🚀 Performance — 25%

**How 20 tools are delivered in ~15 seconds:**

```
User Upload
     │
     ▼ < 200ms
Azure Content Safety ── screens for Hate · Violence · SelfHarm · Sexual
     │
     ▼ Pure Python · < 100ms
career_engine.py ── parse_resume() · naked_truth_score() · ats_score()
     │
     ▼ < 150ms
Azure AI Search ── semantic retrieval · top 7 chunks from 289 indexed
     │
     ▼ ThreadPoolExecutor(max_workers=4) — ALL 4 FIRE SIMULTANEOUSLY
     ├── Call 1 → Tools: Recruiter POV · Cover Letter · Resume Rewrite · JD Template
     ├── Call 2 → Tools: LinkedIn · Intro Scripts · Thank You Email · Salary Negotiation
     ├── Call 3 → Tools: 30-60-90 Plan · Cold Outreach · Career Pivot · Country Laws · Visa · Jobs
     └── Call 4 → Tools: Skills Gap · Interview Prep · STAR Stories
     │
     ▼ Merge all 4 JSON responses
Single Response: naked_truth + ats_match + cards[20] + similar_occupations + metrics + privacy
```

| Metric | Target | Notes |
|--------|--------|-------|
| End-to-end analysis | < 15 seconds | 4 parallel Azure OpenAI calls |
| Azure Content Safety | < 200ms | Every request, before any AI call |
| Azure AI Search retrieval | < 150ms | 289 chunks, semantic top-7 |
| Cold start (serverless) | < 3 seconds | Azure Functions Consumption plan |
| Platform uptime | 99.95% | Azure Functions SLA |
| CI/CD deploy | < 2 minutes | GitHub Actions → Azure live |

**Live verification:** [govrag-v3-func.azurewebsites.net/api/health](https://govrag-v3-func.azurewebsites.net/api/health)

---

## 💡 Innovation — 25%

**What makes this different from every other AI career tool:**

| Innovation | What Others Do | What Alfalah AI Does |
|-----------|---------------|----------------------|
| **Scope** | 1–3 tools | **20 tools in one analysis** |
| **Access** | Paid subscription | **Free forever · no login · no paywall** |
| **Geography** | 3–5 wealthy nations | **195 UN-recognized countries** |
| **Data privacy** | User profiles stored | **Zero storage by architecture** |
| **AI accuracy** | LLM guesses facts | **RAG retrieves facts first — AI formats only** |
| **Speed** | 2–5 minutes | **~15 seconds via 4 parallel calls** |
| **Occupation data** | Generic titles | **436 ISCO-08 groups · 3,000 ESCO · 1,016 O\*NET** |
| **Visa guidance** | Generic advice | **Every route + official government URLs** |

### 20 Career Intelligence Tools

All 20 tools from **one upload · one analysis · one Azure Functions call.**

| # | Tool | What It Delivers |
|---|------|-----------------|
| 01 | **Resume Score** | ATS 0–100 across 8 weighted dimensions with full breakdown |
| 02 | **Recruiter POV** | 6-second hiring manager skim — red flags + quick wins |
| 03 | **Cover Letter** | Top-1% framework · 3 quantified wins · confident close |
| 04 | **Resume Rewrite** | Impact-first bullets · ATS keyword audit · Top 3 wins first |
| 05 | **Skills Gap** | Matched/missing hard+soft · cert URLs · upskill roadmap |
| 06 | **Interview Prep** | 5 full STAR Q&As + questions to ask the interviewer |
| 07 | **STAR Stories** | 3 metrics-driven behavioural examples |
| 08 | **LinkedIn Summary** | Keyword-optimised About section (150–220 words) |
| 09 | **Intro Scripts** | Word-for-word 1-min / 2-min / 3-min verbal introductions |
| 10 | **Thank You Email** | Post-interview follow-up — subject line + full body |
| 11 | **Salary Negotiation** | Market ranges Entry→VP + anchor + counter-offer scripts |
| 12 | **30-60-90 Day Plan** | Structured onboarding milestones for first 90 days |
| 13 | **Cold Outreach** | LinkedIn note + DM + cold email + follow-up sequence |
| 14 | **Career Pivot** | Pivot score + 3 adjacent roles + 90-day transition plan |
| 15 | **Country Laws** | Notice period · termination rights · non-compete · worker rights |
| 16 | **Visa Pathways** | ALL immigration routes + official government URLs |
| 17 | **Matching Jobs** | Titles + companies + 7-country boards + recruiters |
| 18 | **Similar Occupations** | Adjacent roles from ISCO-08 international classification |
| 19 | **JD Template** | Professional job description for this exact role |
| 20 | **Live Job Openings** | Real-time listings from Remotive API · last 7 days |

---

## ☁️ Breadth of Azure Services — 25%

**7 Azure services in production — all in resource group `rg-v3` · East US:**

| Azure Service | Tier | API Version | How It's Used |
|---|---|---|---|
| **Azure Functions v2** | Consumption · serverless | v2 decorator | All 10 API endpoints · Python 3.12 · auto-scales to zero |
| **Azure OpenAI** | gpt-4o-mini · East US | 2024-08-01-preview | 4 parallel AI calls · 8192 tokens · temp 0.3 |
| **Azure AI Search** | Standard S1 | 2024-07-01 | 289 RAG chunks indexed · semantic + BM25 fallback |
| **Azure Content Safety** | Standard v1.0 | 2024-09-01 | Input screening on every request · 4 categories · severity 4 |
| **Azure Key Vault** | Standard | — | All secrets · azure-identity Managed Identity · zero credentials in code |
| **Application Insights** | Pay-per-use | v2 | Latency · errors · RAG chunk telemetry · CI/CD health check |
| **Azure Monitor** | Integrated | — | SLA monitoring · alert rules · cost tracking · rg-v3 dashboard |

```
rg-v3  (East US · Microsoft Hackathon Subscription)
├── govrag-v3-func          Azure Functions v2 · Python 3.12 · Consumption
├── Azure OpenAI            gpt-4o-mini · 4 parallel calls via ThreadPoolExecutor
├── career-knowledge        Azure AI Search index · 289 chunks · semantic retrieval
├── Azure Content Safety    Input gate · Hate/Violence/SelfHarm/Sexual · severity ≥ 4 = blocked
├── Azure Key Vault         azure-identity SDK · Managed Identity · RBAC · zero hardcoded secrets
├── Application Insights    Telemetry · latency tracking · error alerts
└── Azure Monitor           SLA dashboard · alert rules · resource health
```

**azure-identity** (Managed Identity) is used throughout — zero API keys in source code.

---

## 🤖 Responsible AI — 25%

*Implements Microsoft Responsible AI Standard v2 end-to-end across all 6 principles.*

### 3-Gate Safety Pipeline

Every single request passes all 3 gates before a response is returned:

```
GATE 1 — INPUT          GATE 2 — RETRIEVAL        GATE 3 — OUTPUT
────────────────────    ──────────────────────    ──────────────────────
Azure Content Safety    RAG Grounding             Source Citations
Hate · Violence         AI writes ONLY what       Every claim cited
SelfHarm · Sexual       knowledge base confirms   [Source N] mandatory
Severity ≥ 4 = BLOCKED  Faithfulness tracked      Hallucination < 5%
```

### 6 Responsible AI Principles

| Principle | Implementation |
|-----------|---------------|
| **Fairness** | No demographic data · no bias by nationality/age · 195 countries equal quality · ISCO-08 standard |
| **Privacy** | Zero database · zero storage · no cookies · no tracking · refresh = data gone forever |
| **Transparency** | Source citations on every response · ATS scoring methodology disclosed · full docs in /docs |
| **Safety** | Azure Content Safety on every input · 5MB limit · 45K char cap · rate limiting · injection guard |
| **Inclusiveness** | Ages 5–100 · youth/seniors/disability guides · 15 industries · 195 countries · ELI12 mode |
| **Accountability** | Application Insights audit trail · azure-identity RBAC · GitHub version history |

**Privacy is by architecture — not just policy.** No database exists. No resume is ever written to disk.

---

## 🏗️ Architecture

> Full Mermaid diagrams with request flow, RAG engine, security gates, CI/CD: **[ARCHITECTURE.md](./ARCHITECTURE.md)**

```
┌─────────────────────────────────────────────────── rg-v3 · East US ──┐
│                                                                        │
│   User Browser (195 countries · any device)                           │
│         │                                                              │
│         ▼                                                              │
│   Azure Functions v2 · Python 3.12 · 10 endpoints                     │
│         │                                                              │
│         ├─ GATE 1 ──► Azure Content Safety (input screen < 200ms)     │
│         │                                                              │
│         ├─ ZERO AI ──► career_engine.py (parse · score · ATS)         │
│         │                                                              │
│         ├─ RAG ──────► Azure AI Search (289 chunks · semantic top-7)  │
│         │                                                              │
│         ├─ 4 PARALLEL AZURE OPENAI CALLS (ThreadPoolExecutor)         │
│         │      Call 1 · Call 2 · Call 3 · Call 4 — simultaneous       │
│         │      gpt-4o-mini · 8192 tokens · ~15 seconds total          │
│         │                                                              │
│         ├──────────► Application Insights (telemetry · errors)        │
│         └──────────► Azure Key Vault (all secrets · Managed Identity) │
│                                                                        │
│   CI/CD: GitHub push → GitHub Actions → Azure live in < 2 min        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📡 API Reference

**Base URL:** `https://govrag-v3-func.azurewebsites.net`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Platform status · RAG chunk count · all Azure service connectivity |
| `POST` | `/career` | **Main endpoint** — full 20-tool career analysis |
| `POST` | `/upload` | Extract text from PDF / DOCX / TXT (in-memory · never stored) |
| `POST` | `/query` | Grounded RAG Q&A with source citations and faithfulness score |
| `POST` | `/decision` | Algorithmic career decision — 100% zero AI cost |
| `POST` | `/search-jobs` | Live job listings via Remotive API · last 7 days |
| `POST` | `/simplify` | ELI12 text simplification — grade3 / grade6 / grade9 / adult |
| `GET` | `/location` | IP-based country detection for auto-fill |
| `GET` | `/occupations` | ISCO-08 data inventory (436 groups · 3,000 ESCO · 1,016 O\*NET) |
| `GET` | `/responsible-ai` | Responsible AI principles and data handling statement |

```bash
# Full career analysis
curl -X POST https://govrag-v3-func.azurewebsites.net/career \
  -H "Content-Type: application/json" \
  -d '{"resume": "...", "job_description": "...", "country": "Canada", "industry": "IT"}'

# Response shape
{
  "naked_truth": { "composite_score": 74, "dimensions": {...} },
  "ats_match":   { "ats_score": 68, "keyword_gaps": [...] },
  "cards":       { "recruiterPov": {...}, "coverLetter": "...", ... },  // all 20 tools
  "similar_occupations": ["Data Analyst", "Business Intelligence Developer", ...],
  "metrics":     { "latency_ms": 14200, "provider": "Azure OpenAI", "model": "gpt-4o-mini" },
  "privacy":     "Your resume was NOT stored. Gone from memory after this response."
}
```

---

## 📚 RAG Knowledge Base — 289 Chunks from 35 Files

| File | Content | Chunks |
|------|---------|--------|
| `occupations-isco08-complete.md` | 436 ISCO-08 occupation groups (ILO standard) | ~80 |
| `occupations-master-isco08-all.md` | Extended ISCO-08 with descriptions | ~40 |
| `countries-195-complete.md` | All 195 UN countries — salary · visa · labour law | ~40 |
| `visa-immigration-195-countries.md` | All visa routes with official govt URLs | ~20 |
| `certifications-2026.md` | All-industry certs A–Z with enroll URLs | ~15 |
| `skills-az-master.md` + `soft-hard-skills-matrix-2026.md` | 900+ skills matrix | ~15 |
| `global-salary-data.md` + `salary-trends-global-2026.md` | Market salary benchmarks | ~12 |
| `top-1-percent-framework.md` + `resume-best-practices-2026.md` | Top recruiter methodology | ~10 |
| `future-occupations-2026-2125.md` | Emerging roles — 100-year horizon | ~10 |
| `interview-preparation.md` + `negotiation-scripts-word-by-word.md` | Prep + scripts | ~10 |
| `industry-trends-2026-global.md` + `job-market-challenges-2026.md` | Market intelligence | ~10 |
| `career-guide-youth-5-to-18.md` + `seniors-55-plus.md` + `accessibility-disability.md` | Inclusive guides | ~10 |
| 19 additional career + 3 compliance files | Cold outreach · LinkedIn · ATS · compliance | ~17 |

**Standards:** ILO ISCO-08 · European Commission ESCO v1.2 · US O\*NET · Statistics Canada NOC 2021

All files in `data/career/` and `data/compliance/`. Auto-indexed into Azure AI Search on first request.

---

## 🏗️ Repository Structure

```
shahzadms7/v3/
├── function_app.py              ← 887 lines · Azure Functions v2 · all 10 endpoints
├── host.json                    ← routePrefix: "" · Extension Bundle 4.*
├── requirements.txt             ← lean · no heavy ML · fast cold start
├── web.config                   ← Azure routing rules
├── ARCHITECTURE.md              ← full Mermaid diagrams · end-to-end data flow
├── TOOLS_BREAKDOWN.md           ← every Azure service · purpose · tier · version
├── Alfalah_AI_2026_V3.pptx      ← submission deck · 10 slides · speaker notes
│
├── app/core/
│   ├── career_engine.py         ← ATS scorer + resume parser (zero AI cost)
│   ├── decision_engine.py       ← career decision algorithm (zero AI cost)
│   ├── ai_provider.py           ← Azure OpenAI async client
│   ├── azure_ai_services.py     ← PII detection · key phrases · translation
│   ├── rag_engine.py            ← local BM25 fallback search
│   ├── safety_engine.py         ← Azure Content Safety wrapper
│   ├── audit_logger.py          ← Application Insights telemetry
│   └── config.py                ← pydantic-settings · all config from env vars
│
├── data/
│   ├── career/                  ← 32 Markdown knowledge files
│   └── compliance/              ← 3 compliance reference files
│
├── static/
│   └── index.html               ← complete frontend (HTML · CSS · Vanilla JS · no framework)
│
├── docs/
│   ├── RESPONSIBLE_AI_IMPACT_ASSESSMENT.md  ← Microsoft RAI Standard v2 · full risk register
│   ├── TRANSPARENCY_NOTE.md                 ← capabilities · limitations · performance targets
│   └── screenshots/                         ← platform screenshots
│
├── scripts/
│   ├── build_submission_deck.py ← rebuilds the PPTX from scratch
│   └── build_master_files.py    ← data file utilities
│
└── .github/workflows/
    └── main_govrag-v3.yml       ← GitHub Actions → Azure Functions · < 2 min deploy
```

---

## ⚙️ CI/CD Pipeline

```
git push origin main
        │
        ▼
GitHub Actions (ubuntu-latest)
        ├── actions/checkout@v4
        ├── actions/setup-python@v5  →  Python 3.12
        ├── pip install -r requirements.txt  →  .python_packages/
        ├── Azure/functions-action@v1
        │     app-name: govrag-v3-func
        │     publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
        │     scm-do-build-during-deployment: true
        └── Health check: GET /api/health  (30s warm-up)

Deploy time: < 2 minutes · Zero downtime · Serverless swap
```

---

## 💻 Local Development

```bash
# Prerequisites: Python 3.12 · Azure Functions Core Tools v4
git clone https://github.com/shahzadms7/v3
cd v3
pip install -r requirements.txt

# Environment variables (never hardcoded — loaded from Azure Key Vault in production)
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
export AZURE_SEARCH_ENDPOINT="https://your-search.search.windows.net"
export AZURE_SEARCH_KEY="your-key"
export AZURE_CONTENT_SAFETY_ENDPOINT="https://your-cs.cognitiveservices.azure.com"
export AZURE_CONTENT_SAFETY_KEY="your-key"

func start
curl http://localhost:7071/api/health
```

---

## 📖 Deep Dive Documentation

Everything a judge, developer, or reviewer needs — all in this repository:

| Document | What's Inside | Link |
|----------|--------------|------|
| **ARCHITECTURE.md** | End-to-end Mermaid diagrams · request flow · RAG engine · 20-tool execution map · security architecture · CI/CD · performance table | [View](./ARCHITECTURE.md) |
| **TOOLS_BREAKDOWN.md** | Every Azure service with tier · cost · API version · how it connects · Python dependencies | [View](./TOOLS_BREAKDOWN.md) |
| **docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md** | Microsoft RAI Standard v2 · stakeholder analysis · harm matrix · 6 fairness sections · risk register · approval record | [View](./docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md) |
| **docs/TRANSPARENCY_NOTE.md** | Capabilities vs. limitations · performance targets · 8 design decisions · evaluation methodology · all disclaimers | [View](./docs/TRANSPARENCY_NOTE.md) |
| **Alfalah_AI_2026_V3.pptx** | 10-slide submission deck · speaker notes on every slide · real platform screenshots · judge scorecard | [Download](./Alfalah_AI_2026_V3.pptx) |

---

## 🧰 Full Tech Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Cloud | Microsoft Azure | — | 100% infrastructure · rg-v3 · East US |
| AI | Azure OpenAI gpt-4o-mini | 2024-08-01-preview | 4 parallel career analysis calls |
| Search | Azure AI Search | 2024-07-01 | RAG semantic retrieval · 289 chunks |
| Safety | Azure Content Safety | v1.0 · 2024-09-01 | Input gate — every request |
| Security | Azure Key Vault + azure-identity | — | Managed Identity · zero credentials in code |
| Monitoring | Application Insights + Azure Monitor | v2 | Telemetry · alerts · SLA |
| Backend | Python | 3.12 | Azure Functions v2 decorator runtime |
| HTTP | httpx | ≥0.28.0 | Azure OpenAI calls inside ThreadPoolExecutor |
| PDF | pdfminer.six + pymupdf | latest | Resume extraction · dual fallback |
| DOCX | python-docx | ≥1.1.0 | Word document extraction |
| Config | pydantic-settings | ≥2.0.0 | All settings from environment variables |
| Frontend | HTML5 · CSS3 · Vanilla JS | — | No framework · no build step · instant load |
| CI/CD | GitHub Actions | — | Push to main → Azure live in < 2 min |
| Dev AI | Claude Sonnet 4.6 (Claude Code) | — | AI pair programmer · 31 sessions |

---

<div align="center">

*Alfalah AI &nbsp;·&nbsp; Mississauga, Ontario, Canada &nbsp;·&nbsp; Built on Microsoft Azure &nbsp;·&nbsp; Free Forever*

**[🌐 Live Platform](https://govrag-v3-func.azurewebsites.net) &nbsp;·&nbsp; [📊 API Health](https://govrag-v3-func.azurewebsites.net/api/health) &nbsp;·&nbsp; [💻 GitHub](https://github.com/shahzadms7/v3) &nbsp;·&nbsp; [🤖 Responsible AI](./docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md)**

*الفلاح — Come to Success — For Every Human on Earth*

</div>
