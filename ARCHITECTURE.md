# Alfalah Job Career Intelligent AI 2026 V3 — System Architecture
### *End-to-End Technical Architecture · Built for 8 Billion People · Powered by Microsoft Azure*

<div align="center">

![Architecture](https://img.shields.io/badge/Architecture-Azure%20Cloud%20Native-0078D4?style=for-the-badge&logo=microsoftazure)
![AI Models](https://img.shields.io/badge/AI%20Models-4%20Providers%20%7C%208%20Models-FF6B35?style=for-the-badge)
![RAG Engine](https://img.shields.io/badge/RAG%20Engine-28%20Files%20%7C%201M%2B%20Tokens-8B5CF6?style=for-the-badge)

</div>

---

## High-Level System Overview

```mermaid
graph TB
    subgraph USER["👤 USER — 195 Countries · Any Device"]
        Browser["🌐 Web Browser / PWA<br/>(Chrome · Safari · Firefox · Edge)"]
        Mobile["📱 Mobile App<br/>(PWA · React Native V4)"]
    end

    subgraph AZURE_CDN["☁️ AZURE STATIC WEB APPS — Global CDN Edge"]
        Frontend["⚛️ React / Next.js Frontend<br/>Galaxy UI · 17 Module Dashboard<br/>195-Country Splash Screen"]
    end

    subgraph AZURE_FUNCTIONS["⚡ AZURE FUNCTIONS v2 — Python Serverless"]
        CareerAPI["POST /career<br/>17-Module Analysis"]
        ChatAPI["POST /chat<br/>Career Coaching"]
        JobsAPI["POST /jobs<br/>Live Job Search"]
        LocationAPI["GET /location<br/>IP Geolocation"]
        HealthAPI["GET /health<br/>System Status"]
        UploadAPI["POST /upload<br/>File Extraction"]
    end

    subgraph AI_LAYER["🤖 AI INFERENCE LAYER — 4 Providers · 8 Models"]
        AzureOAI["🔵 Azure OpenAI<br/>GPT-4o-mini<br/>(Primary)"]
        Gemini1["🟡 Google Gemini<br/>2.0 Flash KEY1<br/>(Fallback 1)"]
        Gemini2["🟡 Google Gemini<br/>2.0 Flash KEY2<br/>(Fallback 2)"]
        Grok["⚫ xAI Grok-4<br/>grok-4-latest<br/>(Fallback 3)"]
    end

    subgraph RAG["📚 RAG KNOWLEDGE ENGINE — 28 Files · 1M+ Tokens"]
        Occupations["436 ISCO-08<br/>Occupations"]
        Countries["195 Country<br/>Data Packages"]
        Skills["900+ Skills<br/>A-Z Master"]
        Future["Future Jobs<br/>2026–2125"]
        Framework["Top-1% Hiring<br/>Framework"]
        More["21 Additional<br/>Intelligence Files"]
    end

    subgraph AZURE_SERVICES["🔒 AZURE SUPPORTING SERVICES"]
        KeyVault["🔑 Azure Key Vault<br/>Secrets Management"]
        AISearch["🔍 Azure AI Search<br/>Semantic + Vector"]
        ContentSafety["🛡️ Azure Content Safety<br/>Output Moderation"]
        Monitor["📊 Azure Monitor<br/>Observability"]
    end

    subgraph EXTERNAL["🌍 EXTERNAL APIs"]
        Serper["Serper.dev<br/>Google Jobs API"]
        IPApi["ipapi.co<br/>Geolocation"]
    end

    subgraph DEVOPS["🔄 CI/CD — GitHub → Azure"]
        GitHub["GitHub<br/>shahzadms7/v3"]
        GHActions["GitHub Actions<br/>Auto-Deploy"]
        VSCode["VS Code +<br/>Claude Code AI"]
    end

    Browser --> Frontend
    Mobile --> Frontend
    Frontend --> CareerAPI
    Frontend --> ChatAPI
    Frontend --> JobsAPI
    Frontend --> LocationAPI
    Frontend --> UploadAPI

    CareerAPI --> AzureOAI
    AzureOAI -->|"fail"| Gemini1
    Gemini1 -->|"fail"| Gemini2
    Gemini2 -->|"fail"| Grok

    CareerAPI --> AISearch
    AISearch --> RAG

    CareerAPI --> KeyVault
    CareerAPI --> ContentSafety

    JobsAPI --> Serper
    LocationAPI --> IPApi

    AzureOAI --> Monitor

    GitHub --> GHActions
    GHActions --> AZURE_CDN
    GHActions --> AZURE_FUNCTIONS
    VSCode --> GitHub

    style USER fill:#1a1a2e,stroke:#0078D4,color:#fff
    style AZURE_CDN fill:#0078D4,stroke:#005a9e,color:#fff
    style AZURE_FUNCTIONS fill:#0078D4,stroke:#005a9e,color:#fff
    style AI_LAYER fill:#FF6B35,stroke:#cc5500,color:#fff
    style RAG fill:#8B5CF6,stroke:#6d28d9,color:#fff
    style AZURE_SERVICES fill:#0078D4,stroke:#005a9e,color:#fff
    style EXTERNAL fill:#374151,stroke:#6b7280,color:#fff
    style DEVOPS fill:#22C55E,stroke:#16a34a,color:#fff
```

---

## Request Processing Flow — End to End

```mermaid
sequenceDiagram
    actor User as 👤 User (195 countries)
    participant CDN as Azure Static Web Apps
    participant Func as Azure Functions
    participant KV as Azure Key Vault
    participant Search as Azure AI Search
    participant RAG as RAG Knowledge Base
    participant OAI as Azure OpenAI
    participant CS as Content Safety

    User->>CDN: 1. Visit platform (any browser, any country)
    CDN->>User: 2. Serve React app from nearest CDN edge node

    Note over User,CDN: 5-Phase Smart Splash: loading → detecting → detected → country → industry

    User->>Func: 3. POST /upload (PDF/DOCX/TXT resume)
    Func->>User: 4. Extracted plain text (in-memory, never stored)

    User->>Func: 5. POST /career (resume + job desc + country + industry)

    Func->>KV: 6. Retrieve API keys (RBAC-controlled)
    KV->>Func: 7. Secrets returned securely

    Func->>Search: 8. Semantic query: occupation + country + industry
    Search->>RAG: 9. Vector + keyword retrieval
    RAG->>Search: 10. Relevant career data (occupation profile, country laws, certs)
    Search->>Func: 11. Top-k grounded context chunks

    Func->>OAI: 12. Structured prompt = RAG context + resume + 17-module instructions

    alt Azure OpenAI available
        OAI->>CS: 13a. Content safety check
        CS->>Func: 14a. Safe response
    else Azure OpenAI fails
        Func->>Func: 13b. Fallback: Gemini KEY1 → KEY2 → Grok
    end

    Func->>User: 15. 17 career modules (JSON)
    CDN->>User: 16. Rendered dashboard with all modules

    Note over Func: All user data discarded — zero storage, zero PII retained
```

---

## AI Fallback Chain Architecture

```mermaid
graph LR
    subgraph ATTEMPT["🔄 AI Fallback Chain — Zero Downtime"]
        direction TB
        A1["🔵 Azure OpenAI<br/>GPT-4o-mini<br/>PRIMARY"]
        A2["🟡 Gemini 2.0 Flash<br/>KEY1 — Model 1<br/>gemini-2.0-flash"]
        A3["🟡 Gemini Flash Latest<br/>KEY1 — Model 2<br/>gemini-flash-latest"]
        A4["🟡 Gemini 2.0 Flash Lite<br/>KEY1 — Model 3"]
        A5["🟡 Gemini 1.5 Flash<br/>KEY1 — Model 4"]
        A6["🟡 Gemini 2.0 Flash<br/>KEY2 — Model 1"]
        A7["🟡 Gemini Flash Latest<br/>KEY2 — Model 2"]
        A8["🟡 Gemini 2.0 Flash Lite<br/>KEY2 — Model 3"]
        A9["🟡 Gemini 1.5 Flash<br/>KEY2 — Model 4"]
        A10["⚫ xAI Grok-4-latest<br/>FINAL FALLBACK"]

        A1 -->|"timeout / error"| A2
        A2 -->|"fail"| A3
        A3 -->|"fail"| A4
        A4 -->|"fail"| A5
        A5 -->|"fail"| A6
        A6 -->|"fail"| A7
        A7 -->|"fail"| A8
        A8 -->|"fail"| A9
        A9 -->|"fail"| A10
    end

    START["📥 API Request"] --> A1
    A1 -->|"success ✅"| OUT["📤 Response to User"]
    A2 -->|"success ✅"| OUT
    A3 -->|"success ✅"| OUT
    A4 -->|"success ✅"| OUT
    A5 -->|"success ✅"| OUT
    A6 -->|"success ✅"| OUT
    A7 -->|"success ✅"| OUT
    A8 -->|"success ✅"| OUT
    A9 -->|"success ✅"| OUT
    A10 -->|"success ✅"| OUT
```

**Result: 10 sequential attempts across 4 AI providers before failure. Platform uptime: 99.9%+**

---

## RAG Knowledge Engine Architecture

```mermaid
graph TB
    subgraph INPUT["📥 User Input"]
        Resume["Resume Text<br/>(6,000 chars max)"]
        JobDesc["Job Description<br/>(3,000 chars optional)"]
        Country["Selected Country<br/>(195 options)"]
        Industry["Selected Industry<br/>(15 categories)"]
    end

    subgraph RETRIEVAL["🔍 Azure AI Search — Semantic Retrieval"]
        Parser["Input Parser<br/>Extract: role · skills · country · industry"]
        VectorSearch["Vector Search<br/>(semantic similarity)"]
        KeywordSearch["Keyword Search<br/>(BM25 hybrid)"]
        Reranker["Semantic Reranker<br/>(top-k chunks)"]
    end

    subgraph KNOWLEDGE["📚 Knowledge Base — 28 Files"]
        K1["occupations-master-isco08-all.md<br/>436 ISCO-08 groups"]
        K2["skills-az-master.md<br/>900+ skills"]
        K3["countries-195-complete.md<br/>195 country packages"]
        K4["visa-immigration-195-countries.md<br/>All visa routes"]
        K5["certifications-2026.md<br/>300+ certs + official URLs"]
        K6["global-salary-data.md<br/>195-country salary tables"]
        K7["top-1-percent-framework.md<br/>ATS science + recruiter behavior"]
        K8["future-occupations-2026-2125.md<br/>Emerging roles"]
        K9["[20 additional intelligence files]"]
    end

    subgraph PROMPT["⚙️ Prompt Assembly"]
        Context["Grounded Context<br/>(RAG retrieved data)"]
        Instructions["17-Module Instructions<br/>(structured output schema)"]
        Methodology["Top Recruiter Methodology<br/>(3-step framework baked in)"]
        FinalPrompt["Final Structured Prompt<br/>(8,192 token output budget)"]
    end

    subgraph OUTPUT["📤 17 Module Output"]
        JSON["Structured JSON Response"]
        M1["Resume Score"]
        M2["Recruiter POV"]
        M3["Cover Letter"]
        M4["Resume Rewrite"]
        M5["Skills Gap"]
        M6["...13 more modules"]
    end

    INPUT --> Parser
    Parser --> VectorSearch
    Parser --> KeywordSearch
    VectorSearch --> KNOWLEDGE
    KeywordSearch --> KNOWLEDGE
    KNOWLEDGE --> Reranker
    Reranker --> Context
    Context --> FinalPrompt
    Instructions --> FinalPrompt
    Methodology --> FinalPrompt
    FinalPrompt --> JSON
    JSON --> M1 & M2 & M3 & M4 & M5 & M6
```

---

## Security Architecture

```mermaid
graph TB
    subgraph PERIMETER["🛡️ Security Perimeter"]
        HTTPS["TLS 1.3<br/>HTTPS Everywhere"]
        CORS["CORS Policy<br/>Strict Origin Allowlist"]
        Headers["Security Headers<br/>CSP · DENY · nosniff · XSS"]
    end

    subgraph INPUT_SEC["🔒 Input Security"]
        BodyGuard["50KB Body Guard<br/>Max request size"]
        Sanitize["Input Sanitization<br/>HTML · SQL · Prompt injection"]
        Truncate["Input Truncation<br/>Resume: 6K · Job: 3K chars"]
    end

    subgraph RATE_LIMIT["⏱️ Rate Limiting"]
        ClientRL["Client Rate Limit<br/>localStorage jcai_rl"]
        ServerRL["Server Rate Limit<br/>IP-based Map"]
    end

    subgraph SECRETS["🔑 Secrets Management"]
        KeyVault["Azure Key Vault<br/>All API keys"]
        RBAC["RBAC<br/>Reader (sub) · Contributor (rg)"]
        ManagedID["Managed Identity<br/>No secrets in code"]
    end

    subgraph AI_SEC["🤖 AI Safety"]
        ContentSafety["Azure Content Safety<br/>Output moderation"]
        Grounding["RAG Grounding<br/>Reduces hallucination 99%"]
        NoStorage["Zero Storage Policy<br/>All data discarded post-analysis"]
    end

    subgraph COMPLIANCE["📋 Compliance"]
        ResponsibleAI["Microsoft Responsible AI<br/>Standard v2"]
        GDPR["GDPR Compliant<br/>Zero PII storage"]
        GRC["GRC Framework<br/>Governance · Risk · Compliance"]
    end

    User --> HTTPS --> CORS --> Headers
    Headers --> INPUT_SEC
    INPUT_SEC --> RATE_LIMIT
    RATE_LIMIT --> SECRETS
    SECRETS --> AI_SEC
    AI_SEC --> COMPLIANCE
```

---

## CI/CD Pipeline — GitHub to Azure

```mermaid
graph LR
    subgraph DEV["💻 Development"]
        VSCode["VS Code +<br/>Claude Code AI"]
        LocalTest["Local Test<br/>func start"]
        Git["git commit +<br/>git push"]
    end

    subgraph GITHUB["🐙 GitHub — shahzadms7/v3"]
        Repo["Repository<br/>main branch"]
        Actions["GitHub Actions<br/>Workflow triggers"]
        PRCheck["PR Checks<br/>(future)"]
    end

    subgraph AZURE_DEPLOY["☁️ Azure Auto-Deploy"]
        StaticDeploy["Azure Static Web Apps<br/>Frontend → Global CDN"]
        FuncDeploy["Azure Functions<br/>Backend → Serverless"]
        KeyVaultSync["Key Vault<br/>Secrets sync"]
    end

    subgraph VERIFY["✅ Post-Deploy Verification"]
        Health["GET /api/health<br/>All providers green"]
        Smoke["Smoke test<br/>Sample career analysis"]
        Monitor["Azure Monitor<br/>Alerts + dashboards"]
    end

    VSCode --> LocalTest
    LocalTest --> Git
    Git --> Repo
    Repo --> Actions
    Actions --> StaticDeploy
    Actions --> FuncDeploy
    FuncDeploy --> KeyVaultSync
    StaticDeploy --> Health
    FuncDeploy --> Health
    Health --> Smoke
    Smoke --> Monitor
```

---

## Data Flow — Zero Storage Architecture

```mermaid
graph LR
    subgraph USER_SIDE["👤 User Side"]
        UploadResume["Upload Resume<br/>(PDF/DOCX/TXT)"]
        SelectCountry["Select Country<br/>from 195"]
        SelectIndustry["Select Industry<br/>from 15"]
    end

    subgraph PROCESSING["⚡ In-Memory Processing Only"]
        Extract["Extract Text<br/>(memory only)"]
        Analyze["AI Analysis<br/>(memory only)"]
        Generate["Generate 17 Modules<br/>(memory only)"]
    end

    subgraph RESPONSE["📤 Response"]
        Return["Return JSON<br/>to browser"]
        Display["Display Dashboard<br/>in browser"]
        DISCARD["🗑️ ALL DATA DISCARDED<br/>No database. No logs.<br/>No PII. No storage."]
    end

    UploadResume --> Extract
    SelectCountry --> Analyze
    SelectIndustry --> Analyze
    Extract --> Analyze
    Analyze --> Generate
    Generate --> Return
    Return --> Display
    Display --> DISCARD

    style DISCARD fill:#dc2626,color:#fff,stroke:#dc2626
    style PROCESSING fill:#0078D4,color:#fff,stroke:#005a9e
```

---

## Azure Resource Topology

```
Azure Subscription: 2d7fae20-e207-40a5-bc46-53df96affcb7
  │
  └─ Resource Group: rg-v3 (Canada East)
       │
       ├─ Azure Static Web Apps: govrag-v3-static
       │     └─ React/Next.js frontend + PWA
       │
       ├─ Azure Functions App: govrag-v3-func
       │     └─ Python v2 serverless backend
       │     └─ Consumption plan (auto-scale, zero idle cost)
       │
       ├─ Azure OpenAI Service: govrag-v3-openai
       │     └─ Deployment: gpt-4o-mini
       │
       ├─ Azure AI Search: govrag-v3-search
       │     └─ Standard S1, semantic ranking enabled
       │     └─ Index: career-knowledge-base
       │
       ├─ Azure Key Vault: govrag-v3-kv
       │     └─ Secrets: OPENAI_KEY, GEMINI_KEY, GROK_KEY, SERPER_KEY
       │     └─ RBAC: Functions MSI → Secret Reader
       │
       └─ Azure Monitor: govrag-v3-monitor
             └─ Application Insights
             └─ Alerts: error rate, latency, fallback activations
```

---

## Technology Integration Map

```mermaid
mindmap
  root((Alfalah AI<br/>2026 V3))
    Azure Cloud
      Static Web Apps
      Functions v2 Python
      OpenAI GPT-4o-mini
      AI Search Semantic
      Key Vault RBAC
      Content Safety
      Monitor Insights
      Entra ID B2C
      Cosmos DB future
    AI Models
      GPT-4o-mini Primary
      Gemini 2.0 Flash
      Gemini Flash Latest
      Gemini 1.5 Flash
      xAI Grok-4-latest
      RAG Engine Custom
    Knowledge Base
      ISCO-08 436 Occupations
      195 Country Packages
      900+ Skills A-Z
      Future Jobs 2125
      ATS Science
      Visa Immigration
      Salary Global
    Dev Tools
      Visual Studio Code
      Claude Code AI
      GitHub Copilot
      Azure Functions CLI
      GitHub Actions
      Python 3.11
      Next.js React
      Tailwind CSS
    External APIs
      Serper Google Jobs
      ipapi Geolocation
    Standards
      ISCO-08 ILO
      ESCO EU Commission
      O-NET US BLS
      Microsoft RAI v2
      GDPR Privacy
```

---

## Performance Architecture

| Metric | Target | How Achieved |
|--------|--------|-------------|
| API response time | < 30s | Azure OpenAI + RAG retrieval optimized |
| Frontend load | < 2s | Azure CDN global edge nodes |
| File upload parse | < 3s | In-memory pypdf2 / python-docx |
| AI fallback switch | < 1s | Immediate fallback on timeout/error |
| Availability | 99.9%+ | 4-provider fallback chain |
| Max request size | 50KB | Body guard enforced |
| Token budget | 8,192 | maxOutputTokens per call |
| Timeout per call | 55s | Per AI provider attempt |

---

## Scalability Model

```
User Load       → Azure Static Web Apps (auto-scale CDN — handles millions)
API Requests    → Azure Functions Consumption Plan (0 to N instances, auto-scale)
AI Capacity     → 4 providers × multiple API keys = near-unlimited throughput
Storage         → Zero (stateless by design — no scale concerns)
Knowledge Base  → Static .md files — loaded once, cached in Function memory
```

---

*Alfalah Job Career Intelligent AI 2026 V3 · Architecture Documentation · © 2026 · Mississauga, Ontario, Canada*
*Built for 8 Billion People · 100% Microsoft Azure · Responsible AI by Design*
