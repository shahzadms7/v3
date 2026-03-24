# Alfalah AI — الفلاح — "Come to Success"

> **Free AI-powered career tools for all 8 billion humans on Earth.**
> No login. No storage. No cost. No bias. No racism. No religion. No politics.
> Built on Azure Cloud — serving every country, every industry, every language.

---

## Live

| Version | URL | Status |
|---------|-----|--------|
| V2 (Demo locked) | https://shahzad-job-coach-ai.vercel.app | ✅ Live |
| V3 (Azure) | Azure Static Web Apps | 🔨 Active Build |
| GitHub | https://github.com/shahzad-ai-lab/shahzad-job-coach-ai | ✅ |

---

## The Mission

**Shahzad Muhammad · Mississauga, Canada**

Most career tools cost money. Most are built for Western, English-speaking job seekers. Most ignore the 6+ billion people outside North America and Europe.

Alfalah AI changes that.

- **Free forever** — no subscription, no login, no paywall
- **Zero data storage** — your resume never touches our database
- **195 countries** — every UN-recognized nation supported
- **15 industries** — IT, Healthcare, Finance, Engineering, Education, Trades, Marketing, Legal, HR, Logistics, Creative, Hospitality, Government, Science, and more
- **All humanity's professions** — 436 ISCO-08 groups, 3,000+ ESCO occupations, 123,000 global job titles
- **No bias** — same quality of analysis for a textile worker in Bangladesh as a software engineer in San Francisco

---

## V1 — The Prototype (March 6–8, 2026)

Built in 72 hours for a hackathon.

**What it did:**
- 12 AI-powered career cards (resume score, cover letter, interview prep, etc.)
- Single AI provider (Google Gemini)
- Basic resume text input
- Simple CSS design
- No country awareness, no industry awareness

**Result:** Submitted to H1 $6,000 hackathon on March 8, 2026. ✓

**Stack:** Next.js 14 + Google Gemini API + Vercel

---

## V2 — The Intelligence Engine (March 11–15, 2026)

30 sessions of deep engineering.

**What changed:**
- **17 AI cards** — expanded from 12 to 17 comprehensive career analysis tools
- **640KB career knowledge base** — MASTER_CAREER_REFERENCE.md covering visa pathways, salary data, ATS algorithms, global hiring norms across 195 countries
- **RAG system** — 9 local knowledge files injected into every AI call, zero hallucination
- **Multi-provider AI chain** — Gemini KEY1 → Gemini KEY2 → Grok-4-latest (never goes down)
- **5-phase smart splash** — IP auto-detection → country confirm → 195-country selector → industry selector
- **195 countries** — full data packages: labor law, salary, visa, ATS norms, certifications, top employers
- **PDF + DOCX upload** — parse resume from file (5MB limit, secure)
- **Download results** — export all 17 cards as text file
- **PWA store-ready** — installable on Android/iOS, manifest + icons ✅
- **Country-aware AI** — different guidance for in-country vs cross-border job applications
- **Skills Assessment** — 5-step quiz, 7 ISCO career categories, 0-100 score, 70+ career recommendations
- **NASA galaxy UI** — animated stars, nebula clouds, shooting stars, ripple effects
- **RED negative highlighting** — AI-detected weaknesses highlighted in red across all cards
- **Live job search** — Google Jobs via Serper API, country-specific, last 7 days
- **ISCO-08 occupations** — 436 unit groups with JDs, skills, tasks, salary, AI risk assessment

**Stack:** Next.js 14 + Google Gemini + xAI Grok + Serper.dev + Vercel

---

## V3 — Pure Azure Cloud (March 21, 2026 — Active)

**Why V3?** Microsoft Azure AI competition. Full enterprise-grade cloud architecture.

