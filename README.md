# 🏛️ GovRAG V3 — Grounded Knowledge Assistant for Regulated Teams + Career Intelligence

<p align="center">
  <strong>A governed RAG system that answers compliance-critical questions AND serves as a career intelligence platform for 8 billion humans</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/100%25-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/100%25-Azure%20Cloud-0078D4?logo=microsoftazure&logoColor=white" alt="Azure">
  <img src="https://img.shields.io/badge/Microsoft-Hackathon%202026-purple" alt="Hackathon">
  <img src="https://img.shields.io/badge/Zero-Data%20Storage-green" alt="Privacy">
  <img src="https://img.shields.io/badge/Responsible-AI-orange" alt="RAI">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="MIT">
</p>

---

## The Problem — Why This Matters

### For Regulated Teams (Legal, Compliance, Finance, Healthcare)
Every day, **compliance teams** waste hours searching through policies, contracts, and SOPs for answers. When they use generic AI chatbots:
- **75% risk** of hallucinated answers that could violate regulations
- **Zero traceability** — can't prove where an answer came from
- **No audit trail** — no record for regulators
- **One wrong answer** in healthcare or finance can cost **millions in fines**

### For 8 Billion Humans Searching for Jobs
- **75% of resumes** are rejected by ATS before a human sees them
- **87 million workers** need reskilling by 2030 (World Economic Forum)
- Workers **45+** take 46% longer to find jobs (age discrimination)
- Career advice is expensive ($50-150/month) and often generic
- Visa and immigration pathways are confusing across **195 countries**

### Our Answer: GovRAG
**One platform. Two missions. Zero hallucinations.**

---

## What is GovRAG?

GovRAG is a **governed Retrieval-Augmented Generation (RAG) system** that:

1. **Answers questions** from internal documents (policies, contracts, SOPs, career data)
2. **Cites every claim** with exact source references `[Source 1: document.md, Section 3.2]`
3. **Verifies faithfulness** — real-time score showing what % of the answer is grounded
4. **Blocks hallucinations** — answers below 40% confidence are automatically blocked
5. **Logs everything** — full audit trail for compliance teams (metrics only, never user data)
6. **Serves everyone** — free, no login, no data stored, works for compliance AND careers

---

## How It Works — Step by Step

