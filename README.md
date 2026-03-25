# Alfalah AI — Career Intelligence Platform

**A free, AI-powered career platform serving professionals across 195 countries.**

No account required. No data stored. No cost. Built entirely on Microsoft Azure.

---

## Live Deployment

| | |
|-|-|
| Platform | Microsoft Azure — Canada East |
| Frontend | Azure Static Web Apps |
| Backend | Azure Functions (Python v2) |
| AI | Azure OpenAI (GPT-4o-mini) |
| Repository | github.com/shahzadms7/v3 |

---

## What It Does

Alfalah AI analyzes a professional's resume and job description, then produces **17 career intelligence reports** using a grounded knowledge engine — 99% structured career data, 1% Azure OpenAI for final formatting.

**Zero hallucination. Zero guessing. Grounded in authoritative career science.**

---

## 17 Career Intelligence Modules

| # | Module | Output |
|---|--------|--------|
| 1 | Resume Score | ATS algorithm score across 8 weighted dimensions |
| 2 | Recruiter POV | 6-second hiring manager scan — what gets noticed, what gets missed |
| 3 | Cover Letter | Role-specific, quantified, top-1% quality |
| 4 | Resume Rewrite | Diagnosis → win extraction → impact-first restructure |
| 5 | Skills Gap | Matched and missing skills + certifications with official URLs |
| 6 | Interview Prep | Behavioral and technical Q&A + questions to ask the interviewer |
| 7 | STAR Stories | 3 metrics-driven behavioral examples |
| 8 | LinkedIn Summary | Search-optimized About section |
| 9 | Intro Scripts | 1, 2, and 3-minute professional introductions |
| 10 | Matching Jobs | Titles, companies, boards, recruiters across 7 countries |
| 11 | Visa Pathways | In-country and cross-border immigration routes + official government URLs |
| 12 | Thank You Email | Post-interview follow-up that differentiates the candidate |
| 13 | Salary Negotiation | Market salary table (Entry to Executive) in local currency + scripts |
| 14 | Action Plan | 30-60-90 day structured career plan |
| 15 | Cold Outreach | LinkedIn DM, cold email, and follow-up templates |
| 16 | Career Pivot | Adjacent role analysis + 90-day transition roadmap |
| 17 | Country Laws | Labor law, worker rights, ATS compliance by country |

**Plus:**
- Similar occupations based on ISCO-08 classification
- Job description templates for the analyzed role
- Live job postings (Google Jobs, last 7 days, country-specific)
- Top 1% hiring framework insights (how Google, Amazon, Microsoft screen candidates)

---

## Azure Architecture

```
User Browser
    │
    ▼
Azure Static Web Apps (Global CDN)
    │
    ▼
Azure Functions v2 — Python (Serverless)
    ├── POST /career       — 17-module analysis
    ├── POST /chat         — Career coaching conversation
    ├── POST /jobs         — Live job search via Serper API
    ├── GET  /location     — IP geolocation
    ├── GET  /health       — System health
    └── POST /upload       — Secure file extraction (PDF/DOCX/TXT)
    │
    ├── Azure OpenAI (GPT-4o-mini) — Primary AI
    ├── Azure Key Vault — All secrets managed
    ├── Azure AI Search — Semantic retrieval
    └── RAG Knowledge Base (structured .md files)
         ├── 436 ISCO-08 occupations with JDs, skills, salary, AI risk
         ├── 195 country packages (laws, salary, visa, ATS norms)
         ├── 900+ skills A-Z (hard, soft, future)
         ├── Future occupations 2026–2125
         ├── Top 1% hiring framework
         ├── Global companies + tools A-Z
         └── 21 additional career intelligence files
```

**AI Fallback Chain:**
Azure OpenAI → Google Gemini (KEY1 → KEY2) → xAI Grok

---

## Knowledge Base

| File | Coverage |
|------|----------|
| `occupations-master-isco08-all.md` | All 436 ISCO-08 groups — tasks, skills, salary, AI risk, JD template |
| `skills-az-master.md` | 500+ hard skills, 250+ soft skills, 150+ future skills A-Z |
| `future-occupations-2026-2125.md` | Emerging roles across 5 time horizons to 2125 |
| `top-1-percent-framework.md` | ATS algorithms, recruiter science, Google/Amazon/Microsoft hiring |
| `global-platforms-tools-companies.md` | Fortune 500 + all industry tools A-Z by region |
| `MASTER_CAREER_REFERENCE.md` | 640KB — salary, ATS, hiring norms across 195 countries |
| `COUNTRY_PACKAGES_195.md` | Per-country: salary, visa routes, labor law, job boards |
| `CERTIFICATIONS_2026.md` | All-industry certifications A-Z with official URLs |
| `COMPANIES_BY_COUNTRY.md` | Top employers + career URLs for 30+ countries |
| `GLOBAL_CAREER_INTELLIGENCE_2025.md` | Salary trends, ATS systems, job boards, market data |

---

## Occupation Coverage

| Standard | Count | Source |
|----------|-------|--------|
| ISCO-08 | 436 unit groups | ILO International Labour Organization |
| ESCO | 3,000+ occupations | European Commission |
| O*NET | 1,016 occupations | US Department of Labor |
| Global job titles | 123,000+ | Cross-referenced across frameworks |

Covers all 10 ISCO-08 major groups:
Managers · Professionals · Technicians · Clerical · Service & Sales · Agriculture · Trades · Plant & Machine · Elementary · Armed Forces

---

## Global Coverage

**Countries:** 195 UN-recognized nations with localized salary data, visa pathways, labor law, and recruiter norms.

**Companies:** Fortune 500 + top employers across North America, Europe, Middle East, Asia, South Asia, Africa, and Oceania — with direct career portal URLs.

**Tools & Platforms A-Z:**
Cloud (AWS, Azure, GCP), AI/ML (TensorFlow, PyTorch, Hugging Face), ERP (SAP, Oracle, Workday), DevOps (Docker, Kubernetes, Terraform), Data (Spark, Snowflake, dbt), Cybersecurity (Splunk, CrowdStrike), Healthcare (Epic, Cerner), Finance (Bloomberg, Murex), and 500+ more across every sector.

---

## Responsible AI

- **Privacy by design** — no resume stored, no PII collected, all analysis runs in memory
- **Grounded outputs** — responses cite structured data sources, not model inference alone
- **No demographic bias** — analysis based on skills, experience, and role requirements only
- **Transparent methodology** — ATS scoring algorithm dimensions are disclosed to the user
- **Azure Content Safety** — integrated moderation layer on all AI outputs
- **RBAC and Key Vault** — least-privilege access, all secrets managed in Azure Key Vault

---

## Running Locally

```bash
# Prerequisites: Python 3.11+, Azure Functions Core Tools v4
cd v3
pip install -r requirements.txt
func start
```

Environment variables (`.env.local` or Azure Key Vault):
```
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
GEMINI_API_KEY=
GEMINI_API_KEY_2=
GROK_API_KEY=
SERPER_API_KEY=
```

---

## Deploying to Azure

```bash
# Deploy function app directly
func azure functionapp publish govrag-v3-func

# Or push to main — GitHub Actions deploys automatically
git push origin main
```

---

## License

MIT — free to use, modify, and distribute.

---

*Alfalah AI · &copy; 2026 · Mississauga, Ontario, Canada*
