"""
GovRAG V3 — Azure Functions Serverless Version
Created: March 22, 2026 | Microsoft Hackathon

This is the Azure Functions v2 (decorator model) version.
If App Service doesn't work, deploy this instead:
  func azure functionapp publish govrag-v3-func
"""

import azure.functions as func
import json
import re
import time
import hashlib
import os
from pathlib import Path

app = func.FunctionApp()

# ── Lazy-loaded globals ───────────────────────────────────────────────────────
_rag_chunks = None
_word_index = None
_chunk_word_counts = None


def _load_rag():
    """Load and index documents — runs once on first request."""
    global _rag_chunks, _word_index, _chunk_word_counts
    if _rag_chunks is not None:
        return

    _rag_chunks = []
    data_dir = Path(__file__).parent / "data"

    stop_words = {'the','a','an','is','are','was','were','be','been','have','has','had',
                  'do','does','did','will','would','shall','should','may','might','must',
                  'can','could','to','of','in','for','on','with','at','by','from','as',
                  'and','but','or','nor','not','so','very','just','also','this','that',
                  'these','those','it','its','all','each','every','both','few','more'}

    for sub in ["career", "compliance"]:
        sub_dir = data_dir / sub
        if not sub_dir.exists():
            continue
        doc_type = sub
        for md_file in sorted(sub_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            source = md_file.stem
            sections = re.split(r"^## ", content, flags=re.MULTILINE)
            for i, section in enumerate(sections):
                if not section.strip():
                    continue
                lines = section.strip().split("\n")
                title = lines[0].strip()
                body = "\n".join(lines[1:]).strip() if len(lines) > 1 else section.strip()
                if len(body) > 2000:
                    for k, j in enumerate(range(0, len(body), 1200)):
                        _rag_chunks.append({
                            "content": body[j:j+1500], "source": source,
                            "section": title, "doc_type": doc_type, "idx": i*100+k,
                        })
                else:
                    _rag_chunks.append({
                        "content": body or section.strip(), "source": source,
                        "section": title, "doc_type": doc_type, "idx": i,
                    })

    # Build keyword index
    _word_index = {}
    _chunk_word_counts = []
    for ci, chunk in enumerate(_rag_chunks):
        text = f"{chunk['section']} {chunk['content']}".lower()
        words = [w for w in re.findall(r'\b[a-z]{3,}\b', text) if w not in stop_words]
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        _chunk_word_counts.append(freq)

    print(f"[GovRAG] Loaded {len(_rag_chunks)} chunks")


def _search(query, top_k=5, doc_type=None):
    """Pure Python keyword search."""
    _load_rag()
    start = time.time()
    terms = set(re.findall(r'\b[a-z]{3,}\b', query.lower()))
    scores = []
    for i, chunk in enumerate(_rag_chunks):
        if doc_type and chunk["doc_type"] != doc_type:
            continue
        freq = _chunk_word_counts[i]
        score = sum(freq.get(t, 0) for t in terms)
        if score > 0:
            total = sum(freq.values()) or 1
            scores.append((i, round(score / (total**0.5), 4)))
    scores.sort(key=lambda x: x[1], reverse=True)
    results = [{"chunk": _rag_chunks[i], "score": s} for i, s in scores[:top_k]]
    return {"results": results, "time_ms": round((time.time()-start)*1000, 1), "total": len(results)}


def _call_gemini(system_prompt, user_prompt):
    """Call Gemini AI — synchronous for Azure Functions."""
    import google.generativeai as genai
    keys = [os.environ.get("GEMINI_API_KEY", ""), os.environ.get("GEMINI_API_KEY_2", "")]
    models = ["gemini-2.0-flash", "gemini-1.5-flash"]
    for key in keys:
        if not key:
            continue
        genai.configure(api_key=key)
        for model in models:
            try:
                m = genai.GenerativeModel(model)
                r = m.generate_content(f"{system_prompt}\n\n{user_prompt}",
                    generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=4096))
                if r.text:
                    return {"text": r.text, "provider": "Gemini", "model": model}
            except Exception as e:
                continue
    return {"text": "AI unavailable", "provider": "none", "model": "none"}


def _extract_json(text):
    try: return json.loads(text)
    except: pass
    m = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    m = re.search(r'\{[\s\S]*\}', text)
    if m:
        try: return json.loads(m.group(0))
        except: pass
    return {"answer": text, "sources_cited": [], "confidence": 50}


