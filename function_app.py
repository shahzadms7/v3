"""
GovRAG V3 — Azure Functions Serverless (v2 decorator model)
Created: March 22, 2026 | Microsoft Hackathon
100% Python | Serverless | No containers | No timeouts
"""

import azure.functions as func
import json
import re
import time
import os
import asyncio
import httpx
from pathlib import Path

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ── Globals (lazy loaded on first request) ────────────────────────────────────
_chunks = None
_word_index = None
_chunk_freqs = None

STOP_WORDS = {'the','a','an','is','are','was','were','be','been','have','has','had',
              'do','does','did','will','would','shall','should','may','might','must',
              'can','could','to','of','in','for','on','with','at','by','from','as',
              'and','but','or','nor','not','so','very','just','also','this','that',
              'these','those','it','its','all','each','every','both','few','more',
              'most','other','some','such','only','own','same','than','too','about'}


def _load_rag():
    global _chunks, _word_index, _chunk_freqs
    if _chunks is not None:
        return
    _chunks = []
    data_dir = Path(__file__).parent / "data"
    for sub in ["career", "compliance"]:
        sub_dir = data_dir / sub
        if not sub_dir.exists():
            continue
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
                _chunks.append({"content": body or section.strip(), "source": source,
                                "section": title, "type": sub, "idx": i})
    _chunk_freqs = []
    for chunk in _chunks:
        text = f"{chunk['section']} {chunk['content']}".lower()
        words = [w for w in re.findall(r'\b[a-z]{3,}\b', text) if w not in STOP_WORDS]
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        _chunk_freqs.append(freq)
    import logging
    logging.info(f"[GovRAG] Loaded {len(_chunks)} chunks")


