# GovRAG V3 — Grounded Knowledge Assistant for Regulated Teams + Career Intelligence

> **Microsoft Hackathon 2026 | 100% Azure Cloud | 100% Python | Zero Data Storage**

A governed RAG system that answers compliance-critical questions AND serves as a career intelligence platform for 8 billion humans — with source citations, safety checks, hallucination metrics, and full audit trails.

## Architecture

```
Azure App Service (Free) ─── FastAPI + Streamlit (100% Python)
       │
       ├── RAG Engine ─── Azure AI Search (semantic retrieval)
       │                      └── Career + Compliance documents
       ├── AI Provider ─── Gemini (free) → Grok (fallback)
       ├── Safety Engine ── 3-gate validation (input → relevance → confidence)
       ├── Audit Logger ─── Azure Monitor (no PII, metrics only)
       └── Key Vault ────── All secrets (zero keys in code)
```

## Key Principles

- **Zero data storage** — User data lives only in memory during request. Refresh = gone forever
- **Every answer cites sources** — `[Source N]` with clickable verification
- **3-layer safety** — Input gate → Relevance gate → Confidence gate
- **Faithfulness score** — Real-time 0-100% hallucination detection
- **Multi-AI fallback** — Gemini Key1 → Key2 → Grok (enterprise resilience)
- **195 countries** — Career intelligence for all humanity
- **Dual mode** — Compliance (policies/SOPs) + Career (resume/jobs/skills)

## Azure Services (all free tier)

| Service | Purpose |
|---------|---------|
| App Service (F1) | Host Python application |
| AI Search (Free) | Document indexing + RAG retrieval |
| Blob Storage | Document file storage |
| Key Vault | Secrets management |
| Monitor + App Insights | Audit trail + observability |

## Team

| Role | Name |
|------|------|
| Principal Solution Architect | Shahzad Muhammad |
| AI Engineering | Claude Opus 4.6 |
| Student Learner | Zara (age 12) |

## Tech Stack

- **Language**: 100% Python
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI**: Gemini + Grok (free tier, multi-provider fallback)
- **Infrastructure**: Azure (Bicep IaC)
- **CI/CD**: GitHub Actions
- **SDLC**: DevSecOps pipeline

---

*Built for the Microsoft Hackathon 2026 — Mississauga, Ontario, Canada*