**What's different from V2:**
- **100% Azure ecosystem** — no external cloud providers
- **Azure Functions v2 (Python)** — serverless backend, auto-scales, zero cold start penalty
- **Azure OpenAI** — GPT-4o and GPT-4o-mini (Azure-hosted, Canada East)
- **Azure AI Search** — vector + semantic search across all career knowledge
- **Azure Cosmos DB** — NoSQL for session data (zero PII stored)
- **Azure Key Vault** — all secrets managed securely, never in code
- **Azure Entra ID B2C** — identity layer (optional auth for future features)
- **Azure Static Web Apps** — frontend hosting with global CDN
- **GitHub Actions CI/CD** — auto-deploy on every push to main
- **GRC compliance** — RBAC, audit logs, threat protection, data sovereignty

**Architecture:**
```
User Browser
    │
    ▼
Azure Static Web Apps (CDN — global edge)
    │
    ▼
Azure Functions v2 Python (serverless API)
    ├── /career     — 17-card analysis + RAG + AI polish
    ├── /chat       — conversational career coach
    ├── /jobs       — Google Jobs via Serper (last 7 days)
    ├── /location   — IP geolocation (ip-api.com)
    ├── /occupations — career data inventory
    └── /upload     — secure PDF/DOCX/TXT extraction
    │
    ▼
RAG Knowledge Base (local .md files, chunked + indexed)
    ├── 436 ISCO-08 occupations with full JDs
    ├── 195 country packages (laws, salary, visa, ATS)
    ├── 500+ hard skills + 250+ soft skills A-Z
    ├── Future occupations 2026–2125
    ├── Top 1% hiring framework (Google, Amazon, Microsoft)
    ├── Global platforms, tools, Fortune 500 companies
    └── 10 more career intelligence files
    │
    ▼
AI Fallback Chain
    ├── Azure OpenAI (GPT-4o-mini) — primary
    ├── Google Gemini KEY1 (3 models) — fallback
    ├── Google Gemini KEY2 (3 models) — fallback
    └── xAI Grok (grok-4-latest) — final fallback
```

**Resource Group:** `rg-v3` · **Subscription:** `2d7fae20-e207-40a5-bc46-53df96affcb7`
**Region:** Canada East (data sovereignty for Canadian users)

---

## The 17 Career Tools

| # | Tool | What It Does |
|---|------|-------------|
| 1 | Resume Score | ATS algorithm score + 8 weighted dimensions + knockouts |
| 2 | Recruiter POV | 6-second skim test — what gets noticed vs buried |
| 3 | Cover Letter | Top 1% letter with specific hook + 3 quantified wins |
| 4 | Resume Rewrite | 3-step rebuild: diagnose → extract wins → reorder for impact |
| 5 | Skills Gap | Hard/soft matched vs missing + certs with URLs + roadmap |
| 6 | Interview Prep | 5 Q&A + behavioral questions + questions to ask |
| 7 | STAR Stories | 3 behavioral stories with metrics using STAR method |
| 8 | LinkedIn Summary | About section optimized for search + recruiters |
| 9 | Intro Scripts | 1-min, 2-min, 3-min professional introduction scripts |
| 10 | Matching Jobs | Titles + companies + job boards + 7-country recruiters |
| 11 | Visa Pathways | In-country AND cross-border — ALL visa routes + official URLs |
| 12 | Thank You Email | Post-interview email that moves you to top of pile |
| 13 | Salary Negotiation | Salary table Entry→Exec + negotiation scripts (local currency) |
| 14 | Action Plan | 30-60-90 day onboarding and job search plan |
| 15 | Cold Outreach | LinkedIn DM + cold email + follow-up templates |
| 16 | Career Pivot | Pivot score + 3 adjacent roles + 90-day transition plan |
| 17 | Country Laws | Labor law + resume compliance + worker rights + GRC |

**Plus:**
- **Similar Occupations** — ISCO-08 adjacent roles you qualify for today
- **JD Template** — what a proper job description looks like for your role
- **Top 1% Tips** — how Google, Amazon, Microsoft actually hire
- **Live Jobs** — real postings from the last 7 days in your country

---

## The RAG Knowledge Base (27 Files, ~800KB)

All processing is **99% algorithmic** (fast, free, deterministic). AI only handles the final 1% — formatting and narrative polish.