```
┌──────────────────────────────────────────────────────────────────────┐
│                     USER ASKS A QUESTION                             │
│  "What is our data retention policy for EU customers?"               │
│  "Score my resume for this Azure cloud engineer position"            │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 1: INPUT SAFETY GATE                                           │
│  ✓ Check for prompt injection attacks                                │
│  ✓ Detect PII in query (SSN, credit cards) — warn, never store       │
│  ✓ Validate query length                                             │
│  ✗ If dangerous → BLOCK immediately                                  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ ✓ Safe
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 2: RETRIEVE (Search Documents)                                 │
│  • Search 74+ document chunks using TF-IDF / Azure AI Search         │
│  • Find top 5 most relevant paragraphs                               │
│  • Each chunk scored by relevance (0.0 to 1.0)                       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 3: RELEVANCE GATE                                              │
│  ✓ Do we have enough relevant sources?                               │
│  ✓ Is average relevance above threshold?                             │
│  ✗ If insufficient → Return "I don't have enough info" (NOT guess)   │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ ✓ Relevant sources found
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 4: GENERATE (AI Creates Answer)                                │
│  • AI receives ONLY the retrieved chunks (not all documents)         │
│  • Strict instruction: "Answer ONLY from context, cite [Source N]"   │
│  • Multi-AI fallback: Gemini Key1 → Key2 → Grok                     │
│  • Returns JSON with answer + citations + confidence                 │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 5: VERIFY FAITHFULNESS                                         │
│  • Check each sentence: is it grounded in a source?                  │
│  • Calculate faithfulness score: grounded_claims / total_claims       │
│  • Example: "5 out of 6 claims grounded = 83% faithful"              │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 6: CONFIDENCE GATE                                             │
│  • Below 40% → BLOCK (too risky to show)                             │
│  • Below 70% → WARN (show with disclaimer)                           │
│  • Above 70% → ALLOW (trusted answer)                                │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 7: AUDIT LOG                                                   │
│  • Log: timestamp, confidence%, faithfulness%, sources count, latency │
│  • NEVER log: user query text, resume content, any PII               │
│  • Sent to Azure Monitor for production observability                │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 8: RESPOND TO USER                                             │
│  ✅ Grounded answer with [Source N] citations                        │
│  ✅ Faithfulness score (e.g., 92%)                                   │
│  ✅ Confidence score (e.g., 85%)                                     │
│  ✅ Clickable source previews                                        │
│  ✅ Warnings if any                                                  │
│  ✅ Audit ID for compliance tracking                                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Core RAG System
| Feature | Description |
|---------|-------------|
| **Source-Grounded Answers** | Every sentence cites `[Source N]` — click to see exact paragraph |
| **3-Gate Safety Pipeline** | Input safety → Relevance gate → Confidence threshold |
| **Real-time Faithfulness Score** | 0-100% — what percentage of claims are verified in sources |
| **Multi-AI Resilience** | Gemini Key1 → Key2 → Grok fallback (enterprise pattern) |
| **Full Audit Trail** | Every query logged with metrics (never PII) |
| **Dual Domain** | Compliance mode (policies/SOPs) + Career mode (resume/jobs/skills) |

### Killer Feature 1: "Explain Like Zara" (ELI12 Mode)
*Inspired by the Cognitive Load Reduction challenge*

Any complex compliance or career answer can be simplified to adjustable reading levels:
- **Grade 3** — For an 8-year-old
- **Grade 6** — For a 12-year-old (Zara's level)
- **Grade 9** — For a high schooler
- **Adult** — Plain language, no jargon

Uses calm, supportive, non-anxiety-inducing language. Because compliance should be understandable by everyone.

### Killer Feature 2: "Why These Sources?" Explainability
*Inspired by the Lab Notebook AI Assistant challenge*

Every answer comes with a transparency panel:
- **Why** each source was selected (keyword overlap, relevance score)
- **What terms** matched between your question and the document
- **How** the search worked (method, index size, threshold)
- Full retrieval reasoning visible to the user

### Killer Feature 3: Responsible AI Transparency Card
*Referenced in 4 out of 5 hackathon challenges*

A dedicated endpoint (`/api/responsible-ai`) returns our full compliance with Microsoft's 6 Responsible AI principles:
- **Fairness** — No demographic data, uniform treatment
- **Reliability & Safety** — 3-gate pipeline, multi-AI fallback
- **Privacy & Security** — Zero storage, PII detection
- **Inclusiveness** — ELI12 mode, free for all, no login
- **Transparency** — Source citations, explainability, open source
- **Accountability** — Audit trail, safety verdicts, Azure Monitor

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure Resource Group: rg-v3                   │
│                                                                  │
│  ┌──────────────┐    ┌───────────────────────────────────────┐  │
│  │ Azure App    │    │  Python Application (100% Python)      │  │
│  │ Service (F1) │    │  ┌─────────┐ ┌──────────┐ ┌────────┐ │  │
│  │ FREE tier    │───▶│  │ FastAPI │ │Streamlit │ │  RAG   │ │  │
│  │ Python 3.12  │    │  │  API    │ │   UI     │ │ Engine │ │  │
│  └──────────────┘    │  └────┬────┘ └──────────┘ └───┬────┘ │  │
│                      │       │                        │       │  │
│                      │  ┌────▼────────────────────────▼────┐ │  │
│                      │  │  Core Engine                      │ │  │
│                      │  │  • AI Provider (Gemini + Grok)    │ │  │
│                      │  │  • Safety Engine (3 gates)        │ │  │
│                      │  │  • Audit Logger (metrics only)    │ │  │
│                      │  │  • TF-IDF Index (in-memory)       │ │  │
│                      │  └──────────────────────────────────┘ │  │
│                      └───────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Azure Blob   │  │ Azure Key    │  │ Azure Monitor        │  │
│  │ Storage      │  │ Vault        │  │ + App Insights       │  │
│  │ (documents)  │  │ (secrets)    │  │ (audit trail)        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌──────────────┐
  │ GitHub       │
  │ CI/CD        │
  │ (auto-deploy)│
  └──────────────┘
```

