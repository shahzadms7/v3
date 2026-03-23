# Transparency Note: GovRAG V3 — Alfalah AI Career Intelligence Platform

**Version:** 1.0
**Date:** March 22, 2026
**Author:** Shahzad Muhammad, Alfalah AI
**Azure Resource Group:** rg-v3
**Subscription:** 2d7fae20-e207-40a5-bc46-53df96affcb7

This Transparency Note is designed to help you understand how GovRAG V3's AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system — including the technology, the people, and the environment. This document follows [Microsoft's Transparency Note framework](https://learn.microsoft.com/en-us/azure/ai-services/openai/transparency-note) for responsible AI disclosure.

---

## 1. What is GovRAG V3?

GovRAG V3 (Governed Retrieval-Augmented Generation, Version 3) is a **free, zero-login AI career intelligence platform** built on the Microsoft Azure cloud ecosystem. It serves **8 billion humans globally** across **195 UN-recognized countries** with AI-powered career guidance, resume analysis, compliance Q&A, and job market intelligence.

The system uses **Retrieval-Augmented Generation (RAG)** — a pattern where user queries are answered by first retrieving relevant passages from a curated knowledge base of 30+ authoritative data files, then generating a grounded AI response with source citations. A **3-gate governance layer** ensures every response is faithful, safe, and compliant before delivery.

### Core Architecture

| Component | Azure Service | Purpose |
|-----------|--------------|---------|
| Frontend | Azure Static Web Apps | Next.js application, globally distributed |
| API Layer | Azure Functions (Python) | Serverless compute, auto-scaling |
| AI Engine | Azure OpenAI Service | GPT-4o for generation, embeddings for retrieval |
| Search | Azure AI Search | Vector + keyword hybrid search over 30+ data files |
| Knowledge Base | Azure Blob Storage | 30+ curated .md files (career, legal, visa, cert data) |
| Safety | Azure AI Content Safety | Pre- and post-generation content filtering |
| Translation | Azure Translator | Multilingual support for global reach |
| Language | Azure AI Language | Entity recognition, key phrase extraction |
| Monitoring | Azure Application Insights | Performance telemetry, error tracking, usage analytics |

### What It Does

- Analyzes resumes against job descriptions using ATS (Applicant Tracking System) scoring algorithms
- Generates 17 AI career intelligence cards (cover letters, interview prep, STAR stories, salary negotiation, visa pathways, and more)
- Provides country-specific labor law guidance for all 195 UN countries
- Delivers industry-specific certification recommendations
- Answers compliance and career questions grounded in curated, authoritative data files
- Serves users aged 5 to 100 with age-appropriate career guidance

---

## 2. Intended Uses

GovRAG V3 is designed for the following use cases:

### Primary Uses

| Use Case | Description | Example |
|----------|-------------|---------|
| **Resume Analysis** | Score resumes against job descriptions using ATS algorithms, keyword matching, and recruiter methodology | A job seeker uploads their resume and a job posting to receive a composite score, gap analysis, and rewrite suggestions |
| **Career Intelligence** | Generate AI-powered career guidance cards covering 17 dimensions of job search preparation | A user in Nigeria receives visa pathway guidance for a software engineering role in Canada |
| **Compliance Q&A** | Answer questions about labor laws, visa requirements, and hiring regulations grounded in curated data files | A user asks about notice period requirements in Germany and receives cited, country-specific guidance |
| **Certification Guidance** | Recommend industry-recognized certifications based on user's country, industry, and career goals | A healthcare worker in Pakistan receives recommendations for globally recognized certifications |
| **Skills Assessment** | Evaluate career readiness through a 5-step quiz mapping to ISCO-08 occupational categories | A student takes the assessment and receives a score with 70+ career recommendations |

### Target Users

- **Job seekers** in any of 195 countries, at any career stage (entry to executive)
- **Career changers** exploring adjacent roles and pivot strategies
- **International workers** navigating cross-border employment and visa pathways
- **Students** (age 14+) exploring career options and required qualifications
- **Underserved communities** who cannot afford professional career coaching services

### Deployment Context

- **Free access** — no subscription, no payment, no freemium tiers
- **No login required** — zero authentication barriers
- **Zero data storage** — no resumes, queries, or personal data are stored after the session ends
- **Global availability** — served via Azure Static Web Apps with global CDN distribution

---

## 3. Uses That Require Extra Care

The following use cases are **not intended** or require **professional verification**:

### Medical Advice
GovRAG V3 may reference occupational health requirements (e.g., medical clearances for certain roles, disability accommodations). **This information is general guidance only.** Users must consult licensed medical professionals for health-related decisions. The system explicitly disclaims medical authority in its responses.

### Legal Advice
The system provides labor law summaries, visa pathway overviews, and employment regulation guidance sourced from curated reference files. **This is informational only and does not constitute legal counsel.** Immigration decisions, employment disputes, and contract negotiations require consultation with qualified legal professionals in the relevant jurisdiction.

### Financial Decisions
Salary data, cost-of-living comparisons, and negotiation scripts are based on aggregated market data. **Individual compensation decisions** should factor in personal circumstances, local market conditions, and professional financial advice.

### High-Stakes Employment Decisions
Employers should **never** use GovRAG V3 scores as the sole basis for hiring, firing, or promotion decisions. The system is designed to help job seekers improve their applications — not to serve as an automated decision-making tool for employers.

### Vulnerable Populations
The system serves users aged 5-100 with age-appropriate guidance. However:
- **Minors** (under 18): Career guidance for minors is exploratory only and should involve parental or educational supervision
- **Users in crisis**: The system is not a substitute for mental health services, crisis hotlines, or social services
- **Users with limited digital literacy**: While the interface uses ELI12 (Explain Like I'm 12) language, some concepts (visa categories, ATS optimization) may require additional context

### Jurisdictional Limitations
Labor laws, visa requirements, and certification standards change frequently. While the knowledge base is regularly updated, **real-time regulatory changes may not be reflected immediately.** Users should verify critical information with official government sources (links are provided in responses).

---

## 4. Capabilities and Limitations

### What GovRAG V3 Can Do

| Capability | Details |
|-----------|---------|
| **Resume Scoring** | Composite ATS score using keyword density, achievement density, recency decay, section anatomy, and 200+ stop-word filtering |
| **17 AI Cards** | Cover letter, recruiter POV, resume rewrite, skills gap, interview prep, STAR stories, LinkedIn optimization, salary negotiation, visa pathways, career pivot, country laws, and more |
| **195-Country Intelligence** | Country-specific labor laws, visa requirements, salary ranges (local currency), certification recognition, and job market data |
| **30+ Data File RAG** | Grounded responses from curated knowledge base: MASTER_CAREER_REFERENCE (640KB), COUNTRY_PACKAGES_195, CERTIFICATIONS_2026, COMPANIES_BY_COUNTRY (500+ companies), OCCUPATIONS_ISCO08 (436 ISCO-08 groups), and more |
| **Hybrid Search** | Azure AI Search with vector embeddings + BM25 keyword matching for high-recall retrieval |
| **Multi-AI Fallback** | Cascading model chain ensures availability even during individual model outages |
| **Multilingual Support** | Azure Translator integration for global language coverage |
| **Content Safety** | Azure AI Content Safety pre-screens inputs and post-screens outputs |
| **Source Citations** | Every AI response includes citations to the specific data files and passages used |

### What GovRAG V3 Cannot Do

| Limitation | Details |
|-----------|---------|
| **Real-time job listings** | Job market data is based on curated reference files, not live API feeds (Serper.dev integration is planned but not active in V3) |
| **Guarantee employment** | The system improves application quality but cannot guarantee interview callbacks or job offers |
| **Replace professional advice** | Not a substitute for licensed lawyers, doctors, financial advisors, or certified career counselors |
| **Store user history** | Zero-storage architecture means no session history, no saved resumes, no progress tracking between visits |
| **Process non-text resumes** | Highly formatted, image-based, or infographic resumes may not parse accurately |
| **Cover all languages natively** | While Azure Translator provides broad coverage, AI generation quality varies by language; English produces the highest-fidelity outputs |
| **Predict future regulations** | Labor laws and visa policies change; the system reflects the knowledge base at its last update, not real-time legislative changes |
| **Handle multi-document queries** | Each analysis session processes one resume + one job description; comparative analysis across multiple documents is not supported |

### Knowledge Base Scope

The RAG system draws from **30+ curated data files** totaling over 1MB of structured career intelligence:

- **640KB** Master Career Reference (48 sections covering all career domains)
- **195 countries** with GDP, visa types, salary ranges, labor laws, job boards
- **436 ISCO-08** occupational groups with growth projections
- **500+ companies** across 30+ countries with career page URLs
- **All-industry certifications** A-Z (Cloud, Security, Finance, Trades, AI, Healthcare)
- **2026 job market trends**, ATS system intelligence, recruiter methodology

---

## 5. System Performance

### Faithfulness Scoring

GovRAG V3 implements a **faithfulness scoring system** to measure how well AI-generated responses are grounded in the retrieved source documents:

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| **Faithfulness Score** | > 0.85 | Ratio of response claims that are directly supported by retrieved passages |
| **Citation Coverage** | > 0.90 | Percentage of factual claims that include a source citation |
| **Hallucination Rate** | < 0.10 | Percentage of response claims not traceable to any source document |
| **Retrieval Precision** | > 0.80 | Percentage of retrieved passages that are relevant to the query |
| **Retrieval Recall** | > 0.75 | Percentage of relevant passages in the knowledge base that are retrieved |

### Latency Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| **Search Query** | < 200ms | Azure AI Search hybrid query |
| **AI Generation** | < 8s | Azure OpenAI GPT-4o with 8192 max tokens |
| **Content Safety Check** | < 500ms | Azure AI Content Safety pre/post screening |
| **End-to-End Response** | < 15s | Full pipeline: safety check → retrieval → generation → safety check → delivery |
| **Cold Start** | < 3s | Azure Functions consumption plan cold start |

### Availability

| Metric | Target |
|--------|--------|
| **Uptime** | 99.9% (Azure SLA) |
| **Multi-region failover** | Azure Static Web Apps global distribution |
| **AI model fallback** | Cascading chain ensures generation availability |

### Monitoring

All performance metrics are tracked via **Azure Application Insights**:
- Request duration percentiles (p50, p95, p99)
- Error rates by endpoint and error type
- AI model usage and fallback frequency
- Content Safety trigger rates
- Search relevance scores

---

## 6. Key Design Decisions

### Zero Storage Architecture

**Decision:** No user data (resumes, queries, personal information) is stored after the session ends.

**Rationale:** The platform serves 8 billion humans globally, including users in jurisdictions with strict data protection laws (GDPR, PIPEDA, LGPD, POPIA). Zero storage eliminates:
- Data breach risk (no data to breach)
- Cross-border data transfer compliance burden
- Right-to-deletion request handling
- Storage cost scaling with user growth

**Trade-off:** Users cannot access previous analysis results or track progress over time.

### Source Citations in Every Response

**Decision:** Every AI-generated response includes citations to the specific data files and passages that informed the answer.

**Rationale:** Transparency and verifiability are core to responsible AI. Citations allow users to:
- Verify claims against source material
- Understand the basis for recommendations
- Identify when guidance may be outdated
- Build trust in AI-generated content

### 3-Gate Safety Architecture

**Decision:** Every request passes through three governance gates before a response is delivered:

| Gate | Service | Purpose |
|------|---------|---------|
| **Gate 1: Input Safety** | Azure AI Content Safety | Screens user input for harmful content, prompt injection, jailbreak attempts |
| **Gate 2: Retrieval Governance** | Azure AI Search + custom logic | Ensures retrieved passages are from authorized, curated sources only |
| **Gate 3: Output Safety** | Azure AI Content Safety + faithfulness check | Screens generated response for harmful content, hallucination, and unfaithful claims |

**Rationale:** A single safety layer is insufficient for a globally-facing AI system. The 3-gate architecture provides defense-in-depth against:
- Adversarial inputs designed to elicit harmful outputs
- Retrieval of irrelevant or misleading passages
- AI hallucination or unfaithful generation

### Multi-AI Fallback Chain

**Decision:** The system uses a cascading model chain rather than a single AI model.

**Rationale:** Global availability requires resilience against individual model outages, rate limits, and regional service disruptions. The fallback chain ensures users always receive a response.

### Free, No-Login Access

**Decision:** No authentication, no payment, no freemium tiers.

**Rationale:** The mission is to serve 8 billion humans globally, including the most underserved. Authentication barriers disproportionately exclude:
- Users without email addresses
- Users in regions with unreliable internet (login flows add failure points)
- Users with privacy concerns about creating accounts
- Users who need quick, one-time career guidance

### Age-Inclusive Design (Ages 5-100)

**Decision:** The system provides age-appropriate career guidance for all ages.

**Rationale:** Career exploration starts early (children learning about professions) and continues through retirement (career transitions, encore careers, mentorship roles). Age-gating would exclude legitimate users.

---

## 7. Evaluation Methods

### Faithfulness Evaluation

GovRAG V3 measures response faithfulness using the following methodology:

1. **Claim Extraction:** Each AI-generated response is decomposed into individual factual claims
2. **Source Matching:** Each claim is matched against the retrieved passages using semantic similarity
3. **Faithfulness Score:** The ratio of supported claims to total claims produces the faithfulness score
4. **Threshold Enforcement:** Responses with faithfulness scores below 0.70 are flagged for review or regenerated

```
Faithfulness Score = (Claims supported by retrieved passages) / (Total factual claims in response)
```

### Safety Gate Evaluation

| Gate | Evaluation Method | Failure Action |
|------|-------------------|----------------|
| **Input Safety** | Azure AI Content Safety API severity scoring (0-7 scale) across 4 categories: Violence, Self-Harm, Sexual, Hate | Block request, return safe error message |
| **Retrieval Governance** | Source validation (only curated .md files), relevance scoring (minimum threshold 0.60) | Fall back to general guidance without specific citations |
| **Output Safety** | Azure AI Content Safety post-screening + faithfulness threshold check | Regenerate with stricter grounding instructions, or return safe fallback response |

### ATS Scoring Evaluation

The resume scoring algorithm is evaluated against known benchmarks:

| Component | Weight | Evaluation |
|-----------|--------|------------|
| Keyword Match | 30% | Precision/recall of job description keywords found in resume |
| Achievement Density | 25% | Ratio of quantified (numbered) bullets to total bullets |
| Section Anatomy | 15% | Presence and ordering of standard resume sections |
| Recency Decay | 15% | Score penalty for outdated experience (>10 years) without recent reinforcement |
| Stop-Word Filtering | 15% | 200+ generic stop words excluded from keyword matching to reduce false positives |

### Continuous Monitoring

- **Azure Application Insights** tracks all performance and quality metrics in real-time
- **Custom dashboards** monitor faithfulness scores, safety gate trigger rates, and model fallback frequency
- **Alerting rules** notify the development team when metrics fall below thresholds

---

## 8. Responsible AI Considerations

GovRAG V3 is designed in alignment with [Microsoft's Responsible AI Standard v2](https://www.microsoft.com/en-us/ai/principles-and-approach) and the six principles of responsible AI:

### Fairness

| Dimension | Implementation |
|-----------|---------------|
| **Geographic Fairness** | 195 UN-recognized countries with individualized data packages (labor laws, visa types, salary ranges, certifications, job boards) |
| **Age Inclusiveness** | Guidance for ages 5-100 with age-appropriate language and career stage recognition |
| **Industry Coverage** | 15 industry categories covering all major employment sectors globally |
| **Occupational Coverage** | 436 ISCO-08 occupational groups ensuring no profession is excluded |
| **Economic Accessibility** | Completely free — no subscription, no freemium, no hidden costs |
| **Language Access** | Azure Translator integration for multilingual support |
| **Disability Guidance** | Workplace accommodation guidance, disability disclosure strategies, and accessible career pathways included in knowledge base |
| **No Demographic Bias in Scoring** | ATS scoring algorithm evaluates resume content quality (keywords, achievements, structure) — not applicant demographics |

### Privacy

| Dimension | Implementation |
|-----------|---------------|
| **Zero Data Storage** | No resumes, queries, or personal information stored after session ends |
| **No User Tracking** | No cookies, no analytics profiles, no behavioral tracking |
| **No Login Required** | No email, phone, or social media account needed |
| **Client-Side Processing** | Resume text extracted client-side; only text content sent to API |
| **No Third-Party Data Sharing** | User inputs are not shared with third parties, used for model training, or retained in logs |
| **GDPR/PIPEDA/LGPD Compatible** | Zero-storage architecture is compliant by design with major privacy regulations |

### Transparency

| Dimension | Implementation |
|-----------|---------------|
| **Source Citations** | Every AI response cites the specific data files and passages used |
| **This Transparency Note** | Full disclosure of system capabilities, limitations, and design decisions |
| **Open Knowledge Base** | All 30+ data files are curated, documented, and version-controlled |
| **Scoring Explanation** | Resume scores include component breakdowns (keyword match, achievement density, section anatomy, recency) so users understand their score |
| **Limitation Disclosure** | The system explicitly states when guidance should be verified by professionals |
| **Red Flag Highlighting** | Negative findings (MISSING, GAP, WEAK, RED FLAG) are visually highlighted in red so users cannot miss critical issues |

### Safety

| Dimension | Implementation |
|-----------|---------------|
| **3-Gate Architecture** | Input safety, retrieval governance, and output safety gates |
| **Azure AI Content Safety** | Pre- and post-generation content filtering across Violence, Self-Harm, Sexual, and Hate categories |
| **Prompt Injection Defense** | Input sanitization, HTML/injection stripping, 50KB body size limit, 6K resume + 3K job description truncation |
| **Rate Limiting** | Client-side (localStorage) and server-side (IP-based) rate limiting to prevent abuse |
| **Security Headers** | DENY framing, CSP, nosniff, XSS protection headers on all responses |
| **No Harmful Career Guidance** | The system will not provide guidance on illegal employment, exploitation, or harmful workplace practices |

### Reliability and Safety

| Dimension | Implementation |
|-----------|---------------|
| **Multi-AI Fallback** | Cascading model chain ensures response delivery even during outages |
| **Timeout Protection** | 55-second per-call timeout prevents hung requests |
| **Graceful Degradation** | If AI generation fails entirely, users receive informative error messages with alternative actions |
| **Input Validation** | Strict input sanitization prevents malformed data from reaching AI models |
| **Error Monitoring** | Azure Application Insights tracks all errors with alerting thresholds |

### Inclusiveness

| Dimension | Implementation |
|-----------|---------------|
| **ELI12 Language** | AI responses use "Explain Like I'm 12" language level — accessible to users with varying English proficiency |
| **195-Country Coverage** | No country excluded; every UN-recognized nation has a data package |
| **Age 5-100** | Career exploration for children, active guidance for working-age adults, encore career support for seniors |
| **Disability Guidance** | Workplace accommodation strategies, disclosure guidance, and accessible career pathways |
| **Economic Inclusiveness** | Free access ensures career intelligence is not gatekept behind paywalls |
| **No Digital Literacy Barrier** | Simple upload-and-analyze interface; no complex configuration required |
| **Cultural Sensitivity** | Country-specific guidance respects local customs, naming conventions, and resume formats |

### Accountability

| Dimension | Implementation |
|-----------|---------------|
| **Version Control** | All knowledge base files, code, and configuration are version-controlled in GitHub |
| **Audit Trail** | Azure Application Insights provides full request/response audit capability |
| **This Document** | Transparency Note serves as the accountability record for AI system behavior |
| **Regular Updates** | Knowledge base files are updated with each development session to reflect current data |
| **Contact** | Users can report issues via the GitHub repository issue tracker |

---

## 9. Learn More

### Microsoft Responsible AI Resources

| Resource | URL |
|----------|-----|
| Microsoft Responsible AI Principles | https://www.microsoft.com/en-us/ai/principles-and-approach |
| Microsoft Responsible AI Standard v2 | https://www.microsoft.com/en-us/ai/responsible-ai |
| Transparency Note Guidelines | https://learn.microsoft.com/en-us/azure/ai-services/openai/transparency-note |
| Azure AI Content Safety | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/ |
| Azure OpenAI Responsible AI | https://learn.microsoft.com/en-us/legal/cognitive-services/openai/transparency-note |

### Azure Service Documentation

| Service | URL |
|---------|-----|
| Azure OpenAI Service | https://learn.microsoft.com/en-us/azure/ai-services/openai/ |
| Azure AI Search | https://learn.microsoft.com/en-us/azure/search/ |
| Azure Functions | https://learn.microsoft.com/en-us/azure/azure-functions/ |
| Azure Static Web Apps | https://learn.microsoft.com/en-us/azure/static-web-apps/ |
| Azure Blob Storage | https://learn.microsoft.com/en-us/azure/storage/blobs/ |
| Azure AI Content Safety | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/ |
| Azure AI Language | https://learn.microsoft.com/en-us/azure/ai-services/language-service/ |
| Azure Translator | https://learn.microsoft.com/en-us/azure/ai-services/translator/ |
| Azure Application Insights | https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview |
| Azure Cosmos DB | https://learn.microsoft.com/en-us/azure/cosmos-db/ |
| Azure Key Vault | https://learn.microsoft.com/en-us/azure/key-vault/ |

### Alfalah AI Project

| Resource | URL |
|----------|-----|
| Live V2 Demo | https://shahzad-job-coach-ai.vercel.app |
| GitHub Repository | https://github.com/shahzad-ai-lab/shahzad-job-coach-ai |
| V3 Azure Blueprint | See `v3/V3_AZURE_MASTER_BLUEPRINT.md` in repository |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-22 | Initial Transparency Note for GovRAG V3 |

---

*This Transparency Note is a living document and will be updated as the system evolves. Last updated: March 22, 2026.*
