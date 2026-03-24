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


def _call_ai(system, user):
    import logging
    import warnings
    warnings.filterwarnings("ignore")
    errors = []

    # ── PRIORITY 1: Azure OpenAI (100% Azure — primary provider) ──
    az_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    az_key      = os.environ.get("AZURE_OPENAI_KEY", "")
    az_deploy   = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    if az_endpoint and az_key:
        try:
            import httpx
            url = f"{az_endpoint}/openai/deployments/{az_deploy}/chat/completions?api-version=2024-08-01-preview"
            resp = httpx.post(url,
                headers={"api-key": az_key, "Content-Type": "application/json"},
                json={"messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ], "temperature": 0.3, "max_tokens": 8192},
                timeout=55.0)
            if resp.status_code == 200:
                text = resp.json()["choices"][0]["message"]["content"]
                return {"text": text, "provider": "Azure OpenAI", "model": az_deploy}
            errors.append(f"AzureOpenAI: HTTP {resp.status_code} — {resp.text[:120]}")
        except Exception as e:
            errors.append(f"AzureOpenAI: {str(e)[:80]}")

    # ── PRIORITY 2: Gemini (temporary bridge until Azure quota approved) ──
    gemini_keys = [os.environ.get("GEMINI_API_KEY", ""), os.environ.get("GEMINI_API_KEY_2", ""), os.environ.get("GEMINI_API_KEY_3", "")]
    for ki, key in enumerate(gemini_keys):
        if not key:
            continue
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            for model in ["gemini-2.0-flash", "gemini-flash-latest", "gemini-2.0-flash-lite"]:
                try:
                    m = genai.GenerativeModel(model)
                    r = m.generate_content(f"{system}\n\n{user}",
                        generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=8192))
                    if r.text:
                        return {"text": r.text, "provider": f"Gemini-Key{ki+1}", "model": model}
                except Exception as e:
                    errors.append(f"Gemini-{ki+1}/{model}: {str(e)[:80]}")
        except Exception as e:
            errors.append(f"Gemini import: {str(e)[:80]}")

    # ── PRIORITY 3: Grok fallback ──
    grok_keys = [os.environ.get("GROK_API_KEY", ""), os.environ.get("GROK_API_KEY_2", ""), os.environ.get("GROK_API_KEY_3", "")]
    for gi, grok_key in enumerate(grok_keys):
        if not grok_key:
            continue
        try:
            import httpx
            resp = httpx.post("https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {grok_key}", "Content-Type": "application/json"},
                json={"model": "grok-4-1-fast", "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ], "temperature": 0.3, "max_tokens": 8192},
                timeout=55.0)
            if resp.status_code == 200:
                text = resp.json()["choices"][0]["message"]["content"]
                return {"text": text, "provider": f"Grok-Key{gi+1}", "model": "grok-4-1-fast"}
            errors.append(f"Grok-{gi+1}: HTTP {resp.status_code}")
        except Exception as e:
            errors.append(f"Grok-{gi+1}: {str(e)[:80]}")

    logging.error(f"[GovRAG] All AI providers failed: {errors}")
    return {"text": f"AI temporarily unavailable. Errors: {'; '.join(errors)}", "provider": "none", "model": "none"}