---

## Azure Services Used

| Service | Purpose | Tier | Cost |
|---------|---------|------|------|
| **App Service** | Host Python application | F1 (Free) | $0 |
| **Blob Storage** | Document file storage | Standard LRS | ~$0.50/mo |
| **Key Vault** | Secrets management | Standard | ~$0.03/mo |
| **AI Search** | Production RAG retrieval | Free | $0 |
| **Monitor + App Insights** | Audit trail + observability | Free 5GB | $0 |
| **TOTAL** | | | **~$0.53/month** |

---

## Tech Stack — 100% Python

| Layer | Technology | Lines | Why |
|-------|-----------|-------|-----|
| Backend API | **FastAPI** | ~350 | Fastest Python framework, auto-docs at `/docs` |
| Frontend UI | **Streamlit** | ~250 | 100% Python, beautiful dashboards, zero JS |
| RAG Engine | **Custom** (TF-IDF + Azure AI Search) | ~200 | Hybrid search, source grounding |
| Safety Engine | **Custom** (3-gate pipeline) | ~150 | Input, relevance, confidence gates |
| AI Provider | **Gemini + Grok** (multi-fallback) | ~130 | Free tier, enterprise resilience |
| Audit Logger | **Custom** (Azure Monitor) | ~100 | Metrics only, zero PII |
| Config | **Pydantic Settings** | ~60 | Type-safe, env-var driven |
| **TOTAL** | **100% Python** | **~1,240** | Production-grade in under 1,300 lines |

---

## Document Knowledge Base

### Compliance Documents (for regulated teams)
| Document | What It Covers |
|----------|---------------|
| `data-retention-policy.md` | Enterprise data retention schedules, GDPR, disposal rules |
| `hipaa-compliance.md` | Healthcare PHI protection, breach notification, penalties |
| `incident-response-sop.md` | Security incident procedures, severity levels, regulatory notification |

### Career Intelligence (for 8 billion humans)
| Document | What It Covers |
|----------|---------------|
| `global-salary-data.md` | Salary by role, country, experience level (2026 data) |
| `certifications-2026.md` | Professional certifications A-Z with cost, validity, URLs |
| `countries-top-30.md` | Top 30 job markets: GDP, visa, job boards, top employers |
| `job-market-challenges-2026.md` | 10 challenges humanity faces in job search globally |
| `resume-best-practices-2026.md` | ATS optimization, STAR method, 2026 resume trends |
| `ats-scoring-guide.md` | How ATS systems actually work, scoring algorithms |
| `interview-preparation.md` | Top 20 behavioral questions, formats by industry, salary negotiation |

---

