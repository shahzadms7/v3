"""
GovRAG V3 — FastAPI Backend (Main Application)
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
This is the MAIN ENTRY POINT of the entire application.
FastAPI gives us:
  - /api/query — Ask a question (compliance or career)
  - /api/career/analyze — Resume analysis with RAG grounding
  - /api/health — Health check (for Azure monitoring)
  - /api/metrics — Dashboard metrics (audit trail)
  - /docs — Auto-generated API documentation (judges love this)

FLOW:
  User → FastAPI → RAG Engine → AI Provider → Safety Engine → Response

PRIVACY: Zero data stored. Everything in-memory only.
"""

import time
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from ..core.config import settings
from ..core.rag_engine import rag_engine
from ..core.ai_provider import ai_provider, AIProvider
from ..core.safety_engine import safety_engine
from ..core.audit_logger import audit_logger

# ── Create FastAPI app ────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",        # Swagger UI — judges see this
    redoc_url="/redoc",      # Alternative docs
)

# ── CORS (allow frontend to call API) ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load documents on startup ─────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    """Load all documents into RAG index when app starts."""
    print(f"[GovRAG] Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    rag_engine.load_documents()
    print(f"[GovRAG] RAG index ready: {rag_engine.stats}")


# ── Request/Response Models ───────────────────────────────────────────────────
class QueryRequest(BaseModel):
    """What the user sends."""
    query: str = Field(..., max_length=2000, description="The question to ask")
    mode: str = Field("auto", description="Mode: 'compliance', 'career', or 'auto'")

class CareerAnalyzeRequest(BaseModel):
    """Resume analysis request — NEVER stored."""
    resume: str = Field(..., max_length=8000, description="Resume text (never stored)")
    job_description: str = Field("", max_length=4000, description="Job description (optional)")
    analysis_type: str = Field("full", description="Type: full, ats_score, skills_gap, rewrite")
    country: str = Field("", max_length=100, description="User's country")
    industry: str = Field("", max_length=100, description="User's industry")


# ── Endpoint: /api/query ──────────────────────────────────────────────────────
@app.post("/api/query")
async def query(req: QueryRequest):
    """
    Ask a grounded question. Every answer cites sources.
    Privacy: Query is NEVER stored. Only metrics are logged.
    """
    start = time.time()

    # Gate 1: Input safety
    input_check = safety_engine.check_input(req.query)
    if not input_check["passed"]:
        audit_logger.log(verdict="BLOCK", mode=req.mode, latency_ms=int((time.time()-start)*1000))
        raise HTTPException(status_code=400, detail={"error": "Query blocked by safety check", "issues": input_check["issues"]})

    # Retrieve relevant chunks
    doc_type = None if req.mode == "auto" else req.mode
    retrieval = rag_engine.retrieve(req.query, doc_type=doc_type)

    # Gate 2: Relevance check
    relevance = safety_engine.check_relevance(retrieval)
    if not relevance["passed"]:
        audit_logger.log(verdict="BLOCK", mode=req.mode, sources_count=0, latency_ms=int((time.time()-start)*1000))
        return {
            "answer": relevance["message"],
            "grounded": False, "confidence": 0, "faithfulness": 0,
            "sources": [], "warnings": ["No relevant documents found."],
            "metrics": {"retrieval_time_ms": retrieval["retrieval_time_ms"]},
        }

    # Generate grounded answer
    prompt = rag_engine.build_grounded_prompt(req.query, retrieval["chunks"])
    ai_result = await ai_provider.generate(prompt["system"], prompt["user"])
    parsed = AIProvider.extract_json(ai_result["text"])
    answer_text = parsed.get("answer", ai_result["text"])
    ai_confidence = parsed.get("confidence", 50)

    # Verify faithfulness
    faithfulness = rag_engine.verify_faithfulness(answer_text, retrieval["chunks"])

    # Gate 3: Confidence check
    conf_check = safety_engine.check_confidence(faithfulness["faithfulness_score"], ai_confidence)
    warnings = parsed.get("warnings", [])

    if not conf_check["passed"]:
        audit_logger.log(
            verdict="BLOCK", confidence=conf_check["score"],
            faithfulness=faithfulness["faithfulness_score"],
            sources_count=retrieval["total"], provider=ai_result["provider"],
            model=ai_result["model"], mode=req.mode,
            latency_ms=int((time.time()-start)*1000),
        )
        return {
            "answer": conf_check["message"],
            "grounded": False, "confidence": conf_check["score"],
            "faithfulness": faithfulness["faithfulness_score"],
            "sources": rag_engine.build_citation_map(retrieval["chunks"]),
            "warnings": ["Answer blocked due to low confidence."],
            "metrics": {"retrieval_time_ms": retrieval["retrieval_time_ms"],
                        "generation_time_ms": 0, "total_latency_ms": int((time.time()-start)*1000)},
        }

    if conf_check["action"] == "WARN":
        warnings.append(conf_check["message"])

    total_ms = int((time.time() - start) * 1000)

    # Audit log (metrics only, NEVER query text)
    audit_id = audit_logger.log(
        verdict="ALLOW" if conf_check["action"] == "ALLOW" else "WARN",
        confidence=conf_check["score"],
        faithfulness=faithfulness["faithfulness_score"],
        sources_count=retrieval["total"],
        provider=ai_result["provider"], model=ai_result["model"],
        latency_ms=total_ms, warnings=warnings, mode=req.mode,
    )

    return {
        "answer": answer_text,
        "grounded": True,
        "confidence": conf_check["score"],
        "faithfulness": faithfulness["faithfulness_score"],
        "sources": rag_engine.build_citation_map(retrieval["chunks"]),
        "key_facts": parsed.get("key_facts", []),
        "warnings": warnings,
        "metrics": {
            "faithfulness": faithfulness["faithfulness_score"],
            "confidence": conf_check["score"],
            "total_claims": faithfulness["total_claims"],
            "grounded_claims": faithfulness["grounded"],
            "retrieval_time_ms": retrieval["retrieval_time_ms"],
            "total_latency_ms": total_ms,
            "provider": ai_result["provider"],
            "model": ai_result["model"],
        },
        "audit_id": audit_id,
    }


# ── Endpoint: /api/career/analyze ─────────────────────────────────────────────
@app.post("/api/career/analyze")
async def career_analyze(req: CareerAnalyzeRequest):
    """
    Analyze a resume with RAG-grounded career intelligence.
    Privacy: Resume is NEVER stored. Only processed in-memory.
    """
    start = time.time()

    # Build career-specific query from resume + job description
    query_parts = [f"Resume analysis for {req.industry or 'general'} industry"]
    if req.country:
        query_parts.append(f"in {req.country}")
    query_parts.append(req.analysis_type)

    # Search career documents
    career_query = " ".join(query_parts) + " " + req.resume[:500]
    retrieval = rag_engine.retrieve(career_query, doc_type="career", top_k=7)

    # Build career-specific prompt
    chunks = retrieval["chunks"]
    context = "\n\n".join([f"[Source {i+1}: {c.source}, {c.section}]\n{c.content}" for i, c in enumerate(chunks)])

    system_prompt = f"""You are GovRAG Career Intelligence — the world's top career advisor.
You serve 8 billion humans. You make every candidate stand in the TOP 1% of the world.

METHODOLOGY (Top Recruiter 3-Step):
STEP 1 — 6-second skim: What is NOTICED vs MISSED in top third of resume?
STEP 2 — Measurable wins: Every bullet needs a NUMBER (%, $, time, team size, revenue)
STEP 3 — Reorder: Top 3 strongest results in first half of page 1

ANALYSIS TYPE: {req.analysis_type}
COUNTRY: {req.country or 'Global'}
INDUSTRY: {req.industry or 'General'}

Use the CAREER INTELLIGENCE DATA below to ground your advice.
Cite sources for salary data, certification recommendations, and market insights.

CAREER INTELLIGENCE DATA:
{context}

RESPOND IN JSON:
{{
  "analysis_type": "{req.analysis_type}",
  "score": 0-100,
  "summary": "2-3 sentence overview",
  "strengths": ["strength 1 [Source N]"],
  "weaknesses": ["weakness 1"],
  "missing_skills": ["skill 1"],
  "recommended_certs": ["cert [Source N]"],
  "action_items": ["action 1", "action 2"],
  "rewritten_bullets": ["improved bullet 1"],
  "market_insight": "relevant market data [Source N]",
  "confidence": 85
}}"""

    user_prompt = f"""RESUME:
{req.resume}

{f'JOB DESCRIPTION: {req.job_description}' if req.job_description else ''}

Analyze this resume. Be brutally honest. Find every weakness, missing skill, red flag, blind spot.
Make this candidate TOP 1%. Cite career intelligence sources. Return JSON."""

    ai_result = await ai_provider.generate(system_prompt, user_prompt)
    parsed = AIProvider.extract_json(ai_result["text"])

    total_ms = int((time.time() - start) * 1000)

    audit_logger.log(
        verdict="ALLOW", confidence=parsed.get("confidence", 50),
        faithfulness=0, sources_count=len(chunks),
        provider=ai_result["provider"], model=ai_result["model"],
        latency_ms=total_ms, mode="career",
    )

    return {
        "analysis": parsed,
        "sources": rag_engine.build_citation_map(chunks),
        "metrics": {"total_latency_ms": total_ms, "provider": ai_result["provider"], "model": ai_result["model"]},
        "privacy": "Your resume was NOT stored. Data erased from memory after this response.",
    }


# ── Endpoint: /api/health ─────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    """Health check — Azure Monitor uses this."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "rag_index": rag_engine.stats,
        "ai_providers": len(ai_provider.providers),
        "privacy": "Zero data storage. No database. No PII logged.",
    }


# ── Endpoint: /api/metrics ────────────────────────────────────────────────────
@app.get("/api/metrics")
async def metrics():
    """Dashboard metrics — audit trail summary."""
    return {
        "metrics": audit_logger.get_metrics(),
        "recent": audit_logger.get_recent(20),
    }


# ── Endpoint: /api/sources ────────────────────────────────────────────────────
@app.get("/api/sources")
async def list_sources():
    """List all indexed document sources."""
    return {
        "stats": rag_engine.stats,
        "sources": list(set(c.source for c in rag_engine.chunks)),
    }