def _search(query, top_k=5, doc_type=None):
    _load_rag()
    terms = set(re.findall(r'\b[a-z]{3,}\b', query.lower()))
    scores = []
    for i, chunk in enumerate(_chunks):
        if doc_type and chunk["type"] != doc_type:
            continue
        freq = _chunk_freqs[i]
        score = sum(freq.get(t, 0) for t in terms)
        if score > 0:
            total = sum(freq.values()) or 1
            scores.append((i, round(score / (total ** 0.5), 4)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [{"chunk": _chunks[i], "score": s} for i, s in scores[:top_k]]


# ── Azure AI Search ───────────────────────────────────────────────────────────
_az_search_indexed = False

def _ensure_azure_search_index():
    global _az_search_indexed
    if _az_search_indexed:
        return
    _load_rag()
    endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
    key = os.environ.get("AZURE_SEARCH_KEY", "")
    if not endpoint or not key:
        return
    import hashlib, logging
    idx = os.environ.get("AZURE_SEARCH_INDEX", "career-knowledge")
    api_ver = "2024-07-01"
    hdrs = {"api-key": key, "Content-Type": "application/json"}

    index_def = {
        "name": idx,
        "fields": [
            {"name": "id",       "type": "Edm.String", "key": True, "searchable": False},
            {"name": "content",  "type": "Edm.String", "searchable": True, "analyzer": "en.microsoft"},
            {"name": "source",   "type": "Edm.String", "searchable": True, "filterable": True},
            {"name": "section",  "type": "Edm.String", "searchable": True},
            {"name": "doc_type", "type": "Edm.String", "filterable": True},
        ]
    }
    try:
        httpx.put(f"{endpoint}/indexes/{idx}?api-version={api_ver}", headers=hdrs, json=index_def, timeout=30.0)
    except Exception as e:
        logging.warning(f"[AzSearch] Index create: {e}")
        return

    batch = []
    for chunk in (_chunks or []):
        doc_id = hashlib.md5(f"{chunk['source']}-{chunk['idx']}".encode()).hexdigest()
        batch.append({
            "@search.action": "mergeOrUpload",
            "id":       doc_id,
            "content":  chunk["content"][:4000],
            "source":   chunk["source"],
            "section":  chunk["section"][:200],
            "doc_type": chunk["type"],
        })
        if len(batch) >= 100:
            try:
                httpx.post(f"{endpoint}/indexes/{idx}/docs/index?api-version={api_ver}", headers=hdrs, json={"value": batch}, timeout=30.0)
            except Exception:
                pass
            batch = []
    if batch:
        try:
            httpx.post(f"{endpoint}/indexes/{idx}/docs/index?api-version={api_ver}", headers=hdrs, json={"value": batch}, timeout=30.0)
        except Exception:
            pass
    _az_search_indexed = True
    logging.info(f"[AzSearch] Indexed {len(_chunks or [])} chunks → {idx}")


def _search_azure(query, top_k=7, doc_type=None):
    endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
    key      = os.environ.get("AZURE_SEARCH_KEY", "")
    if not endpoint or not key:
        return _search(query, top_k=top_k, doc_type=doc_type)

    import logging
    _ensure_azure_search_index()
    idx     = os.environ.get("AZURE_SEARCH_INDEX", "career-knowledge")
    api_ver = "2024-07-01"
    hdrs    = {"api-key": key, "Content-Type": "application/json"}
    body    = {"search": query, "top": top_k, "queryType": "simple"}
    if doc_type:
        body["filter"] = f"doc_type eq '{doc_type}'"
    try:
        r = httpx.post(f"{endpoint}/indexes/{idx}/docs/search?api-version={api_ver}", headers=hdrs, json=body, timeout=10.0)
        if r.status_code == 200:
            return [
                {"chunk": {"content": h.get("content",""), "source": h.get("source",""),
                           "section": h.get("section",""), "type": h.get("doc_type","career"), "idx": 0},
                 "score": round(h.get("@search.score", 1.0), 4), "via": "azure_search"}
                for h in r.json().get("value", [])
            ]
    except Exception as e:
        logging.warning(f"[AzSearch] Search fallback: {e}")
    return _search(query, top_k=top_k, doc_type=doc_type)


def _check_content_safety(text):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    key      = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        return True, "not_configured"
    import logging
    try:
        r = httpx.post(
            f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={"text": text[:5000], "categories": ["Hate","Violence","SelfHarm","Sexual"],
                  "outputType": "FourSeverityLevels"},
            timeout=5.0
        )
        if r.status_code == 200:
            for cat in r.json().get("categoriesAnalysis", []):
                if cat.get("severity", 0) >= 4:
                    return False, f"Content moderated by Azure Content Safety: {cat['category']}"
        return True, "safe"
    except Exception as e:
        logging.warning(f"[ContentSafety] {e}")
        return True, "unavailable"

# ── ASYNC AI CALLER (SPEED OPTIMIZED) ─────────────────────────────────────────
async def _call_ai_async(system, user):
    """Asynchronous call to Azure OpenAI — drastically reduces execution time."""
    import logging
    az_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    az_key      = os.environ.get("AZURE_OPENAI_KEY", "")
    az_deploy   = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    
    if not az_endpoint or not az_key:
        logging.error("[GovRAG] AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_KEY not set")
        return {"text": "Azure OpenAI not configured.", "provider": "none", "model": "none"}
        
    url = f"{az_endpoint}/openai/deployments/{az_deploy}/chat/completions?api-version=2024-08-01-preview"
    headers = {"api-key": az_key, "Content-Type": "application/json"}
    payload = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ], 
        "temperature": 0.3, 
        "max_tokens": 8192
    }
    
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            
            if resp.status_code == 200:
                text = resp.json()["choices"][0]["message"]["content"]
                return {"text": text, "provider": "Azure OpenAI", "model": az_deploy}
                
            err = f"HTTP {resp.status_code} — {resp.text[:200]}"
            logging.error(f"[GovRAG] Azure OpenAI error: {err}")
            return {"text": f"Azure OpenAI unavailable: {err}", "provider": "none", "model": "none"}
            
    except Exception as e:
        logging.error(f"[GovRAG] Azure OpenAI async exception: {str(e)}")
        return {"text": f"Azure OpenAI error: {str(e)[:150]}", "provider": "none", "model": "none"}

# Keep the sync version for endpoints not yet converted to async
def _call_ai(system, user):
    return asyncio.run(_call_ai_async(system, user))

def _parse_json(text):
    try: return json.loads(text)
    except: pass
    m = re.search(r'
http://googleusercontent.com/immersive_entry_chip/0
This will trigger your GitHub Actions pipeline and automatically deploy the fix to your Azure Function!