## API Endpoints

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/api/query` | POST | Ask a grounded question (compliance or career) |
| `/api/career/analyze` | POST | Resume analysis with RAG-grounded intelligence |
| `/api/simplify` | POST | **ELI12** — Simplify any text to adjustable reading level |
| `/api/explain` | POST | **Why These Sources?** — Retrieval explainability |
| `/api/responsible-ai` | GET | **RAI Card** — Full Responsible AI compliance posture |
| `/api/health` | GET | Health check for Azure Monitor |
| `/api/metrics` | GET | Audit dashboard metrics |
| `/api/sources` | GET | List all indexed documents |
| `/docs` | GET | Swagger API documentation (auto-generated) |

---

## For Non-Technical Users — How to Use GovRAG

### If you're a compliance officer:
1. Open the GovRAG website
2. Select **"Compliance"** mode
3. Type your question: *"What is our data retention policy for EU customers?"*
4. Click **"Get Grounded Answer"**
5. Read the answer — every fact has a `[Source]` tag you can click to verify
6. Check the **Faithfulness Score** (green = trustworthy, yellow = verify, red = unreliable)
7. That's it! Your question was never saved. Close the browser = data gone.

### If you're a job seeker:
1. Open the GovRAG website
2. Select **"Career Intelligence"** mode
3. Go to **"Career Analyzer"** tab
4. Paste your resume
5. Optionally paste a job description you're targeting
6. Select your country and industry
7. Click **"Analyze Resume"**
8. Get: Score (0-100), strengths, weaknesses, missing skills, recommended certifications, action items
9. Everything cited from real career intelligence data
10. Your resume was **NEVER stored**. Privacy first.

### If you don't understand the answer:
1. Click **"Explain Like Zara"** (ELI12 mode)
2. Choose your reading level (Grade 3 to Adult)
3. Get the same answer in simple, everyday words
4. No jargon, no anxiety, no confusion

---

## Benefits

### For Organizations
- **Reduce compliance risk** — Every answer traceable to source documents
- **Save hours daily** — Instant answers vs. manual document searching
- **Audit-ready** — Full trail of every question asked and answered
- **Zero data liability** — Nothing stored, nothing to breach

### For Job Seekers
- **Free forever** — No subscription, no login, no paywall
- **Global coverage** — 195 countries, salary data, visa pathways
- **Honest feedback** — Not flattering, but truthful resume scoring
- **Actionable** — Every weakness comes with a specific fix
- **Private** — Your resume is NEVER stored anywhere

### For Judges & Evaluators
- **Source grounding** — Every claim cites exact document and section
- **Hallucination metrics** — Real-time faithfulness score on every response
- **Safety pipeline** — 3-gate validation, not just prompt engineering
- **Responsible AI** — Full RAI card aligned to Microsoft's 6 principles
- **Production path** — Azure infrastructure, CI/CD, monitoring, audit trail
- **Clean code** — ~1,300 lines of Python, fully documented

---

## Evaluation Metrics

| Metric | What It Measures | Target | How We Measure |
|--------|-----------------|--------|----------------|
| **Faithfulness** | % of claims grounded in sources | > 90% | Automated per-response |
| **Answer Relevance** | Does answer address the question? | > 85% | AI confidence score |
| **Context Precision** | Are retrieved chunks relevant? | > 80% | TF-IDF cosine similarity |
| **Hallucination Rate** | % of ungrounded claims | < 5% | 100% - faithfulness |
| **Latency** | End-to-end response time | < 5 sec | Measured per request |
| **Block Rate** | % of unsafe/uncertain queries blocked | Tracked | Safety engine logs |

---

## Privacy & Security

```
┌────────────────────────────────────────────────────┐
│              ZERO DATA STORAGE                      │
│                                                     │
│  ✅ No database (no SQL, no NoSQL, no Redis)       │
│  ✅ No user accounts (no login, no registration)    │
│  ✅ No cookies tracking users                       │
│  ✅ No analytics tracking individuals               │
│  ✅ Resume/query lives ONLY in memory               │
│  ✅ After response → data permanently erased        │
│  ✅ Refresh browser = clean slate                   │
│  ✅ Audit logs contain metrics ONLY (never PII)     │
│  ✅ PII detection in queries AND responses          │
│  ✅ Prompt injection detection and blocking          │
│  ✅ TLS 1.2 encryption in transit                   │
│  ✅ API keys in Azure Key Vault (production)        │
│  ✅ GDPR compliant by design (nothing to delete)    │
│  ✅ HIPAA consideration (no PHI persisted)          │
└────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.10+ (we use 3.12)
- Git

