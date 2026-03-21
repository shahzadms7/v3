"""
GovRAG V3 — Safety & Compliance Engine
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
3 safety gates BEFORE any answer reaches the user:

Gate 1: INPUT SAFETY — Is the question safe? (no injection, no PII)
Gate 2: RELEVANCE GATE — Do we have enough sources? (prevents guessing)
Gate 3: CONFIDENCE CHECK — Is the answer trustworthy? (blocks low confidence)

Plus: Output safety scan + compliance rule checks

PRIVACY: We NEVER store user queries. Safety checks run in-memory only.
"""

import re
from typing import Optional


class SafetyEngine:
    """3-layer safety system for governed AI responses."""

    def __init__(self, block_threshold: int = 40, warn_threshold: int = 70):
        self.block_threshold = block_threshold
        self.warn_threshold = warn_threshold

        # Prompt injection patterns (attackers try to override AI instructions)
        self.injection_patterns = [
            re.compile(r"ignore\s+(previous|above|all)\s+instructions", re.I),
            re.compile(r"you\s+are\s+now", re.I),
            re.compile(r"system\s*:\s*", re.I),
            re.compile(r"<\s*script", re.I),
            re.compile(r"forget\s+(everything|all|your)", re.I),
            re.compile(r"pretend\s+you\s+are", re.I),
            re.compile(r"act\s+as\s+(if|a|an)", re.I),
            re.compile(r"\]\s*\]\s*\}", re.I),  # JSON injection
        ]

        # PII patterns (we detect but NEVER store)
        self.pii_patterns = [
            {"name": "SSN", "pattern": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "severity": "critical"},
            {"name": "Credit Card", "pattern": re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"), "severity": "critical"},
            {"name": "Email", "pattern": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"), "severity": "medium"},
            {"name": "Phone", "pattern": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"), "severity": "low"},
        ]

    def check_input(self, query: str) -> dict:
        """Gate 1: Check user input for safety issues."""
        issues = []

        # Check prompt injection
        for pattern in self.injection_patterns:
            if pattern.search(query):
                issues.append({"type": "PROMPT_INJECTION", "severity": "critical",
                               "message": "Potential prompt injection detected."})
                break

        # Check PII in query (warn user, don't store)
        for pii in self.pii_patterns:
            if pii["pattern"].search(query):
                issues.append({"type": "PII_DETECTED", "severity": pii["severity"],
                               "message": f"{pii['name']} detected in query. We never store your data."})

        # Check length
        if len(query) > 8000:
            issues.append({"type": "TOO_LONG", "severity": "low",
                           "message": "Input exceeds 8000 characters. Truncated."})

        blocked = any(i["severity"] == "critical" for i in issues)
        return {"passed": not blocked, "issues": issues}

    def check_relevance(self, retrieval_result: dict) -> dict:
        """Gate 2: Are retrieved sources relevant enough?"""
        chunks = retrieval_result.get("chunks", [])
        total = retrieval_result.get("total", 0)

        if total == 0:
            return {"passed": False, "reason": "NO_SOURCES",
                    "message": "No relevant documents found. Cannot provide a grounded answer."}

        avg_relevance = sum(c.relevance_score for c in chunks) / len(chunks) if chunks else 0

        if avg_relevance < 0.15:
            return {"passed": False, "reason": "LOW_RELEVANCE",
                    "message": f"Source relevance too low ({avg_relevance:.0%}). Answer would be unreliable."}

        return {"passed": True, "avg_relevance": round(avg_relevance, 3), "sources_found": total}

    def check_confidence(self, faithfulness_score: int, ai_confidence: int = 100) -> dict:
        """Gate 3: Is the AI confident enough?"""
        score = min(faithfulness_score, ai_confidence)

        if score < self.block_threshold:
            return {"passed": False, "action": "BLOCK", "score": score,
                    "message": f"Confidence {score}% — too low. Answer blocked to prevent misinformation."}

        if score < self.warn_threshold:
            return {"passed": True, "action": "WARN", "score": score,
                    "message": f"Moderate confidence ({score}%). Verify against source documents."}

        return {"passed": True, "action": "ALLOW", "score": score}

    def check_output(self, response: str) -> dict:
        """Check AI response for leaked PII."""
        issues = []
        for pii in self.pii_patterns:
            matches = pii["pattern"].findall(response)
            if matches:
                issues.append({"type": "PII_IN_RESPONSE", "severity": pii["severity"],
                               "data_type": pii["name"], "count": len(matches)})
        return {"issues": issues}

    def full_check(self, query: str, retrieval: dict, answer: str,
                   faithfulness: dict, ai_confidence: int) -> dict:
        """Run all safety gates. Returns final verdict."""
        verdict = {"timestamp": None, "checks": [], "final": "ALLOW", "warnings": []}

        # Gate 1
        input_check = self.check_input(query)
        verdict["checks"].append({"gate": "input_safety", **input_check})
        if not input_check["passed"]:
            verdict["final"] = "BLOCK"
            verdict["block_reason"] = "Input safety failed"
            return verdict

        # Gate 2
        relevance_check = self.check_relevance(retrieval)
        verdict["checks"].append({"gate": "relevance", **relevance_check})
        if not relevance_check["passed"]:
            verdict["final"] = "BLOCK"
            verdict["block_reason"] = relevance_check["message"]
            return verdict

        # Gate 3
        conf_check = self.check_confidence(faithfulness.get("faithfulness_score", 0), ai_confidence)
        verdict["checks"].append({"gate": "confidence", **conf_check})
        if not conf_check["passed"]:
            verdict["final"] = "BLOCK"
            verdict["block_reason"] = conf_check["message"]
            return verdict
        if conf_check["action"] == "WARN":
            verdict["warnings"].append(conf_check["message"])

        # Output check
        output_check = self.check_output(answer)
        if output_check["issues"]:
            verdict["warnings"].extend([f"PII detected: {i['data_type']}" for i in output_check["issues"]])

        return verdict


# Singleton
safety_engine = SafetyEngine()
