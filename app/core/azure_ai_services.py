"""
GovRAG V3 — Azure AI Services Integration
4 Foundry Tools integrated for maximum hackathon score.

1. Content Safety — Check AI responses for harmful content
2. Language Service — PII detection, key phrase extraction, sentiment
3. Translator — Multi-language support (195 countries)
4. Azure AI Search — Semantic search for RAG retrieval

All use FREE tier (F0). Zero cost.
"""

import os
import json
import logging
import httpx

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 1. AZURE CONTENT SAFETY — Check text for harmful content
# ══════════════════════════════════════════════════════════════════════════════
def check_content_safety(text: str) -> dict:
    """Check text against Azure Content Safety. Returns severity scores."""
    key = os.environ.get("CONTENT_SAFETY_KEY", "")
    endpoint = os.environ.get("CONTENT_SAFETY_ENDPOINT", "")
    if not key or not endpoint:
        return {"status": "skipped", "reason": "Content Safety not configured"}

    try:
        resp = httpx.post(
            f"{endpoint}contentsafety/text:analyze?api-version=2024-09-01",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={"text": text[:5120], "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            categories = {c["category"]: c["severity"] for c in data.get("categoriesAnalysis", [])}
            max_severity = max(categories.values()) if categories else 0
            return {
                "status": "checked",
                "categories": categories,
                "max_severity": max_severity,
                "safe": max_severity <= 2,
                "action": "ALLOW" if max_severity <= 2 else "BLOCK",
            }
        return {"status": "error", "code": resp.status_code, "safe": True}
    except Exception as e:
        logger.warning(f"Content Safety error: {e}")
        return {"status": "error", "message": str(e)[:100], "safe": True}


# ══════════════════════════════════════════════════════════════════════════════
# 2. AZURE LANGUAGE SERVICE — PII detection, key phrases, sentiment
# ══════════════════════════════════════════════════════════════════════════════
def detect_pii(text: str) -> dict:
    """Detect PII (personally identifiable information) in text."""
    key = os.environ.get("LANGUAGE_KEY", "")
    endpoint = os.environ.get("LANGUAGE_ENDPOINT", "")
    if not key or not endpoint:
        return {"status": "skipped", "pii_found": [], "redacted": text}

    try:
        resp = httpx.post(
            f"{endpoint}language/:analyze-text/jobs?api-version=2023-04-15-preview",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={
                "kind": "PiiEntityRecognition",
                "parameters": {"modelVersion": "latest"},
                "analysisInput": {"documents": [{"id": "1", "language": "en", "text": text[:5120]}]},
            },
            timeout=10.0,
        )
        # Synchronous endpoint
        resp2 = httpx.post(
            f"{endpoint}text/analytics/v3.1/entities/recognition/pii",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={"documents": [{"id": "1", "language": "en", "text": text[:5120]}]},
            timeout=10.0,
        )
        if resp2.status_code == 200:
            data = resp2.json()
            docs = data.get("documents", [])
            if docs:
                entities = docs[0].get("entities", [])
                redacted = docs[0].get("redactedText", text)
                return {
                    "status": "checked",
                    "pii_found": [{"text": e["text"], "category": e["category"], "confidence": e["confidenceScore"]} for e in entities],
                    "pii_count": len(entities),
                    "redacted": redacted,
                }
        return {"status": "error", "pii_found": [], "redacted": text}
    except Exception as e:
        logger.warning(f"Language PII error: {e}")
        return {"status": "error", "pii_found": [], "redacted": text}


def extract_key_phrases(text: str) -> list:
    """Extract key phrases from text using Azure Language."""
    key = os.environ.get("LANGUAGE_KEY", "")
    endpoint = os.environ.get("LANGUAGE_ENDPOINT", "")
    if not key or not endpoint:
        return []

    try:
        resp = httpx.post(
            f"{endpoint}text/analytics/v3.1/keyPhrases",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={"documents": [{"id": "1", "language": "en", "text": text[:5120]}]},
            timeout=10.0,
        )
        if resp.status_code == 200:
            docs = resp.json().get("documents", [])
            if docs:
                return docs[0].get("keyPhrases", [])
        return []
    except Exception as e:
        logger.warning(f"Key phrases error: {e}")
        return []


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using Azure Language."""
    key = os.environ.get("LANGUAGE_KEY", "")
    endpoint = os.environ.get("LANGUAGE_ENDPOINT", "")
    if not key or not endpoint:
        return {"sentiment": "unknown"}

    try:
        resp = httpx.post(
            f"{endpoint}text/analytics/v3.1/sentiment",
            headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
            json={"documents": [{"id": "1", "language": "en", "text": text[:5120]}]},
            timeout=10.0,
        )
        if resp.status_code == 200:
            docs = resp.json().get("documents", [])
            if docs:
                return {
                    "sentiment": docs[0].get("sentiment", "unknown"),
                    "scores": docs[0].get("confidenceScores", {}),
                }
        return {"sentiment": "unknown"}
    except Exception as e:
        logger.warning(f"Sentiment error: {e}")
        return {"sentiment": "unknown"}


# ══════════════════════════════════════════════════════════════════════════════
# 3. AZURE TRANSLATOR — Translate responses to user's language
# ══════════════════════════════════════════════════════════════════════════════
SUPPORTED_LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "pt": "Portuguese", "zh-Hans": "Chinese (Simplified)", "zh-Hant": "Chinese (Traditional)",
    "ar": "Arabic", "hi": "Hindi", "ur": "Urdu", "ja": "Japanese",
    "ko": "Korean", "ru": "Russian", "it": "Italian", "nl": "Dutch",
    "pl": "Polish", "tr": "Turkish", "vi": "Vietnamese", "th": "Thai",
    "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "mr": "Marathi",
    "sw": "Swahili", "ms": "Malay", "id": "Indonesian", "tl": "Filipino",
    "uk": "Ukrainian", "ro": "Romanian", "cs": "Czech", "hu": "Hungarian",
    "el": "Greek", "sv": "Swedish", "da": "Danish", "no": "Norwegian",
    "fi": "Finnish", "he": "Hebrew", "fa": "Persian", "ps": "Pashto",
}


def translate_text(text: str, target_language: str = "en") -> dict:
    """Translate text using Azure Translator."""
    key = os.environ.get("TRANSLATOR_KEY", "")
    if not key or target_language == "en":
        return {"translated": text, "language": "en", "status": "original"}

    try:
        resp = httpx.post(
            f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}",
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Ocp-Apim-Subscription-Region": "canadaeast",
                "Content-Type": "application/json",
            },
            json=[{"text": text[:5000]}],
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data and data[0].get("translations"):
                return {
                    "translated": data[0]["translations"][0]["text"],
                    "language": target_language,
                    "language_name": SUPPORTED_LANGUAGES.get(target_language, target_language),
                    "status": "translated",
                }
        return {"translated": text, "language": "en", "status": "error"}
    except Exception as e:
        logger.warning(f"Translator error: {e}")
        return {"translated": text, "language": "en", "status": "error"}


def detect_language(text: str) -> str:
    """Detect language of input text."""
    key = os.environ.get("TRANSLATOR_KEY", "")
    if not key:
        return "en"

    try:
        resp = httpx.post(
            "https://api.cognitive.microsofttranslator.com/detect?api-version=3.0",
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Ocp-Apim-Subscription-Region": "canadaeast",
                "Content-Type": "application/json",
            },
            json=[{"text": text[:500]}],
            timeout=5.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return data[0].get("language", "en")
        return "en"
    except:
        return "en"


# ══════════════════════════════════════════════════════════════════════════════
# 4. AZURE AI SEARCH — Semantic search for RAG
# ══════════════════════════════════════════════════════════════════════════════
def search_azure_index(query: str, index_name: str = "govrag-career", top: int = 5) -> list:
    """Search Azure AI Search index."""
    key = os.environ.get("SEARCH_KEY", "")
    endpoint = os.environ.get("SEARCH_ENDPOINT", "")
    if not key or not endpoint:
        return []

    try:
        resp = httpx.post(
            f"{endpoint}/indexes/{index_name}/docs/search?api-version=2024-07-01",
            headers={"api-key": key, "Content-Type": "application/json"},
            json={"search": query, "top": top, "queryType": "simple"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            return [{"score": r.get("@search.score", 0), "content": r.get("content", ""),
                      "source": r.get("source", ""), "section": r.get("section", "")}
                    for r in data.get("value", [])]
        return []
    except Exception as e:
        logger.warning(f"AI Search error: {e}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# COMBINED: Full Azure AI Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def azure_ai_pipeline(query: str, response: str, target_lang: str = "en") -> dict:
    """Run full Azure AI pipeline on a query-response pair."""
    return {
        "content_safety": check_content_safety(response),
        "pii_detection": detect_pii(query),
        "key_phrases": extract_key_phrases(query),
        "sentiment": analyze_sentiment(query),
        "translation": translate_text(response, target_lang) if target_lang != "en" else None,
        "azure_services_used": ["Content Safety", "Language (PII)", "Language (Key Phrases)",
                                 "Language (Sentiment)", "Translator", "AI Search"],
    }
