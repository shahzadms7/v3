# Alfalah AI — Career Intelligence Platform · System Architecture
### *End-to-End Technical Architecture · 100% Microsoft Azure · Built for 8 Billion People*

<div align="center">

![Azure](https://img.shields.io/badge/100%25_Microsoft_Azure-Cloud_Native-0078D4?style=for-the-badge&logo=microsoftazure)
![AI](https://img.shields.io/badge/Azure_OpenAI-4_Parallel_Calls-0078D4?style=for-the-badge&logo=microsoftazure)
![RAG](https://img.shields.io/badge/RAG_Engine-35_Files_%7C_289_Chunks-8B5CF6?style=for-the-badge)

</div>

---

## High-Level System Overview

```mermaid
graph TB
    subgraph USER["👤 USER — 195 Countries · Any Device"]
        Browser["🌐 Web Browser<br/>(Chrome · Safari · Firefox · Edge)"]
    end

    subgraph FRONTEND["📄 STATIC FRONTEND — Served by Azure Functions"]
        HTML["index.html · CSS · Vanilla JS<br/>Galaxy UI · 20-Tool Dashboard<br/>195-Country Auto-Detection"]
    end

    subgraph AZURE_FUNCTIONS["⚡ AZURE FUNCTIONS v2 — Python 3.12 Serverless · 10 Endpoints"]
        CareerAPI["POST /career<br/>20-Tool Analysis"]
        QueryAPI["POST /query<br/>RAG Q&A"]
        UploadAPI["POST /upload<br/>File Extraction"]
        LocationAPI["GET /location<br/>IP Detection"]
        HealthAPI["GET /health<br/>System Status"]
        SimplifyAPI["POST /simplify<br/>ELI12 Mode"]
        DecisionAPI["POST /decision<br/>Career Decision"]
        JobsAPI["POST /search-jobs<br/>Live Listings"]
        OccAPI["GET /occupations<br/>ISCO-08 Data"]
        RAIAPI["GET /responsible-ai<br/>RAI Card"]
    end

    subgraph AI_LAYER["🤖 AZURE OPENAI — 4 Parallel Calls · ThreadPoolExecutor"]
        Call1["Call 1<br/>Tools 1–4<br/>Recruiter+Cover+Rewrite+JD"]
        Call2["Call 2<br/>Tools 5–8<br/>LinkedIn+Scripts+Email+Salary"]
        Call3["Call 3<br/>Tools 9–14<br/>Plan+Outreach+Pivot+Laws+Visa+Jobs"]
        Call4["Call 4<br/>Tools 15–20<br/>Skills+Interview+STAR"]
    end

    subgraph RAG["📚 RAG KNOWLEDGE ENGINE — 35 Files · 289 Chunks"]
        Occupations["436 ISCO-08<br/>Occupations"]
        Countries["195 Country<br/>Data Packages"]
        Skills["900+ Skills<br/>A-Z Master"]
        Future["Future Jobs<br/>2026–2125"]
        Framework["Top-1% Hiring<br/>Framework"]
        More["30 Additional<br/>Intelligence Files"]
    end

    subgraph AZURE_SERVICES["🔒 AZURE SUPPORTING SERVICES"]
        KeyVault["🔑 Azure Key Vault<br/>Secrets · RBAC · Managed Identity"]
        AISearch["🔍 Azure AI Search<br/>Semantic Retrieval · BM25 Fallback"]
        ContentSafety["🛡️ Azure Content Safety<br/>Input Screening · 4 Categories"]
        Monitor["📊 Application Insights<br/>Telemetry · Latency · Errors"]
    end

    subgraph EXTERNAL["🌍 EXTERNAL APIs"]
        Remotive["Remotive API<br/>Live Job Listings (Free)"]
        IPApi["ip-api.com<br/>IP Geolocation"]
    end

    subgraph DEVOPS["🔄 CI/CD — GitHub → Azure · <2 min deploy"]
        GitHub["GitHub<br/>shahzadms7/v3"]
        GHActions["GitHub Actions<br/>Auto-Deploy on push to main"]
        ClaudeCode["Claude Code<br/>AI Pair Programmer"]
    end

    Browser --> HTML
    HTML --> CareerAPI
    HTML --> QueryAPI
    HTML --> UploadAPI
    HTML --> LocationAPI
    HTML --> JobsAPI

    CareerAPI --> ContentSafety
    ContentSafety --> AISearch
    AISearch --> Call1
    AISearch --> Call2
    AISearch --> Call3
    AISearch --> Call4

    Call1 & Call2 & Call3 & Call4 --> CareerAPI

    AISearch -.->|"fallback"| RAG
    CareerAPI --> Monitor
    KeyVault --> CareerAPI

    GitHub --> GHActions --> AZURE_FUNCTIONS
```

---

## Request Processing Flow — POST /career (Main Endpoint)

```mermaid
sequenceDiagram
    participant User as 👤 User Browser
    participant AzFunc as ⚡ Azure Functions v2
    participant Safety as 🛡️ Azure Content Safety
    participant Engine as 🔧 career_engine.py
    participant Search as 🔍 Azure AI Search
    participant OAI as 🤖 Azure OpenAI
    participant MI as Application Insights

    User->>AzFunc: POST /career {resume, job_desc, country, industry}
    AzFunc->>Safety: Screen resume text (Hate/Violence/SelfHarm/Sexual)
    Safety-->>AzFunc: ✅ Safe (severity < 4)

    Note over AzFunc,Engine: STEP 1-3: Zero AI Cost (pure Python)
    AzFunc->>Engine: parse_resume(resume)
    Engine-->>AzFunc: parsed {sections, bullets, dates, keywords}
    AzFunc->>Engine: naked_truth_score(parsed, job_desc, country, industry)
    Engine-->>AzFunc: score {composite_score, 8 dimensions, knockouts}
    AzFunc->>Engine: ats_score(resume, job_desc)
    Engine-->>AzFunc: ats {match_%, keyword_gaps, density}

    Note over AzFunc,Search: STEP 4: RAG Retrieval
    AzFunc->>Search: search(terms, top_k=7)
    Search-->>AzFunc: 7 relevant chunks from 289 indexed

    Note over AzFunc,OAI: STEP 5: 4 Parallel Azure OpenAI Calls
    par ThreadPoolExecutor max_workers=4
        AzFunc->>OAI: Call 1 — Tools 1-4 (recruiterPov, coverLetter, resumeRewrite, jd_template)
        AzFunc->>OAI: Call 2 — Tools 5-8 (linkedinSummary, introScripts, thankYouEmail, salaryNeg)
        AzFunc->>OAI: Call 3 — Tools 9-14 (actionPlan, coldOutreach, careerPivot, countryLaws, visa, jobs)
        AzFunc->>OAI: Call 4 — Tools 15-20 (skillsGap, interviewPrep, starStories)
    end
    OAI-->>AzFunc: 4 JSON responses merged → 20 tools

    AzFunc->>MI: Log latency, model, chunks_used
    AzFunc-->>User: JSON {naked_truth, ats_match, cards[20], similar_occupations, privacy}
    Note over User: Total: 10–20 seconds end-to-end
```

---

## Azure Services — Complete Integration Map

| Azure Service | Tier | Region | Role in Platform | API Version |
|---|---|---|---|---|
| **Azure Functions v2** | Consumption (serverless) | East US | All 10 API endpoints · Python 3.12 · auto-scale | v2 decorator |
| **Azure OpenAI** | gpt-4o-mini | East US | 4 parallel AI calls per analysis · 8192 max tokens | 2024-08-01-preview |
| **Azure AI Search** | Standard S1 | East US | Semantic retrieval · 289 RAG chunks indexed · BM25 fallback | 2024-07-01 |
| **Azure Content Safety** | Standard v1.0 | East US | Input screening before every AI call · 4 categories · severity 4 threshold | 2024-09-01 |
| **Application Insights** | Pay-per-use | East US | Latency tracking · error alerts · chunk telemetry | v2 |
| **Azure Key Vault** | Standard | East US | All secrets · azure-identity managed identity · zero credentials in code | 2023-07-01 |
| **Azure Monitor** | Integrated | East US | Real-time alerts · dashboard · SLA tracking | — |

**Resource Group:** `rg-v3` · **Subscription:** Microsoft Hackathon `2d7fae20-e207-40a5-bc46-53df96affcb7`

---

## 20 Career Intelligence Tools — Execution Map

```mermaid
graph LR
    Input["Resume + JD + Country + Industry"]

    subgraph ZERO_AI["⚡ ZERO AI COST — Pure Python"]
        A1["01 Resume Score\n8 weighted dimensions"]
        A2["ATS Match %\nKeyword density"]
        A3["Similar Occupations\nISCO-08 RAG lookup"]
    end

    subgraph CALL1["Azure OpenAI Call 1"]
        B1["02 Recruiter POV\n6-sec skim simulation"]
        B2["03 Cover Letter\nTop-1% framework"]
        B3["04 Resume Rewrite\nImpact-first bullets"]
        B4["19 JD Template\nRole-specific JD"]
    end

    subgraph CALL2["Azure OpenAI Call 2"]
        C1["08 LinkedIn Summary\n150-220 words optimized"]
        C2["09 Intro Scripts\n1/2/3-min word-for-word"]
        C3["10 Thank You Email\nSubject + full body"]
        C4["11 Salary Negotiation\nTable + anchor scripts"]
    end

    subgraph CALL3["Azure OpenAI Call 3"]
        D1["12 30-60-90 Action Plan\nOnboarding milestones"]
        D2["13 Cold Outreach\nLinkedIn DM + email"]
        D3["14 Career Pivot\nPivot score + roadmap"]
        D4["15 Country Laws\nLabor law + compliance"]
        D5["16 Visa Pathways\nAll routes + govt URLs"]
        D6["17 Matching Jobs\nTitles + companies + boards"]
    end

    subgraph CALL4["Azure OpenAI Call 4"]
        E1["05 Skills Gap\nMatched + missing + certs"]
        E2["06 Interview Prep\n5 full STAR Q&As"]
        E3["07 STAR Stories\n3 metrics-driven examples"]
    end

    subgraph LIVE["🌐 Live API"]
        F1["20 Live Job Openings\nRemotive API · last 7 days"]
    end

    Input --> ZERO_AI
    Input --> CALL1 & CALL2 & CALL3 & CALL4
    Input --> LIVE
```

---

## RAG Knowledge Engine — 35 Files · 289 Chunks

```mermaid
graph TB
    subgraph CAREER["📁 data/career/ — 32 files"]
        C1["occupations-isco08-complete.md\noccupations-master-isco08-all.md\n436 ISCO-08 groups"]
        C2["countries-195-complete.md\ncountries-top-30.md\n195 UN country packages"]
        C3["visa-immigration-195-countries.md\ngovernment-immigration-portals.md\nAll visa routes + govt URLs"]
        C4["certifications-2026.md\ntraining-certifications-global.md\nAll-industry certs A-Z"]
        C5["global-salary-data.md\nsalary-trends-global-2026.md\nMarket salary benchmarks"]
        C6["skills-az-master.md\nsoft-hard-skills-matrix-2026.md\n900+ skills matrix"]
        C7["top-1-percent-framework.md\nresume-best-practices-2026.md\nTop recruiter methodology"]
        C8["future-occupations-2026-2125.md\nindustry-trends-2026-global.md\nEmerging roles + trends"]
        C9["interview-preparation.md\nnegotiation-scripts-word-by-word.md\ncold-outreach-templates.md"]
        C10["ats-scoring-guide.md\nrejection-reasons-database.md\njob-description-templates-100.md"]
        C11["linkedin-optimization-guide.md\ncareer-roadmap-templates.md\nhidden-job-market-2026.md"]
        C12["career-guide-youth-5-to-18.md\ncareer-guide-seniors-55-plus.md\ncareer-guide-accessibility-disability.md"]
        C13["global-platforms-tools-companies.md\ncompetitor-platforms-keywords.md\ncurrency-conversion-195.md\njob-market-challenges-2026.md"]
    end

    subgraph COMPLIANCE["📁 data/compliance/ — 3 files"]
        D1["data-retention-policy.md\nhipaa-compliance.md\nincident-response-sop.md"]
    end

    subgraph INDEX["🔍 Azure AI Search Index: career-knowledge"]
        IDX["289 chunks indexed\nBM25 + semantic retrieval\ntop-k=7 per query\nLocal BM25 fallback"]
    end

    CAREER --> INDEX
    COMPLIANCE --> INDEX
```

**Data Standards:** ILO ISCO-08 · European Commission ESCO v1.2 · US O*NET · Statistics Canada NOC 2021

---

## Security Architecture

```mermaid
graph TB
    subgraph GATES["3-Gate Safety Pipeline"]
        G1["Gate 1: INPUT\nAzure Content Safety\nHate · Violence · SelfHarm · Sexual\nSeverity threshold: 4"]
        G2["Gate 2: RETRIEVAL\nRAG Grounding\nAI writes only what knowledge base confirms\nFaithfulness score tracked"]
        G3["Gate 3: OUTPUT\nSource citations mandatory\nHallucination detection\nPII warning on query responses"]
    end

    subgraph INFRA["Infrastructure Security"]
        S1["Azure Key Vault\nAll secrets via managed identity\nZero credentials in code"]
        S2["RBAC\nLeast-privilege access\nReader on subscription\nContributor on rg-v3"]
        S3["Input Validation\n45,000 char resume limit\n5MB file upload limit\nAllowed types: PDF/DOCX/TXT/MD/CSV"]
        S4["Rate Limiting\n300 req/hr server-side\nIP-based tracking"]
    end

    subgraph PRIVACY["Privacy by Architecture"]
        P1["Zero Database\nNo resume stored\nNo PII retained\nRefresh = gone forever"]
        P2["Zero Cookies\nNo tracking\nNo behavioral profiling\nNo third-party analytics"]
        P3["In-Memory Only\nFile extracted → analyzed → discarded\nNo temp files written to disk"]
    end

    G1 --> G2 --> G3
```

---

## CI/CD Pipeline

```
Push to main (GitHub)
        │
        ▼
GitHub Actions (ubuntu-latest)
        ├── actions/checkout@v4
        ├── actions/setup-python@v5 (Python 3.12)
        ├── pip install -r requirements.txt --target=.python_packages/lib/site-packages
        ├── Azure/functions-action@v1
        │     app-name: govrag-v3-func
        │     publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
        │     scm-do-build-during-deployment: true
        │     enable-oryx-build: true
        └── Health check: GET /api/health (30s warm-up)

Deploy time: ~2 minutes · Zero downtime · Serverless swap
```

---

## Performance Targets

| Metric | Target | Actual (observed) |
|--------|--------|-------------------|
| End-to-end analysis | < 15 seconds | 10–20 seconds |
| Content Safety check | < 500ms | ~200ms |
| RAG retrieval (Azure AI Search) | < 200ms | ~150ms |
| Single Azure OpenAI call | < 8 seconds | 5–12 seconds |
| File upload + extraction | < 2 seconds | < 1 second |
| Cold start (serverless) | < 3 seconds | ~2 seconds |
| Platform uptime | 99.9% (Azure SLA) | Azure guaranteed |

---

## Repository Structure

```
shahzadms7/v3/
├── function_app.py              # Azure Functions v2 — all 10 endpoints (887 lines)
├── host.json                    # routePrefix: "" · Extension Bundle 4.*
├── requirements.txt             # Python dependencies (lean — no heavy ML)
├── web.config                   # Azure routing rules
│
├── app/core/
│   ├── career_engine.py         # Resume parser + ATS scorer (zero AI cost)
│   ├── decision_engine.py       # Full career decision algorithm
│   ├── ai_provider.py           # Azure OpenAI async client
│   ├── rag_engine.py            # Local BM25 search fallback
│   ├── safety_engine.py         # Azure Content Safety wrapper
│   ├── azure_ai_services.py     # PII detection, key phrases, translation
│   ├── audit_logger.py          # Application Insights telemetry
│   └── config.py                # pydantic-settings from env vars
│
├── data/
│   ├── career/                  # 32 Markdown knowledge files
│   └── compliance/              # 3 compliance reference files
│
├── static/
│   └── index.html               # Single-page frontend (HTML/CSS/Vanilla JS)
│
├── docs/
│   ├── RESPONSIBLE_AI_IMPACT_ASSESSMENT.md
│   ├── TRANSPARENCY_NOTE.md
│   └── screenshots/             # Platform screenshots
│
└── .github/workflows/
    └── main_govrag-v3.yml       # CI/CD: GitHub → Azure Functions
```

---

<div align="center">

*Alfalah AI · 100% Microsoft Azure · East US · rg-v3*

**[Live Platform](https://govrag-v3-func.azurewebsites.net) · [API Health](https://govrag-v3-func.azurewebsites.net/api/health) · [GitHub](https://github.com/shahzadms7/v3)**

</div>