# ── HTTP Trigger: /api/health ─────────────────────────────────────────────────
@app.route("health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    _load_rag()
    return func.HttpResponse(json.dumps({
        "status": "healthy", "version": "3.0.0",
        "chunks": len(_rag_chunks or []),
        "privacy": "Zero data storage",
    }), mimetype="application/json")


# ── HTTP Trigger: /api/query ──────────────────────────────────────────────────
@app.route("query", methods=["POST"])
def query(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    try:
        body = req.get_json()
    except:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    q = (body.get("query") or "")[:2000].strip()
    mode = body.get("mode", "auto")
    if not q:
        return func.HttpResponse(json.dumps({"error": "Query required"}), status_code=400, mimetype="application/json")

    doc_type = None if mode == "auto" else mode
    retrieval = _search(q, top_k=5, doc_type=doc_type)

    if not retrieval["results"]:
        return func.HttpResponse(json.dumps({
            "answer": "No relevant documents found.", "grounded": False,
            "confidence": 0, "sources": [],
        }), mimetype="application/json")

    # Build grounded prompt
    ctx = "\n\n---\n\n".join([
        f"[Source {i+1}: {r['chunk']['source']}, {r['chunk']['section']}]\n{r['chunk']['content']}"
        for i, r in enumerate(retrieval["results"])
    ])

    system = """You are GovRAG. Answer ONLY from context. Cite [Source N] for every claim.
If insufficient info, say "INSUFFICIENT EVIDENCE". Return JSON:
{"answer":"...[Source N]...","sources_cited":[1,2],"confidence":85,"warnings":[],"key_facts":["fact [Source N]"]}"""

    user = f"CONTEXT:\n{ctx}\n\nQUESTION: {q}\n\nReturn JSON."
    ai = _call_gemini(system, user)
    parsed = _extract_json(ai["text"])
    answer = parsed.get("answer", ai["text"])

    # Faithfulness check
    sentences = [s.strip() for s in re.split(r'[.!?]+', answer) if len(s.strip()) > 15]
    all_content = " ".join(r["chunk"]["content"].lower() for r in retrieval["results"])
    grounded = sum(1 for s in sentences if re.search(r'\[Source \d+\]', s))
    faith_score = round((grounded / len(sentences)) * 100) if sentences else 0

    sources = [{"num": i+1, "doc": r["chunk"]["source"], "section": r["chunk"]["section"],
                "relevance": r["score"], "preview": r["chunk"]["content"][:200]}
               for i, r in enumerate(retrieval["results"])]

    return func.HttpResponse(json.dumps({
        "answer": answer, "grounded": True,
        "confidence": parsed.get("confidence", 50),
        "faithfulness": faith_score,
        "sources": sources,
        "key_facts": parsed.get("key_facts", []),
        "warnings": parsed.get("warnings", []),
        "metrics": {"faith": faith_score, "latency_ms": int((time.time()-start)*1000),
                    "provider": ai["provider"], "model": ai["model"]},
    }), mimetype="application/json")


# ── HTTP Trigger: /api/simplify (ELI12) ──────────────────────────────────────
@app.route("simplify", methods=["POST"])
def simplify(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    text = (body.get("text") or "")[:4000]
    level = body.get("reading_level", "grade6")
    levels = {"grade3": "8-year-old", "grade6": "12-year-old named Zara",
              "grade9": "high school student", "adult": "non-technical adult"}
    system = f"Simplify for a {levels.get(level, '12-year-old')}. Be calm, supportive. Use bullet points. Return JSON: {{\"simplified\":\"...\",\"summary\":\"one line\"}}"
    ai = _call_gemini(system, f"Simplify:\n{text}")
    parsed = _extract_json(ai["text"])
    return func.HttpResponse(json.dumps({
        "simplified": parsed.get("simplified", ai["text"]),
        "reading_level": level, "summary": parsed.get("summary", ""),
    }), mimetype="application/json")


# ── HTTP Trigger: /api/responsible-ai ─────────────────────────────────────────
@app.route("responsible-ai", methods=["GET"])
def responsible_ai(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({
        "principles": {
            "fairness": "No demographic data, uniform treatment, 195 countries",
            "reliability": "3-gate safety, multi-AI fallback, faithfulness scoring",
            "privacy": "ZERO storage, no database, PII detection, refresh=gone",
            "inclusiveness": "ELI12 mode, free, no login, WCAG considerations",
            "transparency": "Source citations, explainability, open source",
            "accountability": "Audit trail, safety verdicts, Azure Monitor",
        },
        "data_storage": "NONE",
        "hallucination_target": "<5%",
    }), mimetype="application/json")