### Run Locally (2 minutes)
```bash
# Clone
git clone https://github.com/shahzadms7/v3.git
cd v3

# Install dependencies
pip install -r requirements.txt

# Set up environment (create .env file with your API keys)
cp api/.env.example .env
# Edit .env with your Gemini and/or Grok keys

# Start API server
uvicorn app.api.main:app --reload --port 8000

# In another terminal, start Streamlit UI
streamlit run app/ui/streamlit_app.py
```

### Test the API
```bash
# Health check
curl http://localhost:8000/api/health

# Ask a question
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our data retention policy for EU customers?"}'

# See API docs
open http://localhost:8000/docs
```

---

## Project Structure

```
v3/
├── .github/workflows/       # CI/CD: test → security scan → deploy
│   └── deploy.yml
├── app/                     # Application code (100% Python)
│   ├── api/
│   │   └── main.py          # FastAPI — 8 endpoints, all logic
│   ├── core/
│   │   ├── config.py        # Central settings (Pydantic)
│   │   ├── ai_provider.py   # Multi-AI: Gemini → Grok fallback
│   │   ├── rag_engine.py    # RAG: retrieve, ground, verify
│   │   ├── safety_engine.py # 3-gate safety pipeline
│   │   └── audit_logger.py  # Audit trail (metrics only, no PII)
│   └── ui/
│       └── streamlit_app.py # Streamlit frontend (3 tabs)
├── data/
│   ├── career/              # 7 career intelligence documents
│   └── compliance/          # 3 compliance documents
├── requirements.txt         # Python dependencies
├── startup.sh              # Azure App Service startup
└── README.md               # This file
```

---

## Roadmap: PoC → Pilot → Production

| Phase | Scope | Status |
|-------|-------|--------|
| **PoC** (Hackathon) | 10 docs, single instance, TF-IDF search, free AI | ✅ Built |
| **Pilot** | 100+ docs, Azure AI Search, vector embeddings, RBAC | 📋 Planned |
| **Production** | Multi-tenant, SSO, compliance dashboard, SLA 99.9% | 📋 Future |

### Production Evolution Path
- Replace TF-IDF with **Azure AI Search semantic ranking** (already integrated)
- Add **Azure OpenAI** with managed identity (zero keys in code)
- Add **Entra ID B2C** for enterprise SSO
- Add **Azure API Management** for rate limiting and analytics
- Add **Cosmos DB** for enterprise audit trail (with TTL auto-delete)
- Add **Azure Front Door** for global CDN and WAF

---

## Team

| Role | Name | Contribution |
|------|------|-------------|
| **Principal Solution Architect** | Shahzad Muhammad | Architecture, Azure, GRC compliance, vision |
| **AI Engineering** | Claude Opus 4.6 | Full-stack development, RAG engine, safety system |
| **Student Learner** | Zara (age 12) | Testing ELI12 mode, learning Azure + AI step by step |

---

## Built With

- **Python 3.12** — 100% Python, every line
- **FastAPI** — Backend API framework
- **Streamlit** — Frontend UI framework
- **Google Gemini** — Primary AI (free tier)
- **xAI Grok** — Fallback AI (free tier)
- **Azure App Service** — Hosting (free tier)
- **Azure Blob Storage** — Document storage
- **Azure Key Vault** — Secrets management
- **Azure Monitor** — Observability
- **GitHub Actions** — CI/CD pipeline
- **scikit-learn** — TF-IDF vectorization

---

## References

- [Microsoft Responsible AI Toolbox](https://github.com/microsoft/responsible-ai-toolbox)
- [WCAG 2.2 Accessibility Guidelines](https://www.w3.org/TR/WCAG22/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence)

---

## License

MIT License — Free for all humanity.

---

<p align="center">
  <strong>Built with 💙 for the Microsoft Hackathon 2026</strong><br>
  <em>Shahzad Muhammad · Mississauga, Ontario, Canada</em><br>
  <em>Serving all 8 billion humans — East to West</em>
</p>