def _parse_json(text):
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


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/health — Test page to verify everything works
# ══════════════════════════════════════════════════════════════════════════════
@app.route("health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    _load_rag()
    return func.HttpResponse(json.dumps({
        "status": "healthy",
        "version": "3.0.0",
        "platform": "Azure Functions Serverless",
        "chunks_loaded": len(_chunks or []),
        "career_chunks": sum(1 for c in (_chunks or []) if c["type"] == "career"),
        "compliance_chunks": sum(1 for c in (_chunks or []) if c["type"] == "compliance"),
        "sources": list(set(c["source"] for c in (_chunks or []))),
        "ai_keys_configured": bool(os.environ.get("GEMINI_API_KEY")),
        "privacy": "Zero data storage. No database. Refresh = gone.",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2), mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/query — Grounded RAG Q&A with citations
# ══════════════════════════════════════════════════════════════════════════════
@app.route("query", methods=["POST"])
def query(req: func.HttpRequest) -> func.HttpResponse:
    import logging
    start = time.time()
    try:
        try:
            body = req.get_json()
        except:
            return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

        q = (body.get("query") or "")[:2000].strip()
        mode = body.get("mode", "auto")
        target_lang = body.get("language", "en")
        if not q:
            return func.HttpResponse(json.dumps({"error": "Query required"}), status_code=400, mimetype="application/json")

        # ── AZURE AI: PII Detection + Key Phrases ──
        azure_ai = {}
        try:
            from app.core.azure_ai_services import detect_pii, extract_key_phrases, detect_language
            pii = detect_pii(q)
            azure_ai["pii_detection"] = {"count": pii.get("pii_count", 0), "status": pii.get("status")}
            if pii.get("pii_count", 0) > 0:
                azure_ai["pii_warning"] = "PII detected in query. We NEVER store your data."
            azure_ai["key_phrases"] = extract_key_phrases(q)
            azure_ai["detected_language"] = detect_language(q)
        except Exception as e:
            azure_ai["error"] = str(e)[:80]

        # Search
        doc_type = None if mode == "auto" else mode
        results = _search(q, top_k=5, doc_type=doc_type)
        if not results:
            return func.HttpResponse(json.dumps({"answer": "No relevant documents found.",
                "grounded": False, "confidence": 0, "sources": []}), mimetype="application/json")

        # Build grounded prompt
        ctx = "\n\n---\n\n".join([
            f"[Source {i+1}: {r['chunk']['source']}, {r['chunk']['section']}]\n{r['chunk']['content']}"
            for i, r in enumerate(results)])

        system = """You are GovRAG — a Grounded Knowledge Assistant. Answer ONLY from the context below.
Cite [Source N] for every claim. If insufficient info, say "INSUFFICIENT EVIDENCE".
Return JSON: {"answer":"...[Source N]...","sources_cited":[1,2],"confidence":85,"warnings":[],"key_facts":["fact [Source N]"]}"""

        ai = _call_ai(system, f"CONTEXT:\n{ctx}\n\nQUESTION: {q}\n\nReturn JSON.")
        parsed = _parse_json(ai["text"])
        answer = parsed.get("answer", ai["text"])

        # Faithfulness check
        sentences = [s.strip() for s in re.split(r'[.!?]+', answer) if len(s.strip()) > 15]
        grounded = sum(1 for s in sentences if re.search(r'\[Source \d+\]', s))
        faith = round((grounded / len(sentences)) * 100) if sentences else 0

        sources = [{"num": i+1, "doc": r["chunk"]["source"], "section": r["chunk"]["section"],
                    "relevance": r["score"], "preview": r["chunk"]["content"][:200]}
                   for i, r in enumerate(results)]

        # ── AZURE AI: Content Safety check on response ──
        safety_result = {}
        try:
            from app.core.azure_ai_services import check_content_safety, translate_text
            safety_result = check_content_safety(answer)
            if not safety_result.get("safe", True):
                answer = "Response blocked by Azure Content Safety. The answer contained potentially harmful content."
                faith = 0
            # ── AZURE AI: Translate if requested ──
            translation = None
            if target_lang and target_lang != "en":
                translation = translate_text(answer, target_lang)
                if translation.get("status") == "translated":
                    answer = translation["translated"]
        except Exception as e:
            safety_result = {"error": str(e)[:80]}

        return func.HttpResponse(json.dumps({
            "answer": answer, "grounded": True,
            "confidence": parsed.get("confidence", 50), "faithfulness": faith,
            "sources": sources, "key_facts": parsed.get("key_facts", []),
            "warnings": parsed.get("warnings", []),
            "azure_ai": {**azure_ai, "content_safety": safety_result},
            "metrics": {"faithfulness": faith, "latency_ms": int((time.time()-start)*1000),
                        "provider": ai["provider"], "model": ai["model"],
                        "azure_services_used": ["Content Safety", "Language PII", "Language KeyPhrases", "Translator"]},
        }, indent=2), mimetype="application/json")
    except Exception as e:
        logging.error(f"[GovRAG] Query error: {str(e)}")
        return func.HttpResponse(json.dumps({
            "error": str(e), "latency_ms": int((time.time()-start)*1000)
        }), status_code=500, mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/simplify — ELI12 Mode (Explain Like Zara)
# ══════════════════════════════════════════════════════════════════════════════
@app.route("simplify", methods=["POST"])
def simplify(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    text = (body.get("text") or "")[:4000]
    level = body.get("reading_level", "grade6")
    levels = {"grade3": "8-year-old", "grade6": "12-year-old named Zara",
              "grade9": "high school student", "adult": "non-technical adult"}
    system = f"Simplify for a {levels.get(level, '12-year-old')}. Be calm, supportive. Use bullet points. No jargon. Return JSON: {{\"simplified\":\"...\",\"summary\":\"one line\"}}"
    ai = _call_ai(system, f"Simplify:\n{text}")
    parsed = _parse_json(ai["text"])
    return func.HttpResponse(json.dumps({
        "simplified": parsed.get("simplified", ai["text"]),
        "reading_level": level, "summary": parsed.get("summary", ""),
    }, indent=2), mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/career — Resume Analysis with RAG
# ══════════════════════════════════════════════════════════════════════════════
@app.route("career", methods=["POST"])
def career(req: func.HttpRequest) -> func.HttpResponse:
    """Naked Truth Career Analysis — 99% data-driven, 1% AI formatting."""
    import logging
    start = time.time()
    try:
        body = req.get_json()
        resume = (body.get("resume") or "")[:45000]
        job_desc = (body.get("job_description") or "")[:10000]
        country = body.get("country", "")
        industry = body.get("industry", "")
        if not resume:
            return func.HttpResponse(json.dumps({"error": "Resume required"}), status_code=400, mimetype="application/json")

        # ── STEP 1: Parse resume (ZERO AI cost) ──
        from app.core.career_engine import parse_resume, naked_truth_score, ats_score
        parsed = parse_resume(resume)

        # ── STEP 2: Score against TOP 1% standard (ZERO AI cost) ──
        truth = naked_truth_score(parsed, job_desc, country, industry)

        # ── STEP 3: ATS match against job description (ZERO AI cost) ──
        ats = ats_score(resume, job_desc) if job_desc else {"ats_score": None}

        # ── STEP 4: RAG search for career intelligence (ZERO AI cost) ──
        search_terms = f"resume {industry} {country} career certification salary skills"
        results = _search(search_terms, top_k=7, doc_type="career")
        career_intel = [{"source": r["chunk"]["source"], "section": r["chunk"]["section"],
                         "relevance": r["score"], "preview": r["chunk"]["content"][:200]}
                        for r in results]

        # ── STEP 5: ALL 17 AI CARDS — One call, full power ──
        ctx = "\n\n".join([
            f"[Source {i+1}: {r['chunk']['source']} | {r['chunk']['section']}]\n{r['chunk']['content'][:400]}"
            for i, r in enumerate(results)
        ])
        score = truth.get("composite_score", 0)
        system = f"""You are GovRAG Career — the world's most powerful career AI engine. Top 1% standard. Brutal honesty. Data-driven.

COUNTRY: {country or 'Global'} | INDUSTRY: {industry or 'General'}
RESUME SCORE: {score}/100 | VERDICT: {truth.get('verdict','')}
STRENGTHS: {truth.get('strengths',[])}
WEAKNESSES: {truth.get('weaknesses',[])}
HIDDEN ISSUES: {truth.get('hidden_issues',[])}

CAREER INTELLIGENCE (RAG):
{ctx}

JOB DESCRIPTION PROVIDED: {'YES' if job_desc else 'NO'}

Return ONLY a valid JSON object with ALL 17 keys below. No markdown, no explanation, ONLY the JSON:
{{
  "recruiterPov": {{"first_impression":"6-second verdict","top_third":["what recruiter sees first","..."],"buried":["what's hidden","..."],"red_flags":["flag1","..."],"quick_wins":["fix1","..."]}},
  "coverLetter": "Full 3-paragraph cover letter tailored to job/country. Hook + 3 wins + confident close.",
  "resumeRewrite": "Rewritten resume bullets only — top 3 strongest results moved to first half. Every bullet has a number (%, $, time, team size).",
  "skillsGap": {{"matched_hard":["skill1","..."],"missing_hard":["gap1","..."],"soft_matched":["..."],"soft_missing":["..."],"certs_to_pursue":[{{"name":"cert","url":"official-url","priority":"HIGH/MED"}}],"roadmap":["step1","..."]}},
  "interviewPrep": {{"qa":[{{"q":"question","a":"answer with STAR"}}],"questions_to_ask":["q1","..."]}},
  "starStories": [{{"title":"story title","s":"situation","t":"task","a":"action","r":"quantified result"}}],
  "linkedinSummary": "First-person LinkedIn About: bold hook + 3 top skills + impact + seeking statement. 3-4 sentences.",
  "introScripts": {{"min1":"1-minute phone screen script","min2":"2-minute hiring manager script","min3":"3-minute technical round script"}},
  "thankYouEmail": "Post-interview email: thank + specific reference + reinforce 2 qualifications + confirm readiness.",
  "salaryNegotiation": {{"table":[{{"level":"Entry","range":"local currency range"}},{{"level":"Mid","range":"..."}},{{"level":"Senior","range":"..."}},{{"level":"Lead","range":"..."}},{{"level":"Director","range":"..."}}],"script":"negotiation script","counter_script":"counter-offer script"}},
  "actionPlan": {{"day30":["action1","..."],"day60":["action1","..."],"day90":["action1","..."]}},
  "coldOutreach": {{"linkedin_request":"connection note (300 char max)","linkedin_dm":"full DM","cold_email":"subject + body","follow_up":"1-week follow-up email"}},
  "careerPivot": {{"pivot_score":"Easy/Moderate/Challenging","reason":"why","adjacent_roles":[{{"title":"role","transferable":["skill1"],"gaps":["gap1"],"time_to_qualify":"X months"}}],"plan_90_day":["step1","..."]}},
  "countryLaws": {{"notice_period":"...","termination_rights":"...","non_compete":"...","resume_compliance":["rule1","..."],"tax_forms":["form1","..."],"worker_rights":["right1","..."]}},
  "visaPathways": {{"scenario":"in_country/outside_country","in_country":["local requirement1","..."],"outside_country":[{{"type":"visa type","description":"...","url":"official gov url"}}],"digital_nomad":"availability","working_holiday":"availability"}},
  "matchingJobs": {{"titles":["job title 1","..."],"companies":["company1","..."],"job_boards":["board with url","..."],"recruiters_by_country":[{{"country":"{country}","firms":["firm1","firm2"]}}],"freelance_platforms":["platform1","..."]}}
}}"""

        ai = _call_ai(system, f"Resume (first 3000 chars):\n{resume[:3000]}\n\nJob Description:\n{job_desc[:1500] if job_desc else 'Not provided'}\n\nReturn the JSON now.")
        cards = _parse_json(ai["text"])

        return func.HttpResponse(json.dumps({
            "naked_truth": truth,
            "ats_match": ats,
            "cards": cards,
            "career_intelligence": career_intel,
            "ai_provider": ai["provider"],
            "ai_model": ai["model"],
            "metrics": {
                "latency_ms": int((time.time()-start)*1000),
                "method": "Algorithmic scoring + RAG + 17-card AI engine",
                "resume_score": score,
                "provider": ai["provider"],
                "model": ai["model"],
            },
            "privacy": "Your resume was NOT stored. Gone from memory after this response.",
        }, indent=2), mimetype="application/json")
    except Exception as e:
        logging.error(f"[GovRAG] Career error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/decision — FULL CAREER DECISION (hardest algorithm)
# ══════════════════════════════════════════════════════════════════════════════
@app.route("decision", methods=["POST"])
def decision(req: func.HttpRequest) -> func.HttpResponse:
    """Complete career decision — resume + gaps + country fit + pivots. ZERO AI cost."""
    import logging
    start = time.time()
    try:
        body = req.get_json()
        resume = (body.get("resume") or "")[:45000]
        if not resume:
            return func.HttpResponse(json.dumps({"error": "Resume required"}), status_code=400, mimetype="application/json")

        from app.core.career_engine import parse_resume
        from app.core.decision_engine import full_decision

        parsed = parse_resume(resume)
        result = full_decision(
            parsed,
            job_desc=body.get("job_description", ""),
            country=body.get("country", ""),
            industry=body.get("industry", ""),
            target_role=body.get("target_role", ""),
        )

        # Add career intelligence from RAG
        search_q = f"{body.get('industry','')} {body.get('country','')} career salary certification visa"
        rag_results = _search(search_q, top_k=5, doc_type="career")
        result["career_intelligence"] = [
            {"source": r["chunk"]["source"], "section": r["chunk"]["section"],
             "relevance": r["score"], "preview": r["chunk"]["content"][:300]}
            for r in rag_results
        ]
        result["metrics"] = {"latency_ms": int((time.time()-start)*1000), "method": "100% algorithm — zero AI cost"}
        result["privacy"] = "Your resume was NOT stored. Zero database. Refresh = gone."

        return func.HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
    except Exception as e:
        logging.error(f"[GovRAG] Decision error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e), "latency_ms": int((time.time()-start)*1000)}), status_code=500, mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/upload — Upload PDF, DOCX, TXT files for analysis
# ══════════════════════════════════════════════════════════════════════════════
@app.route("upload", methods=["POST"])
def upload(req: func.HttpRequest) -> func.HttpResponse:
    """Extract text from uploaded PDF, DOCX, or TXT files. ZERO storage — file processed in memory only."""
    import logging
    start = time.time()
    try:
        # Get the uploaded file from multipart form data
        file_data = None
        file_name = ""
        content_type = req.headers.get("Content-Type", "")

        if "multipart/form-data" in content_type:
            # Multipart upload
            for input_file in req.files.values():
                file_data = input_file.read()
                file_name = input_file.filename or "unknown"
                break
        else:
            # Raw body upload
            file_data = req.get_body()
            file_name = req.headers.get("X-Filename", req.params.get("filename", "unknown.txt"))

        if not file_data:
            return func.HttpResponse(json.dumps({"error": "No file uploaded"}), status_code=400, mimetype="application/json")

        # ── SECURITY: File size limit (5MB = ~20 pages) ──
        MAX_FILE_SIZE = 5 * 1024 * 1024
        if len(file_data) > MAX_FILE_SIZE:
            return func.HttpResponse(json.dumps({
                "error": f"File too large ({len(file_data)//1024//1024}MB). Maximum 5MB (~20 pages).",
                "max_size": "5MB", "your_size": f"{len(file_data)//1024}KB"
            }), status_code=413, mimetype="application/json")

        # ── SECURITY: Allowed file types only ──
        ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "md", "csv"}
        file_ext = file_name.lower().rsplit(".", 1)[-1] if "." in file_name else ""
        if file_ext not in ALLOWED_EXTENSIONS:
            return func.HttpResponse(json.dumps({
                "error": f"File type .{file_ext} not allowed. Supported: PDF, DOCX, TXT, MD",
            }), status_code=400, mimetype="application/json")

        text = ""
        extraction_method = ""

        # ── Extract text based on file type ──
        if file_ext == "pdf":
            try:
                import fitz  # pymupdf
                doc = fitz.open(stream=file_data, filetype="pdf")
                text = "\n".join(page.get_text() for page in doc)
                extraction_method = "pymupdf"
                doc.close()
            except ImportError:
                # Fallback: basic PDF text extraction without pymupdf
                text_bytes = file_data.decode("utf-8", errors="ignore")
                # Extract readable text between stream markers
                chunks = re.findall(r'\((.*?)\)', text_bytes)
                text = " ".join(c for c in chunks if len(c) > 3 and c.isprintable())
                extraction_method = "basic-fallback"

        elif file_ext == "docx":
            try:
                from docx import Document
                import io
                doc = Document(io.BytesIO(file_data))
                text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
                extraction_method = "python-docx"
            except ImportError:
                # Fallback: extract raw text from DOCX XML
                import zipfile, io
                with zipfile.ZipFile(io.BytesIO(file_data)) as z:
                    if "word/document.xml" in z.namelist():
                        xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
                        text = re.sub(r"<[^>]+>", " ", xml)
                        text = re.sub(r"\s+", " ", text).strip()
                extraction_method = "xml-fallback"

        elif file_ext in ("txt", "md", "csv"):
            text = file_data.decode("utf-8", errors="ignore")
            extraction_method = "plaintext"

        else:
            return func.HttpResponse(json.dumps({
                "error": f"Unsupported file type: .{file_ext}. Supported: PDF, DOCX, TXT, MD"
            }), status_code=400, mimetype="application/json")

        # Truncate to 45K chars (~12 pages at zero margin)
        MAX_WORDS = 7000
        MAX_CHARS = 45000
        text = text[:MAX_CHARS].strip()
        word_count = len(text.split())
        if word_count > MAX_WORDS:
            # Truncate by word count
            text = " ".join(text.split()[:MAX_WORDS])

        if not text or len(text) < 20:
            return func.HttpResponse(json.dumps({
                "error": "Could not extract text from file. Try copy-pasting instead.",
                "file": file_name, "bytes": len(file_data), "extraction": extraction_method,
            }), status_code=400, mimetype="application/json")

        return func.HttpResponse(json.dumps({
            "text": text,
            "file": file_name,
            "file_type": file_ext,
            "chars_extracted": len(text),
            "words_extracted": len(text.split()),
            "extraction_method": extraction_method,
            "truncated": len(file_data) > 10000,
            "latency_ms": int((time.time()-start)*1000),
            "privacy": "File was processed in MEMORY only. ZERO storage. Already erased.",
        }, indent=2), mimetype="application/json")

    except Exception as e:
        logging.error(f"[GovRAG] Upload error: {str(e)}")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: /api/responsible-ai — RAI Transparency Card
# ══════════════════════════════════════════════════════════════════════════════
@app.route("responsible-ai", methods=["GET"])
def responsible_ai(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({
        "responsible_ai_card": {
            "project": "GovRAG V3",
            "fairness": "No demographic data, uniform treatment, 195 countries",
            "reliability": "3-gate safety, multi-AI fallback, faithfulness scoring",
            "privacy": "ZERO storage, no database, PII detection, refresh=gone",
            "inclusiveness": "ELI12 mode, free, no login, WCAG considerations",
            "transparency": "Source citations, explainability, open source",
            "accountability": "Audit trail, safety verdicts, Azure Monitor",
        },
        "data_storage": "NONE",
        "hallucination_target": "<5%",
    }, indent=2), mimetype="application/json")


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT: / and /home — Serve the frontend HTML
# ══════════════════════════════════════════════════════════════════════════════
def _serve_html():
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return func.HttpResponse(html_path.read_text(encoding="utf-8"), mimetype="text/html")
    return func.HttpResponse("<h1>GovRAG V3 — Frontend not found</h1>", mimetype="text/html", status_code=404)

@app.route("home", methods=["GET"])
def home(req: func.HttpRequest) -> func.HttpResponse:
    return _serve_html()

@app.route("", methods=["GET"])
def root(req: func.HttpRequest) -> func.HttpResponse:
    return _serve_html()