| File | Coverage |
|------|----------|
| `occupations-master-isco08-all.md` | All 436 ISCO-08 groups, JDs, skills, salary, AI risk |
| `skills-az-master.md` | 500+ hard skills, 250+ soft skills, future skills 2026–2125 |
| `future-occupations-2026-2125.md` | Emerging roles across 5 time horizons to 2125 |
| `top-1-percent-framework.md` | Google/Amazon/Microsoft hiring science, ATS algorithms |
| `global-platforms-tools-companies.md` | Fortune 500 + tools A-Z + companies by region worldwide |
| `MASTER_CAREER_REFERENCE.md` | 640KB career intelligence covering 195 countries |
| `COUNTRY_PACKAGES_195.md` | All 195 UN countries — salary, visa, laws, boards |
| `CERTIFICATIONS_2026.md` | All-industry certs A-Z — Cloud, Cyber, Finance, Trades, AI |
| `COMPANIES_BY_COUNTRY.md` | Top employers + career URLs for 30+ countries |
| `OCCUPATIONS_ISCO08.md` | ISCO-08 436 groups, BLS fastest-growing, 2026 roles |
| `ALL_COUNTRIES.md` | 195 UN countries, ISO codes, regions, tiers |
| + 16 more | Platforms, certifications, compliance, salary data |

---

## All Professions — All Humanity

ISCO-08 covers every job humans do, from Managing Directors to Agricultural Laborers:

| Major Group | Occupations | Examples |
|-------------|-------------|---------|
| 1 — Managers | Chief Executives, Directors | CEO, COO, Department Manager |
| 2 — Professionals | Engineers, Doctors, Scientists | Software Dev, Nurse, Accountant |
| 3 — Technicians | IT Techs, Paramedics | Network Tech, Medical Lab Tech |
| 4 — Clerical | Admin, Secretaries | Data Entry, Receptionist |
| 5 — Service/Sales | Retail, Healthcare Aides | Salesperson, Personal Care Worker |
| 6 — Agriculture | Farmers, Fishers | Market Gardener, Livestock Farmer |
| 7 — Trades | Electricians, Builders | Plumber, Welder, Carpenter |
| 8 — Plant/Machine | Operators, Drivers | Truck Driver, Assembly Line Worker |
| 9 — Elementary | Cleaners, Laborers | Construction Helper, Food Preparer |
| 0 — Armed Forces | Military Officers, Soldiers | Officer, Non-Commissioned Officer |

**Total:** 436 unit groups → 3,000+ ESCO occupations → 123,000+ global job titles

No job is too small. No career is too niche. Every human gets equal quality analysis.

---

## Global Tools, Platforms, Technologies (A-Z)

The platform knows every tool across every industry:

**Cloud:** AWS · Azure · GCP · Oracle Cloud · IBM Cloud · Alibaba Cloud
**AI/ML:** TensorFlow · PyTorch · scikit-learn · Hugging Face · OpenAI · Anthropic · Vertex AI
**ERP/CRM:** SAP · Oracle ERP · Salesforce · Microsoft Dynamics · Workday · ServiceNow
**DevOps:** Docker · Kubernetes · Terraform · Jenkins · GitHub Actions · ArgoCD
**Data:** Spark · Databricks · Snowflake · dbt · Airflow · Kafka · Tableau · Power BI
**Cybersecurity:** Splunk · CrowdStrike · Palo Alto · Fortinet · SentinelOne · Tenable
**Healthcare:** Epic · Cerner · MEDITECH · Allscripts · HealthStream
**Finance:** Bloomberg · Reuters Eikon · Murex · Finastra · Temenos · FIS · Fiserv
**HR Tech:** Workday · SAP SuccessFactors · BambooHR · ADP · Greenhouse · Lever
**Design:** Figma · Adobe XD · Sketch · InVision · Canva · Adobe Creative Suite
**...and 500+ more** across every industry sector

---

## Companies Worldwide

Career URLs for top employers on every continent:

