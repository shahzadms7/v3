# Alfalah AI — Career Intelligence Platform

> **الفلاح** · "Come to Success" · Free AI career guidance for 8 billion people worldwide

<div align="center">

[![Azure Functions](https://img.shields.io/badge/Azure_Functions_v2-Python_3.12-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/products/functions)
[![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-gpt--4o--mini-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/products/ai-services/openai-service)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python_3.12-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)

**Live:** https://govrag-v3-func.azurewebsites.net &nbsp;|&nbsp; **API Health:** https://govrag-v3-func.azurewebsites.net/api/health

</div>

---

## Overview

Alfalah AI is a **free, zero-login, zero-storage** AI career intelligence platform built entirely on Microsoft Azure. It delivers 20 specialized career intelligence tools to professionals across all 195 UN-recognized countries — powered by Azure OpenAI and grounded in structured career science from ISCO-08, ESCO, and ILO.

**No subscription. No account. No data retained. Built for the 8 billion.**

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Microsoft Azure Cloud                    │
│                                                             │
│  Browser  ──►  Azure Functions v2 (Python 3.12)            │
│                        │                                   │
│              ┌─────────┼──────────┐                        │
│              ▼         ▼          ▼                        │
│         Azure OpenAI  Azure AI  Azure Content              │
│         gpt-4o-mini   Search    Safety                     │
│              │         │                                   │
│         4 parallel  289 RAG    Input screening             │
│         AI calls    chunks     (hate/violence)             │
│              └─────────┴──────────┘                        │
│                        │                                   │
│              Application Insights · Key Vault              │
└─────────────────────────────────────────────────────────────┘
```

---

## Azure Services

| Service | Configuration | Purpose |
|---------|--------------|---------|
| **Azure Functions v2** | Python 3.12 · Consumption plan | Serverless API — 15 endpoints, auto-scales to zero |
| **Azure OpenAI** | gpt-4o-mini · eastus | 4 parallel AI calls per analysis (20 tools in ~15s) |
| **Azure AI Search** | Standard tier · 289 RAG chunks | Semantic search over career knowledge base |
| **Azure Content Safety** | v1.0 | Input screening before every AI call |
| **Azure Static Web Apps** | Free tier · CDN | Frontend HTML/CSS/JS global delivery |
| **Application Insights** | Connected to Functions | Real-time telemetry, error tracking, latency |
| **Azure Key Vault** | Standard tier | All API keys and connection strings |

**Resource Group:** `rg-v3` · **Subscription:** `2d7fae20-e207-40a5-bc46-53df96affcb7` · **Region:** East US

---

## 20 Career Intelligence Tools

All tools execute in parallel across 4 Azure OpenAI calls — results in 10–20 seconds.

| # | Tool | Output |
|---|------|--------|
| 01 | Resume Score | ATS score 0–100 across 8 weighted dimensions |
| 02 | Recruiter Perspective | 6-second hiring manager skim simulation |
| 03 | Skills Gap Analysis | Hard/soft skills matched + cert roadmap |
| 04 | Resume Rewrite | Impact-first bullets with metrics |
| 05 | Cover Letter | 3-paragraph, role-specific, quantified wins |
| 06 | Interview Preparation | 5 Q&A with STAR answers + questions to ask |
| 07 | STAR Stories | 3 behavioural stories with metrics |
| 08 | LinkedIn Summary | Keyword-optimised About section |
| 09 | Introduction Scripts | 1-min / 2-min / 3-min verbal intros |
| 10 | Thank You Email | Post-interview follow-up with subject line |
| 11 | Salary Negotiation | Table by level + anchor scripts |
| 12 | 30-60-90 Day Plan | Structured onboarding milestones |
| 13 | Cold Outreach | LinkedIn DM + cold email + follow-up |
| 14 | Career Pivot | Difficulty score + 3 adjacent roles + 90-day plan |
| 15 | Labour Law | Country-specific notice, termination, non-compete |
| 16 | Visa Pathways | In-country + all immigration routes with govt URLs |
| 17 | Matching Jobs | Titles + companies + job boards + recruiters |
| 18 | Similar Occupations | ISCO-08 adjacent roles |
| 19 | JD Template | Professional job description for the role |
| 20 | Live Job Openings | Real-time listings from Remotive |

---

## API Reference

**Base URL:** `https://govrag-v3-func.azurewebsites.net`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Platform status, RAG chunks loaded, Azure services |
| `POST` | `/career` | Full 20-tool career analysis |
| `POST` | `/upload` | Extract text from PDF / DOCX / TXT |
| `POST` | `/query` | Grounded RAG question-answer |
| `POST` | `/decision` | Algorithmic career decision (zero AI cost) |
| `POST` | `/search-jobs` | Live job listings via Remotive |
| `GET` | `/responsible-ai` | Responsible AI principles and data handling |

**POST /career — Request:**
```json
{
  "resume": "Full resume text (max 45,000 chars)",
  "job_description": "Job description (max 10,000 chars)",
  "country": "Canada",
  "industry": "IT"
}
```

---

## Knowledge Base (RAG)

| Source | Content | Chunks |
|--------|---------|--------|
| ISCO-08 | 436 international occupational groups | ~80 |
| ESCO | 3,000+ European job classifications | ~40 |
| Future Occupations | Emerging roles 2026–2125 | ~30 |
| Country Packages | 195 UN countries — salary, visa, labour law | ~60 |
| Certifications | All-industry certs A–Z with URLs | ~30 |
| Companies | 500+ top employers by country with career URLs | ~25 |
| Top-1% Framework | Recruiter science and ATS methodology | ~10 |
| Global Intelligence | Salary data, hiring trends, platforms | ~14 |
| **Total** | | **289 chunks** |

All files stored in `data/career/` as Markdown. Indexed automatically into Azure AI Search on first request.

---

## Repository Structure

```
/
├── function_app.py          # Azure Functions v2 app — all 15 endpoints
├── host.json                # Azure Functions runtime config (routePrefix: "")
├── requirements.txt         # Python dependencies
├── web.config               # IIS/Azure routing rules
├── app/
│   └── core/
│       ├── career_engine.py     # Resume parser + ATS scorer (zero AI cost)
│       ├── decision_engine.py   # Full career decision algorithm
│       ├── rag_engine.py        # Local BM25 search fallback
│       ├── ai_provider.py       # Azure OpenAI client
│       ├── safety_engine.py     # Content safety wrapper
│       └── config.py            # Centralised settings (env vars)
├── data/
│   ├── career/              # Career knowledge base (Markdown)
│   └── compliance/          # Compliance documents (Markdown)
├── static/
│   └── index.html           # Single-page frontend (HTML/CSS/JS)
├── docs/
│   ├── RESPONSIBLE_AI_IMPACT_ASSESSMENT.md
│   └── TRANSPARENCY_NOTE.md
└── .github/
    └── workflows/
        └── main_govrag-v3.yml   # CI/CD — GitHub Actions → Azure Functions
```

---

## CI/CD

Push to `main` → GitHub Actions automatically deploys to Azure Functions.

```yaml
# .github/workflows/main_govrag-v3.yml
- Set up Python 3.12
- pip install -r requirements.txt
- Azure/functions-action@v1  (publish profile from GitHub Secrets)
- Health check: /api/health
```

**Deploy time:** ~2 minutes · **Zero downtime** (serverless swap)

---

## Local Development

```bash
# Prerequisites: Python 3.12, Azure Functions Core Tools v4
git clone https://github.com/shahzadms7/v3
cd v3

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Azure credentials

# Run locally
func start

# Test
curl http://localhost:7071/api/health
```

**Required environment variables:**

| Variable | Description |
|----------|-------------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name (default: `gpt-4o-mini`) |
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search endpoint |
| `AZURE_SEARCH_KEY` | Azure AI Search admin key |
| `AZURE_CONTENT_SAFETY_ENDPOINT` | Content Safety endpoint |
| `AZURE_CONTENT_SAFETY_KEY` | Content Safety key |

---

## Privacy & Responsible AI

- **Zero storage** — no database, no logs of resume content
- **Zero PII retained** — all data processed in-memory, discarded after response
- **Content Safety** — every input screened by Azure Content Safety before AI processing
- **Transparency** — every AI response cites RAG sources and confidence scores
- **Fairness** — identical analysis for all 195 countries, no demographic data collected

Full assessment: [docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md](./docs/RESPONSIBLE_AI_IMPACT_ASSESSMENT.md)

---

## Built With

| Tool | Role |
|------|------|
| Microsoft Azure | 100% cloud infrastructure |
| Azure OpenAI (gpt-4o-mini) | Career intelligence generation |
| Azure AI Search | Semantic knowledge retrieval |
| Python 3.12 | Backend runtime |
| GitHub Actions | CI/CD automation |
| Claude Sonnet 4.6 | Development assistant (Claude Code) |

---

## Hackathon

**Microsoft AI Skills Challenge — March 2026**
Built in 30 sessions. Submitted March 26, 2026.

---

*Alfalah AI · Mississauga, Ontario, Canada · [GitHub](https://github.com/shahzadms7/v3)*