**North America:** Apple · Google · Microsoft · Amazon · Meta · JPMorgan · Goldman Sachs · RBC · TD Bank · Shopify · [+25 more]
**Europe:** SAP · Siemens · Volkswagen · HSBC · Unilever · Nestlé · LVMH · Airbus · [+40 more]
**Middle East:** Saudi Aramco · Emirates · ADNOC · Etisalat · STC · Majid Al Futtaim · [+15 more]
**Asia:** Samsung · Toyota · TSMC · Infosys · TCS · Wipro · Alibaba · Tencent · [+40 more]
**South Asia:** HBL · PTCL · Engro · Lucky Cement · Sui Gas · [+10 more]
**Africa:** MTN · Safaricom · Standard Bank · Dangote · [+10 more]
**Oceania:** BHP · Commonwealth Bank · Telstra · ANZ · Westpac · [+10 more]

---

## Future Occupations (2026–2125)

The platform includes 100+ years of emerging career roles:

**Near-term (2026–2035):**
- AI Prompt Engineer · LLM Fine-Tuning Specialist · AI Ethics Officer
- Carbon Market Trader · ESG Analyst · Green Hydrogen Engineer
- Longevity Scientist · Microbiome Nutritionist

**Mid-term (2035–2060):**
- Digital-Physical Integration Architect · Quantum Algorithm Designer
- CRISPR Gene Therapy Specialist · Vertical Farm Systems Engineer

**Long-term (2060–2125):**
- Space Habitat Architect · Asteroid Mining Engineer
- Post-AGI Collaboration Designer · Extended Cognition Interface Engineer

---

## Security

- **Zero PII storage** — resumes processed in memory, never written to disk or database
- **Input sanitization** — HTML injection, SQL injection, prompt injection all blocked
- **50KB body guard** — oversized payloads rejected
- **Rate limiting** — per-IP limits (disabled in dev, enforced in production)
- **HTTPS only** — Azure enforced TLS 1.2+
- **CORS locked** — only approved origins accepted
- **Azure Key Vault** — all API keys managed, never in code
- **RBAC** — least-privilege access on all Azure resources

---

## Skills Assessment

A separate `/assess` tool (5-step quiz):

1. **Current situation** — working, studying, transitioning
2. **Industry** — 7 ISCO career categories
3. **Experience level** — entry to executive
4. **Strengths** — top 3 self-assessed skills
5. **Goals** — what you want to achieve

**Output:** 0-100 career readiness score + 70+ personalized career recommendations

---

## Running Locally (V3)

```bash
# Prerequisites: Python 3.11+, Azure Functions Core Tools v4

cd v3
pip install -r requirements.txt
func start

# Frontend: open static/index.html in browser
# Or: serve with Live Server (VS Code extension)
```

**Environment variables needed:**
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
GEMINI_API_KEY=your-key
GEMINI_API_KEY_2=your-key
GROK_API_KEY=your-key
SERPER_API_KEY=your-key
```

---

## Deploying to Azure

```bash
# Deploy function app
cd v3
func azure functionapp publish govrag-v3-func

# Or via GitHub Actions (auto on push to main)
git push origin main
```

CI/CD: `.github/workflows/` auto-deploys frontend + backend on push to main.

---

## Contributing

This is a free, open-source project serving humanity.

**No bias. No racism. No religious discrimination. No political agenda.**

Every contribution should uphold these values:
- Career tools should work equally well for a nurse in Nigeria and a developer in Norway
- Salary data should be accurate for local markets, not just Silicon Valley
- Visa guidance should reflect real pathways, not ideal-world scenarios
- Skills recommendations should include free learning resources, not just expensive courses

---

## License

MIT License — free forever.

---

## Built by

**Shahzad Muhammad**
Mississauga, Ontario, Canada
Mission: Free AI tools for all 8 billion humans on Earth.

*Alfalah (الفلاح) — Arabic/Urdu for "Come to Success"*
*Used in the Islamic call to prayer: "Come to prayer, come to success"*
*A word that belongs to all humanity — success has no borders.*

---

*V3 last updated: March 2026*
